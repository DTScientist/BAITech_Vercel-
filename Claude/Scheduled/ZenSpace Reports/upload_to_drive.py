"""
ZenSpace Reports — Google Drive Uploader (OAuth2)
==================================================
Uploads a CSV to Google Drive using OAuth2 (your personal Google account).
On first run, opens a browser for one-time authorization. Token is saved
locally so all future runs are fully automatic — no browser needed again.

Usage:
    python upload_to_drive.py <csv_file_path>

Setup (one-time):
    1. Go to console.cloud.google.com → your project
    2. APIs & Services → Credentials → Create Credentials → OAuth 2.0 Client ID
    3. Application type: Desktop app → name it "ZenSpace Uploader" → Create
    4. Download the JSON → rename it to: oauth_client.json
    5. Place oauth_client.json in the same folder as this script
    6. Run this script once — a browser will open → sign in → approve access
    7. Token is saved as drive_token.json → all future runs are automatic

Requirements:
    pip install google-api-python-client google-auth google-auth-oauthlib
"""

import sys
import os
import json
from pathlib import Path

# ── CONFIG ────────────────────────────────────────────────────────────────────
DRIVE_FOLDER_ID  = "1bY2f0dHRzQqOtFIRlbWy6BIflqhzIoAn"
SCRIPT_DIR       = Path(__file__).parent
CLIENT_FILE      = SCRIPT_DIR / "oauth_client.json"
TOKEN_FILE       = SCRIPT_DIR / "drive_token.json"
SCOPES           = ["https://www.googleapis.com/auth/drive.file"]
# ──────────────────────────────────────────────────────────────────────────────


def get_drive_service():
    """Authenticate using OAuth2. Opens browser on first run, uses saved token after."""
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    creds = None

    # Load saved token if it exists
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    # If no valid token, do the OAuth flow (opens browser once)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CLIENT_FILE.exists():
                raise FileNotFoundError(
                    f"\n❌ oauth_client.json not found at: {CLIENT_FILE}\n\n"
                    "One-time setup:\n"
                    "  1. Go to console.cloud.google.com → your project\n"
                    "  2. APIs & Services → Credentials → Create Credentials → OAuth 2.0 Client ID\n"
                    "  3. Application type: Desktop app → name: ZenSpace Uploader → Create\n"
                    "  4. Download JSON → rename to oauth_client.json\n"
                    f"  5. Place it here: {CLIENT_FILE}\n"
                    "  6. Run this script again — browser will open for one-time approval\n"
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_FILE), SCOPES)
            creds = flow.run_local_server(port=0)

        # Save token for future runs
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
        print(f"✅ Token saved to {TOKEN_FILE} — future runs won't need browser")

    return build("drive", "v3", credentials=creds, cache_discovery=False)


def upload_csv(csv_path: str) -> dict:
    """Upload CSV to Google Drive folder. Updates file if it already exists."""
    from googleapiclient.http import MediaFileUpload

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    service  = get_drive_service()
    file_name = Path(csv_path).name

    # Check if file already exists (avoid duplicates)
    existing = service.files().list(
        q=f"name='{file_name}' and '{DRIVE_FOLDER_ID}' in parents and trashed=false",
        fields="files(id, name)"
    ).execute()

    media = MediaFileUpload(csv_path, mimetype="text/csv", resumable=False)

    if existing.get("files"):
        file_id = existing["files"][0]["id"]
        service.files().update(
            fileId=file_id,
            media_body=media,
            fields="id, name, webViewLink"
        ).execute()
        action = "updated"
    else:
        meta = {"name": file_name, "parents": [DRIVE_FOLDER_ID]}
        result = service.files().create(
            body=meta, media_body=media, fields="id, name, webViewLink"
        ).execute()
        file_id = result["id"]
        action = "uploaded"

    # Make shareable (anyone with link can view)
    service.permissions().create(
        fileId=file_id,
        body={"type": "anyone", "role": "reader"},
    ).execute()

    shareable_link = f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"
    folder_link    = f"https://drive.google.com/drive/folders/{DRIVE_FOLDER_ID}"

    return {
        "file_id":       file_id,
        "file_name":     file_name,
        "shareable_link": shareable_link,
        "folder_link":   folder_link,
        "action":        action,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python upload_to_drive.py <csv_file_path>")
        sys.exit(1)

    csv_path = sys.argv[1]
    print(f"📤 Uploading: {Path(csv_path).name}")

    try:
        result = upload_csv(csv_path)
        print(f"✅ {result['action'].capitalize()} successfully!")
        print(f"📄 File: {result['file_name']}")
        print(f"🔗 Shareable link: {result['shareable_link']}")
        print(f"📁 Folder: {result['folder_link']}")
        # JSON output for the scheduled task to parse
        print(f"\n__RESULT_JSON__:{json.dumps(result)}")
    except FileNotFoundError as e:
        print(str(e))
        sys.exit(1)
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
