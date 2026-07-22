"""MCP server for the Academic Intelligence Platform.

Exposes the same read-only SQL capability the Streamlit agent uses, so ANY MCP
client (Claude Desktop, Cursor, a Claude.ai custom connector, ...) can query the
academic data with its own LLM -- no OpenRouter key needed on this path.

Thin wrapper over aip/db.py: that module already enforces read-only at the engine,
rejects multi-statement / non-SELECT SQL, and times out runaway queries.

Run locally (stdio, for Claude Desktop / Cursor):   python mcp_server.py
Run as a remote connector (HTTP):                   python mcp_server.py --http
"""
import os
import sys

# Resolve data + docs against THIS file, so the server works from any cwd
# (MCP clients launch it with an arbitrary working directory).
ROOT = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("AIP_DB", os.path.join(ROOT, "data", "aip.duckdb"))

from mcp.server.fastmcp import FastMCP  # noqa: E402

from aip import db  # noqa: E402

mcp = FastMCP(
    "aip",
    instructions=(
        "Academic Intelligence Platform: NIAT/NxtWave academic data (what was "
        "planned, delivered, its content, and student feedback) in one DuckDB store. "
        "Call guide() and describe_schema() BEFORE writing SQL -- the join keys are "
        "non-obvious and a naive join gives a confidently wrong answer. Then use "
        "run_sql() (read-only SELECT/WITH only)."
    ),
)

MAX_DISPLAY_ROWS = 200


def _load(*names):
    parts = []
    for n in names:
        p = os.path.join(ROOT, "docs", n)
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                parts.append(f.read())
    return "\n\n---\n\n".join(parts)


@mcp.tool()
def guide() -> str:
    """The join contract, data caveats, and ready-made query recipes. Read this
    FIRST -- it is what stops a plausible-but-wrong join."""
    return _load("data-notes.md", "examples.md")


@mcp.tool()
def describe_schema() -> str:
    """Live schema: every table/view with its columns, types, and row count."""
    return db.schema_text()


@mcp.tool()
def run_sql(query: str) -> str:
    """Run one read-only SQL query (SELECT/WITH only) and return the rows as a
    table. Writes, DDL, and multi-statement input are rejected at the engine."""
    try:
        cols, rows, truncated = db.run_sql(query)
    except db.QueryError as e:
        return f"QUERY REJECTED: {e}"  # fed back so the model can repair
    if not rows:
        return "(0 rows)"
    lines = [" | ".join(cols)]
    for r in rows[:MAX_DISPLAY_ROWS]:
        lines.append(" | ".join("" if c is None else str(c)[:80] for c in r))
    note = []
    if len(rows) > MAX_DISPLAY_ROWS:
        note.append(f"showing {MAX_DISPLAY_ROWS} of {len(rows)} rows")
    if truncated:
        note.append("result capped at 1000 rows -- add LIMIT or aggregate")
    if note:
        lines.append(f"[{'; '.join(note)}]")
    return "\n".join(lines)


@mcp.resource("aip://guide")
def guide_resource() -> str:
    """Same content as guide(), for clients that read resources."""
    return _load("data-notes.md", "examples.md")


if __name__ == "__main__":
    transport = "streamable-http" if "--http" in sys.argv else "stdio"
    mcp.run(transport=transport)
