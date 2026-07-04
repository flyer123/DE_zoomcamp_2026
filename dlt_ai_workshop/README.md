## Workshop Instructions

[](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2026/workshops/dlt/README.md#workshop-instructions)

### Step 1: Create a New Project Folder

[](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2026/workshops/dlt/README.md#step-1-create-a-new-project-folder)

Create a fresh folder for your pipeline and open it in Cursor (or your preferred agentic IDE):

mkdir my-dlt-pipeline
cd my-dlt-pipeline

### Step 2: Add the dlt MCP Server Config

[](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2026/workshops/dlt/README.md#step-2-add-the-dlt-mcp-server-config)

Choose the setup for your IDE:

Cursor - go to **Settings → Tools & MCP → New MCP Server** and add:
{
  "mcpServers": {
    "dlt": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "dlt[duckdb]",
        "--with",
        "dlt-mcp[search]",
        "python",
        "-m",
        "dlt_mcp"
      ]
    }
  }
}



### Step 3: Install dlt Workspace

[](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2026/workshops/dlt/README.md#step-3-install-dlt-workspace)

    pip install "dlt[workspace]"

### Step 4: Initialize the dlt Project



    dlt init dlthub:open_library duckdb

This scaffolds the pipeline files and configuration for Open Library. You now have everything you need to start prompting.

> 📖 **Reference:** [Open Library Workspace Instructions](https://dlthub.com/workspace/source/open-library)

### Step 5: Prompt the Agent to Build and Run the Pipeline

[](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2026/workshops/dlt/README.md#step-5-prompt-the-agent-to-build-and-run-the-pipeline)

This is where the magic happens. The `dlt init` command scaffolds sample prompts you can use. Here's an example to get started:

```

   
Build a REST API source for NYC taxi data.

API details:
- Base URL: https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api
- Data format: Paginated JSON (1,000 records per page)
- Pagination: Stop when an empty page is returned

Place the code in taxi_pipeline.py and name the pipeline taxi_pipeline.
Use @dlt rest api as a tutorial.

```
#Step 6: Run and Debug

Run your pipeline and iterate with the agent until it works:

    python taxi_pipeline.py




