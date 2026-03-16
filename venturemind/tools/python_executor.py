"""Controlled Python execution environment for calculations."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


SAFE_BUILTINS = {
    "abs": abs,
    "min": min,
    "max": max,
    "sum": sum,
    "len": len,
    "round": round,
    "sorted": sorted,
    "range": range,
}


@dataclass
class PythonExecutor:
    """Executes small Python snippets with restricted globals."""

    def run(self, code: str, variables: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """Execute code and return the resulting locals dictionary."""

        if not code:
            return {}

        local_vars: Dict[str, Any] = dict(variables or {})
        exec(code, {"__builtins__": SAFE_BUILTINS}, local_vars)
        return local_vars
