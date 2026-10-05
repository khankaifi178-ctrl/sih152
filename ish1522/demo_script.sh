#!/bin/bash
set -e

echo "=================================================================="
echo "  SOCIAL LENS (NTRO) — MASTER DEMO & VERIFICATION SCRIPT"
echo "=================================================================="

echo "[1/4] Generating synthetic dataset (125,000+ posts, 38,000+ users)..."
python3 data/sample/generate_sample.py

echo "[2/4] Running full automated test suite (42 test cases)..."
python3 tests/test_suite.py

echo "[3/4] Verifying API Client endpoints & responses..."
python3 -c "
from backend.api_client import APIClient
client = APIClient()
_, summary = client.get_summary()
_, trends = client.get_trends()
print('API Verification: Total Posts =', summary['total_posts_formatted'], '| Top Trend =', trends['trends'][0]['topic'])
"

echo "[4/4] Social Lens AI Analytics Framework is ready!"
echo "Dashboard UI: Open frontend/index.html or start backend with 'python3 backend/main.py 8000'"
echo "=================================================================="
