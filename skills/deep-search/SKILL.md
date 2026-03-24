---
name: "deep-search"
description: "Core workflow skill: Responsible for task decomposition, progress tracking according to the plan skill instructions, and leveraging the DeepSearch tool to acquire key information."
version: "2.0.0"
---

# CLI Tool Usage & Connections

When you need to perform searches, you should use the `deep-search` CLI client. The CLI communicates with the DeepSearch backend server to perform intelligent, agentic searches and browser extractions.

### Installation
If the `deep-search` command is not found or not installed in your environment, you must install it directly from the public internet using the following command:
```bash
curl -sSL https://raw.githubusercontent.com/radiumce/deep-search-cli/main/scripts/install-cli.sh | bash
```
*(Ensure `~/.local/bin` is added to your `PATH` after installation).*

### Checking Server Connection
If the `deep-search` command fails with a connection error (e.g., "Cannot reach server" or "Connection refused"), you should:
1. Run `deep-search` with no arguments to view the currently configured API server and check its health status.
2. If the server is unreachable, ask the user for the correct server URL.
3. Configure the correct server explicitly using the `--server` flag:
   `deep-search --server <service_url>`

### CLI Usage Examples
- **Check Status / Health:** 
  `deep-search`
- **Configure Server:** 
  `deep-search --server http://127.0.0.1:7572`
- **Single Search Request:**
  `deep-search search "latest developments in quantum computing"`
- **Parallel Search Requests (Batch):**
  `deep-search search "history of the electric car" "current EV market share in 2026"`
- **Web Extraction (Browse):**
  `deep-search browse "https://en.wikipedia.org/wiki/Artificial_intelligence"`

# Application Scenarios & Tool Selection
- When the search, analysis, or research work is highly professional or domain-specific, it should take priority to be executed via the `deep-search` CLI tool.
- Multi-step research tasks must be planned and tracked properly, using the `deep-search` tool to execute the actual searching phases.

# DeepSearch Guidelines
Follow these guidelines when executing tasks that require external information input:

0. **Search Request Specification**
    - The search task is executed by sub-agents encapsulated within the tool. Therefore, when sending a search request, avoid asking the sub-agent to provide "opinions"; instead, request "facts". For example:
        * *"Research the solution for problem X"* implies an expectation for subjective judgment and thinking. This is a bad search request.
        * *"Find documentation and materials on industry solutions used to solve problem X"* is a good request because it simply asks the search agent to extract objective search results.

1.  **Timeliness Constraints**
    - Before executing a search, if the work involves a specific point in time or requires the latest data, you **must** call a `time` or `date` CLI command to confirm the current time, otherwise, ask the user first.

2.  **Search Execution Standards**
    - **Single Cohesion**: A single, non-parallel search task should fulfill one single, cohesive search requirement.
    - **Parallel Acceleration**: When there are multiple independent search or page extraction tasks, actively use the parallel batch capabilities of the `deep-search` CLI (by passing multiple arguments) to accelerate the workflow.
    - **Decision Support**: Utilize search to assist in tool selection or solution comparison (e.g., search "Pros and cons of Solution A vs Solution B").

3.  **Result Processing**
    - Perform semantic understanding of the search results rather than mechanical matching.
    - The information gathered from the search should act as the input for your next planning phase or task execution.
