"""CSV export helper."""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Dict, Any, List


@dataclass
class CSVExportTool:
    """Persist structured data to CSV files."""

    output_dir: str = "./data/exports"

    def __post_init__(self) -> None:
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

    def export(self, filename: str, rows: Iterable[Dict[str, Any]]) -> str:
        """Write rows to a CSV and return the path."""

        rows = list(rows)
        if not rows:
            raise ValueError("No rows supplied for export")

        fieldnames: List[str] = sorted({key for row in rows for key in row})
        output_path = Path(self.output_dir) / filename

        with output_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)

        return str(output_path)
