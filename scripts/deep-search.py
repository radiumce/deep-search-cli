#!/usr/bin/env python3
"""
Standalone Zero-Dependency CLI Client for DeepSearch.

Usage:
  deep-search                         # Show current server config and check health
  deep-search --server <url>          # Set the API server URL
  deep-search search [REQUESTS...]    # Execute search
  deep-search browse [URLS...]        # Execute web extraction
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

CONFIG_DIR = Path.home() / ".deep-search"
CONFIG_FILE = CONFIG_DIR / "config.json"
DEFAULT_SERVER = "http://127.0.0.1:8000"


def load_config() -> dict:
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"server": DEFAULT_SERVER}


def save_config(config: dict) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)


def get_server() -> str:
    config = load_config()
    server = config.get("server", DEFAULT_SERVER)
    # Strip trailing slash
    if server.endswith("/"):
        server = server[:-1]
    return server


def format_output(results: list, requests: list, command: str) -> str:
    """Format the results into a readable text output."""
    output = []
    output.append(f"=== DeepSearch {command.capitalize()} Results ===")
    
    for i, (req, res) in enumerate(zip(requests, results), 1):
        output.append("-" * 40)
        output.append(f"Request [{i}/{len(requests)}]: {req}")
        output.append("-" * 40)
        output.append(str(res))
        output.append("\n")
        
    return "\n".join(output)


def post_request(endpoint: str, payload: dict, timeout: float) -> dict:
    server = get_server()
    url = f"{server}{endpoint}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, 
        data=data, 
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            frames = ["⏳", "⌛"]
            frame_idx = 0
            
            for line in response:
                if not line.strip():
                    continue
                try:
                    data = json.loads(line.decode("utf-8"))
                    if data.get("type") == "heartbeat":
                        sys.stderr.write(f"\r{frames[frame_idx]} Waiting for server... ")
                        sys.stderr.flush()
                        frame_idx = (frame_idx + 1) % len(frames)
                    elif data.get("type") == "result":
                        sys.stderr.write("\r" + " " * 30 + "\r")
                        sys.stderr.flush()
                        return data
                    elif data.get("type") == "error":
                        sys.stderr.write("\r" + " " * 30 + "\r")
                        sys.stderr.flush()
                        print(f"Server error: {data.get('error')}", file=sys.stderr)
                        sys.exit(1)
                    else:
                        # Fallback for non-streaming old API responses
                        return data
                except json.JSONDecodeError:
                    pass
            return {}
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        try:
            err_json = json.loads(body)
            msg = err_json.get("error", body)
        except Exception:
            msg = body
        print(f"Server returned HTTP {e.code}: {msg}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Error: Could not connect to the server at {server}", file=sys.stderr)
        print(f"       Reason: {e.reason}", file=sys.stderr)
        print("       Please ensure the server is running or configure a different server using:", file=sys.stderr)
        print("       deep-search --server <url>", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Request failed: {e}", file=sys.stderr)
        sys.exit(1)


def get_request(endpoint: str, timeout: float = 10.0) -> dict:
    server = get_server()
    url = f"{server}{endpoint}"
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        try:
            err_json = json.loads(body)
            msg = err_json.get("error", body)
        except Exception:
            msg = body
        print(f"Server returned HTTP {e.code}: {msg}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Error: Could not connect to the server at {server}", file=sys.stderr)
        print(f"       Reason: {e.reason}", file=sys.stderr)
        print("       Please ensure the server is running or configure a different server using:", file=sys.stderr)
        print("       deep-search --server <url>", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Request failed: {e}", file=sys.stderr)
        sys.exit(1)


def print_status() -> None:
    server = get_server()
    print(f"Configured API Server: {server}")
    print("Checking server health...")
    try:
        resp = get_request("/api/health")
        if resp.get("status") == "ok":
            print(f"[*] Server is up and running. (Version {resp.get('version', 'unknown')})")
        else:
            print(f"[!] Server responded with unknown status: {resp}")
    except SystemExit:
        pass


def main():
    parser = argparse.ArgumentParser(
        description="DeepSearch CLI standalone client.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--server",
        type=str,
        help="Set the deepsearch-mcp API server URL globally"
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=420.0,
        help="Timeout in seconds for operations (default: 420.0)"
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    search_parser = subparsers.add_parser("search", help="Execute intelligent search")
    search_parser.add_argument("requests", nargs="+", help="One or more search requests")

    browse_parser = subparsers.add_parser("browse", help="Execute web extraction")
    browse_parser.add_argument("requests", nargs="+", help="Target URLs or extraction requests")

    args = parser.parse_args()

    # Handle global flags without subcommand first
    if args.server:
        config = load_config()
        config["server"] = args.server
        save_config(config)
        print(f"Server URL updated to: {args.server}")
        if not args.command:
            print_status()
            sys.exit(0)

    if not args.command:
        if args.server:
            # handled above
            pass
        else:
            print_status()
        sys.exit(0)

    if args.command == "search":
        resp = post_request("/api/search", {"requests": args.requests}, args.timeout)
        results = resp.get("results", [])
        if not isinstance(results, list):
             results = [results]
        print(format_output(results, args.requests, "Search"))

    elif args.command == "browse":
        resp = post_request("/api/browse", {"requests": args.requests}, args.timeout)
        results = resp.get("results", [])
        if not isinstance(results, list):
             results = [results]
        print(format_output(results, args.requests, "Browse"))


if __name__ == "__main__":
    main()
