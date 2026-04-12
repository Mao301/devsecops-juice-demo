import requests
import os
import time
import sys

# =========================
# CONFIG
# =========================
API_KEY = os.getenv("HEYHACK_API_KEY")
APPLICATION_ID = os.getenv("APPLICATION_ID")

THRESHOLD = float(os.getenv("CVSS_THRESHOLD", 11))
INTERVAL = int(os.getenv("CHECK_INTERVAL", 30))

BASE_URL = "https://app.heyhack.com/api/findings"

HEADERS = {
    "accept": "*/*",
    "Authorization": API_KEY
}

# =========================
# VALIDATION
# =========================
if not API_KEY or not APPLICATION_ID:
    print("❌ Missing required environment variables")
    sys.exit(1)

print(f"🔍 Monitoring Heyhack findings")
print(f"   - Application: {APPLICATION_ID}")
print(f"   - Threshold CVSS >= {THRESHOLD}")
print(f"   - Interval: {INTERVAL}s\n")

# =========================
# MAIN LOOP
# =========================
while True:
    try:
        url = f"{BASE_URL}?application_id={APPLICATION_ID}&accepted=false&cvss_score={THRESHOLD}"

        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            print("⚠️ Error fetching findings")
            print(response.status_code, response.text)
            time.sleep(INTERVAL)
            continue

        findings = response.json()

        print(f"📊 Findings >= {THRESHOLD}: {len(findings)}")

        if len(findings) > 0:
            print("\n❌ Critical vulnerabilities detected!\n")

            for f in findings:
                print(f" - {f.get('vulnerabilityTitle')} | CVSS {f.get('cvssScore')}")

            print("\n🚨 Failing pipeline due to security threshold breach")
            sys.exit(1)

        print("✅ No critical findings yet\n")

    except Exception as e:
        print(f"⚠️ Exception during monitoring: {e}")

    time.sleep(INTERVAL)