# DeepSearch CLI

A dedicated command-line interface (CLI) client for connecting and interacting with a private `deep-search` service.

> **⚠️ IMPORTANT NOTICE**
>
> This project is **strictly a client application** and is highly dependent on a **private `deep-search` backend service**. It **cannot** be used as a standalone local search tool. If you do not have access to the required backend service and its configuration environment, this client will not function.

## Installation

You can easily install or update the `deep-search` client directly from the public internet using the following command:

```bash
curl -sSL https://raw.githubusercontent.com/radiumce/deep-search-cli/main/scripts/install-cli.sh | bash
```

The installation script will automatically fetch the latest `deep-search` client from GitHub and install it into your user's `~/.local/bin` directory.

*(Note: After installation, please ensure that `~/.local/bin` is added to your system's `PATH` environment variable)*

## Configuration & Usage

Before using the client, you must specify the address of your private server:

```bash
deep-search --server <YOUR_PRIVATE_SERVER_URL>
```

### Basic Commands

- **Smart Search (Search):**
  ```bash
  deep-search search "Your search query"
  ```

- **Web Extraction (Browse):**
  ```bash
  deep-search browse "https://example.com"
  ```

- **Check Configuration and Server Health:**
  ```bash
  deep-search
  ```
