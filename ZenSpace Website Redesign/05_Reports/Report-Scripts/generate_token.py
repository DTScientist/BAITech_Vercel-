"""
ZenSpace — Google Drive Token Generator (run this ONCE on your computer)
=========================================================================
This script opens your browser, asks you to sign into Google and approve
Drive access, then saves drive_token.json. After that, all automated
uploads work silently with no browser prompts ever again.

HOW TO RUN (on your Windows machine):
    1. Open Command Prompt or PowerShell in this folder
    2. Run: pip install google-auth-oauthlib google-api-python-client
    3. Run: python generate_token.py
    4. Browser opens → sign in → click Allow
    5. Done! drive_token.json is saved in this folder.
"""

from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES      = ["https://www.googleapis.com/auth/drive.file"]
SCRIPT_DIR  = Path(__file__).parent
CLIENT_FILE = SCRIPT_DIR / "oauth_client.json"
TOKEN_FILE  = SCRIPT_DIR / "drive_token.json"

if not CLIENT_FILE.exists():
    print(f"❌ oauth_client.json not found at: {CLIENT_FILE}")
    print("Download it from Google Cloud Console → APIs & Services → Credentials")
    exit(1)

print("🌐 Opening browser for Google sign-in...")
print("   Sign in and click Allow — this only happens once.\n")

flow  = InstalledAppFlow.from_client_secrets_file(str(CLIENT_FILE), SCOPES)
creds = flow.run_local_server(port=0)

with open(TOKEN_FILE, "w") as f:
    f.write(creds.to_json())

print(f"\n✅ Success! Token saved to: {TOKEN_FILE}")
print("   All future automated uploads will work silently — no browser needed.")
