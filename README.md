# nishati-mcp

## Why This Exists

Getting connected to power in Kenya — or deciding between grid and off-grid solar — depends on tariff bands, connection procedures and subsidy programmes that are difficult to compare side by side. Energy access decisions are long-lived and expensive to reverse, so the comparison matters more than the brochure.

## Install

```bash
pip install nishati-mcp
```

## Tools (5)

- **`kplc_connection_guide`** —   
  <sub>args: county, connection_type</sub>
- **`tariff_calculator`** —   
  <sub>args: monthly_units_kwh, customer_type</sub>
- **`solar_options_guide`** —   
  <sub>args: budget_kes, use_case</sub>
- **`energy_subsidy_programs`** —   
  <sub>args: county</sub>
- **`energy_rights_query`** —   
  <sub>args: topic</sub>

## Example

```python
from nishati_mcp.server import tariff_calculator

result = tariff_calculator(units_kwh=150)
# band breakdown, levies, estimated bill
```

## Claude Desktop Integration

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "nishati-mcp": {
      "command": "python",
      "args": ["-m", "nishati_mcp.server"]
    }
  }
}
```

## Data & Disclaimers

Tariffs are set by EPRA and revised periodically. Treat calculations as indicative and confirm current rates with KPLC or epra.go.ke before relying on them.

Every tool response carries a `source` field. Responses labelled `DEMO` are
illustrative reference data, not a live feed — verify against the authority
named in the response before acting on it.

## Part of the East Africa Coordination Stack

This MCP server is one of 32 tools in the Kenya coordination infrastructure.
Connect it to [`africa-coord-bus`](https://github.com/gabrielmahia/africa-coord-bus) —
the coordination event bus that routes signals between domains automatically.

```bash
pip install africa-coord-bus
```

All 32 servers: [pypi.org/user/gmahia](https://pypi.org/user/gmahia/)
Live demo: [coord-cascade-demo](https://github.com/gabrielmahia/coord-cascade-demo)

## IP & Collaboration

MIT licensed. Feedback via GitHub Issues only — pull requests are not accepted. Demo data is labeled DEMO and is not suitable for operational decisions. Full policy: [docs/architecture/IP_POLICY.md](docs/architecture/IP_POLICY.md). Security reports: see [SECURITY.md](SECURITY.md).

<!-- interconnect:v1 -->
## Part of the East Africa coordination stack

- **Install & run:** `pip install reli-cli && reli list` — 33 MCP servers on the [official MCP Registry](https://registry.modelcontextprotocol.io) under `io.github.gabrielmahia`
- **Evaluate any model on Swahili agent tasks:** [kipimo](https://github.com/gabrielmahia/kipimo) · [dataset](https://huggingface.co/datasets/gmahia/kipimo) · [leaderboard](https://huggingface.co/spaces/gmahia/kipimo-leaderboard)
- **Coordinate across servers:** [africa-coord-bus](https://pypi.org/project/africa-coord-bus/) — offline-first event bus with a built-in Kenya routing table
- **Datasets:** [huggingface.co/gmahia](https://huggingface.co/gmahia) · **Docs hub:** [nairobi-stack](https://github.com/gabrielmahia/nairobi-stack)

Model-agnostic by design: closed APIs, open-weight models, and small distilled models are all first-class citizens.
<!-- /interconnect:v1 -->
