#!/usr/bin/env python3
"""SEO Agent — Configuration"""

import json
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "config.json"

DEFAULT_CONFIG = {
    "telegram_token": "",
    "telegram_chat_id": "",
    "domain": "zenspaceevents.com",
    "site_url": "https://www.zenspaceevents.com",
    "company_name": "ZenSpace Event Solutions",
    "email": "info@zenspace.io",
    "tasks_completed": [],
    "tasks_rejected": [],
    "tasks_pending": [],
    "current_task_index": 0,
    "agent_started": False,
}


def load_config():
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text())
    return DEFAULT_CONFIG.copy()


def save_config(config):
    CONFIG_PATH.write_text(json.dumps(config, indent=2))


def setup(token, chat_id, domain="zenspaceevents.com"):
    config = load_config()
    config["telegram_token"] = token
    config["telegram_chat_id"] = str(chat_id)
    config["domain"] = domain
    config["site_url"] = f"https://www.{domain}"
    save_config(config)
    print(f"✓ Config saved: {CONFIG_PATH}")
    return config
