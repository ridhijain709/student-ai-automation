from __future__ import annotations

import csv
import os
from datetime import datetime


def _ensure_data_dir() -> None:
    os.makedirs("data", exist_ok=True)


def save_lead(name: str, message: str) -> None:
    _ensure_data_dir()
    path = os.path.join("data", "leads.csv")
    file_exists = os.path.exists(path)

    with open(path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["created_at", "name", "message"])
        writer.writerow([datetime.now().isoformat(), name, message])

