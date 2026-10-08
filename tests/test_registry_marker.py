import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]


def test_the_readme_carries_the_mcp_registry_marker():
    """The MCP registry refuses a release whose PyPI README lacks 'mcp-name: <server name>' (it silently stopped habari, nishati and jumuia from updating)."""
    name = json.loads((ROOT / "server.json").read_text(encoding="utf-8"))["name"]
    assert f"mcp-name: {name}" in (ROOT / "README.md").read_text(encoding="utf-8")
