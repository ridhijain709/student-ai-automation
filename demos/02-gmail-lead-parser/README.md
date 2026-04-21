# Gmail Lead Parser + Sheet Logger

## Problem
CA firms receive client queries via email daily.
Staff manually reads, classifies, and logs each one — slow and error-prone.

## Solution
Python script using Gmail API + Gemini: reads incoming emails → extracts client name, query type, urgency → auto-logs to Google Sheet → flags urgent items.

## Tools Used
- Gmail API (Google Cloud, free tier)
- Google Gemini API (gemini-1.5-flash)
- Google Sheets API
- Python 3.10

## What It Does
1. Reads last 10 unread emails from inbox
2. Sends each to Gemini with prompt: "Extract: sender name, query type, urgency (High/Medium/Low)"
3. Writes structured row to Google Sheet
4. Marks email as read

## Business Impact
- Eliminates manual email logging
- Urgent queries flagged within seconds
- Builds searchable client query database automatically

## Status
Core script functional. Integration demo available on request.
