# DevObs <img width="940" height="324" alt="image" src="https://github.com/user-attachments/assets/4f6a7cec-fc80-4bc7-a54c-343c5dc4e753" />




**DevObs** — short for **Dev**Ops + **Obs**ervability — is an MCP (Model Context Protocol) server that lets you check system health, manage Docker containers, debug network issues, and inspect application logs, all through natural conversation with an AI assistant instead of juggling a dozen terminal commands.

Ask questions like *"is my rabbitmq container running?"*, *"why can't I reach port 8080?"*, or *"show me the last 20 error logs"* — and get answers directly, without leaving your chat interface.

## Why "DevObs"?

The name reflects exactly what this tool does — it sits at the intersection of two disciplines:

- **DevOps** — managing infrastructure day-to-day: starting/stopping containers, checking what's running, keeping services healthy
- **Observability** — understanding the current state of a system: CPU, memory, disk, network reachability, and logs

DevObs doesn't replace full observability platforms like Prometheus or Datadog (it has no historical metrics or alerting), but it **replaces the manual, repetitive triage work** those platforms don't cover — the "let me quickly check five things across five terminal windows" moment every developer and DevOps engineer knows well.

## Who this helps

**Developers** who just want a fast answer without memorizing Docker flags, `psutil` syntax, or `nc`/`curl` incantations — describe what you need in plain language.

**DevOps / SRE engineers** doing quick incident triage — check container status, restart a crashed service, verify a port is open, and read recent logs, all in one continuous conversation instead of bouncing between tools.

**On-call engineers at 2am** who want the fastest path from "something's wrong" to "here's what's actually happening," especially useful for less experienced team members during a rotation.

## What it can do

| Category | Capabilities |
|---|---|
| **System Metrics** | CPU, memory, disk usage; uptime; overall health report; top CPU/memory processes; find a process by name |
| **Networking** | DNS resolution; check local/remote port status; check if an HTTP endpoint is reachable |
| **Docker** | List, start, stop, restart containers; get detailed container status; live CPU/memory/network container stats; container logs; pull + create a new container if it doesn't exist |
| **Logs** | Read the full application log; tail the last N lines; search by keyword; count entries by level (INFO/WARN/ERROR) |

## Requirements

- Python **3.13+**
- [uv](https://docs.astral.sh/uv/) (for dependency management)
- Docker installed and running (required for all Docker-related tools)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/devobs.git
   cd devobs
   ```

2. **Install dependencies with `uv`:**
   ```bash
   uv sync
   ```
   This reads `pyproject.toml` / `uv.lock` and creates a `.venv` automatically.

3. **Run the server:**
   ```bash
   uv run main.py
   ```
   By default, the server starts on `http://0.0.0.0:8090`.

## Connecting DevObs to your AI assistant

DevObs speaks MCP over HTTP. Add it to your MCP client configuration (e.g., Claude Desktop, or any MCP-compatible client) by pointing it at:

```
http://localhost:8090
```

Once connected, you can start asking questions directly — no special syntax needed. Examples:

- "What's my current CPU and memory usage?"
- "List all my Docker containers"
- "Restart the `rabbitmq` container"
- "Check if google.com is reachable on port 443"
- "Show me the last 10 log lines"
- "How many ERROR entries are in the logs?"

## Project structure

```
devobs/
├── main.py              # MCP server entry point — registers all tools
├── tools/                # Thin MCP-facing wrapper functions
├── services/             # Actual logic (psutil, docker SDK, socket, etc.)
├── sample_logs/          # Sample application.log used by the log tools
├── pyproject.toml         # Project metadata & dependencies
├── uv.lock                # Locked dependency versions
└── .python-version         # Pinned Python version
```

## ⚠️ Security — read this before deploying beyond localhost

DevObs is built for **local development and personal/trusted-network use**. Before exposing it more broadly (a shared server, a public URL, a team environment), be aware of the following:

- **No authentication is implemented.** Anyone who can reach the server's port can call *any* tool — including destructive ones like `stop_container`, `restart_container`, and `start_or_create_container`.
- **`create_or_start_container` can pull and run arbitrary Docker images and mount arbitrary host paths.** Without access control, this is equivalent to giving a caller shell-level access to your Docker host.
- **CORS is currently wide open (`allow_origins=["*"]`).** This is convenient for local development but means any website's JavaScript could call this server if it's reachable.
- **This server needs access to the Docker socket**, which is itself a highly privileged resource on any machine.

### Before deploying this beyond your own machine, you should:

1. **Add an authentication layer** — at minimum, a shared-secret/API key check on incoming requests; ideally OAuth or a proper identity provider if multiple people will use it.
2. **Restrict CORS** to only the specific origins that need access, not `*`.
3. **Consider read-only vs. read-write modes** — you may want a deployment mode that disables destructive tools (`stop_container`, `restart_container`, `start_or_create_container`) entirely for less-trusted contexts.
4. **Run behind a reverse proxy** (e.g., nginx, Caddy) with TLS if exposed over a network.
5. **Scope Docker socket access carefully** — consider running this in an environment where the "blast radius" of a compromised or misused server is limited.

**In short: treat this as a powerful admin tool, not a public-facing service, until you've added the access controls above.**

## Contributing

Issues and pull requests are welcome. If you're adding new tools, please keep the `tools/` (MCP-facing) and `services/` (actual logic) separation intact — it keeps the codebase testable and easy to reason about.

## License - MIT

contact me at - mohdalisaad868@gmail.com
