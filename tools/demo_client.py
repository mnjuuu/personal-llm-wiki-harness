#!/usr/bin/env python3
"""Small demo client for the local wiki MCP server."""

from __future__ import annotations

import json
import subprocess
import sys


def send(proc: subprocess.Popen[str], request: dict) -> dict:
    assert proc.stdin and proc.stdout
    proc.stdin.write(json.dumps(request, ensure_ascii=False) + "\n")
    proc.stdin.flush()
    return json.loads(proc.stdout.readline())


def main() -> int:
    proc = subprocess.Popen(
        [sys.executable, "tools/wiki_mcp_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
    )
    try:
        print(send(proc, {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}))
        print(send(proc, {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}))
        print(
            send(
                proc,
                {
                    "jsonrpc": "2.0",
                    "id": 3,
                    "method": "tools/call",
                    "params": {
                        "name": "wiki.query",
                        "arguments": {"question": "What does the wiki harness provide?"},
                    },
                },
            )
        )
    finally:
        proc.terminate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

