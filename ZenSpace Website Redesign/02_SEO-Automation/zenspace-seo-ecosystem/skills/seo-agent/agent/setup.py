#!/usr/bin/env python3
"""SEO Agent — Quick Setup"""

import argparse
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from config import setup

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SEO Agent Setup")
    parser.add_argument("--token", required=True, help="Telegram Bot Token from @BotFather")
    parser.add_argument("--chat-id", required=True, help="Your Telegram Chat ID")
    parser.add_argument("--domain", default="zenspaceevents.com", help="Your domain")
    args = parser.parse_args()

    config = setup(args.token, args.chat_id, args.domain)
    print(f"\n✅ Setup complete!")
    print(f"   Domain: {config['domain']}")
    print(f"   Bot Token: {config['telegram_token'][:10]}...")
    print(f"   Chat ID: {config['telegram_chat_id']}")
    print(f"\n   Now run: python3 agent/telegram_bot.py")
