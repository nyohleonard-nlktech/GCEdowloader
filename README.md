# GCE Downloader

A Flask web application for locating and downloading examination-paper PDFs from the configured SchoolFAQs source website.

## Features
- Flask subject-selection interface.
- Subject-to-source-slug mapping.
- Candidate paper URL generation from subject, paper number, and year.
- PDF URL extraction from HTML anchors, iframes, and embeds.
- Streamed PDF response with a generated filename.
- Health endpoint.

## Stack
Python, Flask, Requests, BeautifulSoup, Gunicorn.

## Requirements
Python 3.9+, pip, and network access to the configured upstream source.

## Setup
```bash
git clone https://github.com/nyohleonard-nlktech/GCEdowloader.git
cd GCEdowloader
python -m venv .venv
```

Activate:
```bash
# macOS / Linux
source .venv/bin/activate
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Install and run:
```bash
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000.

## HTTP routes

| Method | Route | Purpose |
|---|---|---|
| GET | / | Render subject selection page |
| GET | /health | Health check |
| POST | /download | Locate and stream a paper PDF |

Example JSON request to POST /download:
```json
{
  "subject": "Computer Science",
  "year": "2024",
  "paper": "1"
}
```

## Structure
```text
app.py
requirements.txt
templates/
.github/
```

The upstream site's URL conventions and markup may change. Respect its terms, copyright, and access rules; only download or redistribute materials where permitted. Add input validation, request timeouts for PDF downloads, and rate limiting before public deployment.

No license file is present; all rights reserved unless an explicit license is added.
