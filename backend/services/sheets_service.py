from __future__ import annotations

import csv
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from backend.config import settings


@dataclass
class SheetsAppendResult:
    mode: str
    ok: bool
    detail: str


def _ensure_parent_dir(path: str) -> None:
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)


def append_lead_row(
    *,
    lead_id: int,
    name: Optional[str],
    phone: Optional[str],
    email: Optional[str],
    source: str,
    message: Optional[str],
    tags: Optional[str],
    created_at: datetime,
) -> SheetsAppendResult:
    """
    Demo-friendly Sheets integration.

    - SHEETS_MODE=mock (default): appends to ./data/sheets_mock.csv
    - SHEETS_MODE=google: appends to a real Google Sheet (requires credentials/env)
    """
    mode = (settings.SHEETS_MODE or "mock").lower().strip()
    if mode == "google":
        return _append_google_sheet(
            lead_id=lead_id,
            name=name,
            phone=phone,
            email=email,
            source=source,
            message=message,
            tags=tags,
            created_at=created_at,
        )
    return _append_mock_csv(
        lead_id=lead_id,
        name=name,
        phone=phone,
        email=email,
        source=source,
        message=message,
        tags=tags,
        created_at=created_at,
    )


def _append_mock_csv(
    *,
    lead_id: int,
    name: Optional[str],
    phone: Optional[str],
    email: Optional[str],
    source: str,
    message: Optional[str],
    tags: Optional[str],
    created_at: datetime,
) -> SheetsAppendResult:
    path = os.path.join("data", "sheets_mock.csv")
    _ensure_parent_dir(path)
    file_exists = os.path.exists(path)

    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(
                [
                    "lead_id",
                    "created_at",
                    "name",
                    "phone",
                    "email",
                    "source",
                    "message",
                    "tags",
                ]
            )
        writer.writerow(
            [
                lead_id,
                created_at.isoformat(),
                name or "",
                phone or "",
                email or "",
                source,
                message or "",
                tags or "",
            ]
        )

    return SheetsAppendResult(mode="mock", ok=True, detail=f"Appended to {path}")


def _append_google_sheet(
    *,
    lead_id: int,
    name: Optional[str],
    phone: Optional[str],
    email: Optional[str],
    source: str,
    message: Optional[str],
    tags: Optional[str],
    created_at: datetime,
) -> SheetsAppendResult:
    if not settings.GOOGLE_SHEETS_SPREADSHEET_ID:
        return SheetsAppendResult(mode="google", ok=False, detail="Missing GOOGLE_SHEETS_SPREADSHEET_ID")
    if not settings.GOOGLE_SERVICE_ACCOUNT_FILE:
        return SheetsAppendResult(mode="google", ok=False, detail="Missing GOOGLE_SERVICE_ACCOUNT_FILE")

    try:
        # Lazy import so local demo doesn't require Google deps unless used.
        from google.oauth2.service_account import Credentials
        from googleapiclient.discovery import build

        creds = Credentials.from_service_account_file(
            settings.GOOGLE_SERVICE_ACCOUNT_FILE,
            scopes=["https://www.googleapis.com/auth/spreadsheets"],
        )
        service = build("sheets", "v4", credentials=creds)

        sheet_name = settings.GOOGLE_SHEETS_SHEET_NAME or "Leads"
        range_name = f"{sheet_name}!A:H"
        values = [
            [
                lead_id,
                created_at.isoformat(),
                name or "",
                phone or "",
                email or "",
                source,
                message or "",
                tags or "",
            ]
        ]

        service.spreadsheets().values().append(
            spreadsheetId=settings.GOOGLE_SHEETS_SPREADSHEET_ID,
            range=range_name,
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body={"values": values},
        ).execute()

        return SheetsAppendResult(mode="google", ok=True, detail="Appended to Google Sheet")
    except Exception as e:
        return SheetsAppendResult(mode="google", ok=False, detail=f"Google Sheets append failed: {e}")

