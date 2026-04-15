from flask import Flask, render_template, request, Response, jsonify
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import re
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

BASE_URL = "https://minesec.schoolfaqs.net"
PAPER_BASE = f"{BASE_URL}/paper"

SUBJECT_SLUGS = {
    "computer science": "computer-science",
    "physics": "physics",
    "chemistry": "chemistry",
    "biology": "biology",
    "mathematics": "mathematics",
    "further mathematics": "further-mathematics",
    "geography": "geography",
    "history": "history",
    "economics": "economics",
    "ict": "ict",
}

def extract_pdf(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all(["a", "iframe", "embed"]):
        link = tag.get("src") or tag.get("href")
        if link and ".pdf" in link.lower():
            return urljoin(BASE_URL, link)
    match = re.search(r'["\']([^"\']*?\.pdf[^"\']*?)["\']', html, re.IGNORECASE)
    return urljoin(BASE_URL, match.group(1)) if match else None

@app.route('/health')
def health():
    return 'OK', 200

@app.route('/')
def index():
    try:
        subjects = list(SUBJECT_SLUGS.keys())
        return render_template('index.html', subjects=subjects)
    except Exception as e:
        logging.error(f"Failed to render index: {e}")
        return jsonify({'error': 'Failed to load page'}), 500

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    subj = data.get('subject', '').lower()
    year = data.get('year', '')
    paper = data.get('paper', '')

    slug = SUBJECT_SLUGS.get(subj, subj.replace(" ", "-"))
    candidates = [
        f"{PAPER_BASE}/{slug}-{paper}-{year}",
        f"{PAPER_BASE}/gce-ol-{slug}-{paper}-{year}"
    ]

    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0"})

    for url in candidates:
        try:
            r = session.get(url, timeout=12)
            if r.status_code == 200:
                pdf_url = extract_pdf(r.text)
                if pdf_url:
                    pdf_response = session.get(pdf_url, stream=True)
                    if pdf_response.status_code == 200:
                        filename = f"{slug}_paper{paper}_{year}.pdf"
                        return Response(
                            pdf_response.iter_content(8192),
                            mimetype='application/pdf',
                            headers={
                                'Content-Disposition': f'attachment; filename={filename}'
                            }
                        )
        except:
            continue

    return jsonify({'error': 'Paper not found. Try a different year or paper number.'}), 404

