from __future__ import annotations

import csv
import os
from datetime import datetime

FILE = os.path.join("data", "leads.csv")


def save_lead(name: str, message: str, intent: str, client_type: str) -> None:
    os.makedirs(os.path.dirname(FILE) or ".", exist_ok=True)
    file_exists = os.path.isfile(FILE)

    with open(FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Name", "Message", "Intent", "Client Type"])
        writer.writerow([datetime.now().isoformat(timespec="seconds"), name, message, intent, client_type])

