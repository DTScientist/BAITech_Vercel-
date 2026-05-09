"""
ZenSpace Reports — Google Drive Uploader (Apps Script)
=======================================================
Uploads a CSV to Google Drive via a Google Apps Script web app.
No OAuth, no service accounts, no Python libraries needed beyond 'requests'.

Usage:
    python upload_to_drive.py <csv_file_path>

Returns the shareable Drive link via stdout (parsed by scheduled task).
"""

import sys
import json
import pathlib
import requests

APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxAsem7_0CLRXmnCfN6M92w4HNLTq8NJ2dho_cDG5stP7rSvGurZxy1C3-13jIgPBSo/exec"


def upload_csv(csv_path: str) -> dict:
    csv_content = pathlib.Path(csv_path).read_text(encoding="utf-8")
    file_name   = pathlib.Path(csv_path).name

    response = requests.post(
        APPS_SCRIPT_URL,
        json={"csv": csv_content, "filename": file_name},
        timeout=30
    )
    response.raise_for_status()
    result = response.json()

    if not result.get("success"):
        raise RuntimeError(f"Apps Script error: {result.get('error')}")

    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python upload_to_drive.py <csv_file_path>")
        sys.exit(1)

    csv_path = sys.argv[1]
    print(f"📤 Uploading: {pathlib.Path(csv_path).name}")

    try:
        result = upload_csv(csv_path)
        print(f"✅ Uploaded successfully!")
        print(f"📄 File: {pathlib.Path(csv_path).name}")
        print(f"🔗 Shareable link: {result['link']}")
        print(f"📁 Folder: {result['folderLink']}")
        print(f"\n__RESULT_JSON__:{json.dumps(result)}")
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
