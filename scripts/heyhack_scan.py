import requests
import os
import sys
from dotenv import load_dotenv

load_dotenv()

def main():
    heyhack_api_key = os.getenv("HEYHACK_API_KEY")

    if not heyhack_api_key:
        print("❌ Missing HEYHACK_API_KEY")
        sys.exit(1)

    heyhack_url = "https://app.heyhack.com/api/scanjobs"
    profile_id = "9066c97f-d8e6-4c08-b48a-5bb96814f70a"
    application_id = "ff836b6a-5628-467d-8b2e-925c149fa4d6"

    params = {
        "profile_id": profile_id,
        "application_id": application_id
    }

    headers = {
        "accept": "*/*",
        "Authorization": f"Heyhack {heyhack_api_key}"
    }

    response = requests.post(heyhack_url, headers=headers, params=params)

    if response.status_code == 200:
        print("✅ Scan initiated successfully")
        print(response.json())
    else:
        print(f"❌ Error initiating scan: {response.status_code}")
        print(response.text)
        sys.exit(1)

if __name__ == "__main__":
    main()