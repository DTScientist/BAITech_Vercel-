#!/usr/bin/env python3
"""
SEO Agent — Main Entry Point
Orchestrates: Audit → Task Generation → Telegram Approval → Execution → Verification

Usage:
  python3 agent.py --mode bot        # Run persistent Telegram bot (recommended)
  python3 agent.py --mode push       # Push all tasks to Telegram at once
  python3 agent.py --mode status     # Check current progress
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config import load_config
from tasks import TASKS, get_progress_summary
from telegram_bot import run_bot


async def push_all_tasks():
    """Push all pending tasks to Telegram in one batch."""
    from telegram import Bot
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup

    config = load_config()
    token = config.get("telegram_token")
    chat_id = config.get("telegram_chat_id")

    if not token or not chat_id:
        print("ERROR: Run setup.py first.")
        return

    bot = Bot(token=token)
    status_file = Path(__file__).parent / "task_status.json"
    status = json.loads(status_file.read_text()) if status_file.exists() else {"completed": [], "rejected": []}
    completed = set(status.get("completed", []))
    rejected = set(status.get("rejected", []))

    remaining = [t for t in TASKS if t["id"] not in completed and t["id"] not in rejected]

    if not remaining:
        await bot.send_message(chat_id=chat_id, text="🎉 All SEO tasks are complete!")
        return

    # Send summary
    total = len(TASKS)
    done = len(completed)
    msg = (
        f"🤖 *ZenSpace SEO Agent — Task Batch*\n\n"
        f"Sending {len(remaining)} tasks for your review.\n"
        f"Already completed: {done}/{total}\n\n"
        f"For each task, you'll see:\n"
        f"• What it does (plain English)\n"
        f"• The exact code to paste\n"
        f"• Where to paste it in Wix\n"
        f"• Approve/Skip/Reject buttons\n\n"
        f"Let's go! 👇"
    )
    await bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
    await asyncio.sleep(1)

    # Send each task
    for i, task in enumerate(remaining):
        priority_emoji = {1: "🔴", 2: "🟠", 3: "🟡"}
        p = priority_emoji.get(task["priority"], "⚪")

        # Task description
        desc = (
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📋 *Task {done + i + 1} of {total}*\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"*{task['name']}*\n"
            f"{p} Priority: {task['priority']} | ⏱ {task.get('time_estimate', '5 min')}\n\n"
            f"💡 {task['plain_explanation']}\n\n"
            f"🔧 *Wix Steps:*\n"
        )
        for step in task.get("wix_steps", []):
            desc += f"  {step}\n"

        await bot.send_message(chat_id=chat_id, text=desc, parse_mode="Markdown")

        # Code
        code = task.get("code", "")
        if len(code) > 4000:
            code = code[:4000] + "\n..."
        await bot.send_message(chat_id=chat_id, text=f"```\n{code}\n```", parse_mode="Markdown")

        # Buttons
        keyboard = [
            [
                InlineKeyboardButton("✅ Done", callback_data=f"approve:{task['id']}"),
                InlineKeyboardButton("⏭ Skip", callback_data=f"skip:{task['id']}"),
                InlineKeyboardButton("❌ Reject", callback_data=f"reject:{task['id']}"),
            ]
        ]
        await bot.send_message(
            chat_id=chat_id,
            text="👆 Tap when done:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

        await asyncio.sleep(0.5)  # Avoid rate limits

    await bot.send_message(
        chat_id=chat_id,
        text=(
            f"📦 *All {len(remaining)} tasks sent!*\n\n"
            f"Work through them at your own pace.\n"
            f"Tap ✅ Done on each one after you paste it.\n"
            f"Use /progress to check your status anytime."
        ),
        parse_mode="Markdown",
    )


def show_status():
    """Show current progress."""
    status_file = Path(__file__).parent / "task_status.json"
    status = json.loads(status_file.read_text()) if status_file.exists() else {"completed": [], "rejected": []}

    completed = status.get("completed", [])
    rejected = status.get("rejected", [])
    total = len(TASKS)
    done = len(completed)
    rej = len(rejected)
    remaining = total - done - rej
    pct = round((done / total) * 100) if total > 0 else 0

    print(f"\n{'='*50}")
    print(f"  ZenSpace SEO Agent — Status")
    print(f"{'='*50}")
    print(f"  {'█' * (pct // 5)}{'░' * (20 - pct // 5)} {pct}%")
    print(f"  ✅ Completed: {done}/{total}")
    print(f"  ❌ Rejected: {rej}")
    print(f"  ⏳ Remaining: {remaining}")
    print(f"{'='*50}")

    if completed:
        print(f"\n  Completed tasks:")
        for tid in completed:
            task = next((t for t in TASKS if t["id"] == tid), None)
            if task:
                print(f"    ✅ {task['name']}")

    remaining_tasks = [t for t in TASKS if t["id"] not in completed and t["id"] not in rejected]
    if remaining_tasks:
        print(f"\n  Next up:")
        for t in remaining_tasks[:5]:
            p = {1: "🔴", 2: "🟠", 3: "🟡"}.get(t["priority"], "⚪")
            print(f"    {p} {t['name']}")
        if len(remaining_tasks) > 5:
            print(f"    ... and {len(remaining_tasks) - 5} more")

    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ZenSpace SEO Agent")
    parser.add_argument("--mode", choices=["bot", "push", "status"], default="bot",
                        help="bot=persistent bot, push=send all tasks, status=check progress")
    args = parser.parse_args()

    if args.mode == "bot":
        run_bot()
    elif args.mode == "push":
        asyncio.run(push_all_tasks())
    elif args.mode == "status":
        show_status()
