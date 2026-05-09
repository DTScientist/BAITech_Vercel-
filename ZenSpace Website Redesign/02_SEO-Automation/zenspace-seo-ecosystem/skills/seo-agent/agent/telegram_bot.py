#!/usr/bin/env python3
"""
SEO Agent — Telegram Bot
Sends SEO tasks for approval, handles responses, tracks progress.
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode

from config import load_config, save_config
from tasks import TASKS, get_task_by_id, get_progress_summary

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

STATUS_FILE = Path(__file__).parent / "task_status.json"

# ─── Status Management ───

def load_status():
    if STATUS_FILE.exists():
        return json.loads(STATUS_FILE.read_text())
    return {"completed": [], "rejected": [], "current_index": 0, "started": False, "log": []}


def save_status(status):
    STATUS_FILE.write_text(json.dumps(status, indent=2, default=str))


def log_action(status, action, task_id, note=""):
    status["log"].append({
        "time": datetime.now().isoformat(),
        "action": action,
        "task_id": task_id,
        "note": note,
    })
    save_status(status)


# ─── Message Formatting ───

def format_task_message(task, index, total):
    priority_emoji = {1: "🔴 CRITICAL", 2: "🟠 HIGH", 3: "🟡 MEDIUM"}
    p = priority_emoji.get(task["priority"], "⚪")

    msg = f"━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    msg += f"📋 *Task {index + 1} of {total}*\n"
    msg += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    msg += f"*{task['name']}*\n"
    msg += f"Priority: {p}\n"
    msg += f"Category: {task['category']}\n"
    msg += f"Time: ~{task.get('time_estimate', '5 min')}\n\n"
    msg += f"💡 *Why this matters:*\n{task['plain_explanation']}\n\n"

    # Wix steps
    msg += f"🔧 *How to do it in Wix:*\n"
    for step in task.get("wix_steps", []):
        msg += f"  {step}\n"

    return msg


def format_code_message(task):
    code = task.get("code", "")
    if len(code) > 3500:
        code = code[:3500] + "\n... (truncated — full code sent in next message)"

    msg = f"📝 *Code to paste:*\n\n"
    msg += f"```\n{code}\n```"
    return msg


# ─── Bot Handlers ───

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    config = load_config()
    status = load_status()

    completed = len(status.get("completed", []))
    total = len(TASKS)
    remaining = total - completed - len(status.get("rejected", []))

    msg = f"🤖 *ZenSpace SEO Agent*\n\n"
    msg += f"I have *{total} SEO tasks* ready for your site.\n"
    msg += f"✅ Completed: {completed}\n"
    msg += f"⏳ Remaining: {remaining}\n\n"
    msg += f"Commands:\n"
    msg += f"/next — Send the next task for approval\n"
    msg += f"/progress — See full progress report\n"
    msg += f"/runall — Send all remaining tasks one by one\n"
    msg += f"/reset — Start over from the beginning\n"
    msg += f"/help — Show this message\n\n"
    msg += f"Tap /next to start!"

    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)


async def next_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status = load_status()
    completed = set(status.get("completed", []))
    rejected = set(status.get("rejected", []))

    # Find next uncompleted task
    next_t = None
    next_idx = 0
    for i, task in enumerate(TASKS):
        if task["id"] not in completed and task["id"] not in rejected:
            next_t = task
            next_idx = i
            break

    if not next_t:
        await update.message.reply_text(
            "🎉 *All tasks are done!*\n\n"
            "Use /progress to see the full report.\n"
            "Use /reset to start over.",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    total = len(TASKS)

    # Send task description
    await update.message.reply_text(
        format_task_message(next_t, next_idx, total),
        parse_mode=ParseMode.MARKDOWN,
    )

    # Send code
    await update.message.reply_text(
        format_code_message(next_t),
        parse_mode=ParseMode.MARKDOWN,
    )

    # Send approval buttons
    keyboard = [
        [
            InlineKeyboardButton("✅ Done — I pasted it", callback_data=f"approve:{next_t['id']}"),
            InlineKeyboardButton("⏭ Skip for now", callback_data=f"skip:{next_t['id']}"),
        ],
        [
            InlineKeyboardButton("❌ Reject", callback_data=f"reject:{next_t['id']}"),
            InlineKeyboardButton("📋 Copy code again", callback_data=f"code:{next_t['id']}"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👆 *Did you paste it?* Tap when done:",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN,
    )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action, task_id = query.data.split(":", 1)
    status = load_status()
    task = get_task_by_id(task_id)
    task_name = task["name"] if task else task_id

    if action == "approve":
        if task_id not in status.get("completed", []):
            status.setdefault("completed", []).append(task_id)
            log_action(status, "completed", task_id)

        done = len(status["completed"])
        total = len(TASKS)
        pct = round((done / total) * 100)

        await query.edit_message_text(
            f"✅ *{task_name}* — Done!\n\n"
            f"Progress: {done}/{total} ({pct}%)\n"
            f"{'█' * (pct // 5)}{'░' * (20 - pct // 5)}\n\n"
            f"Send /next for the next task.",
            parse_mode=ParseMode.MARKDOWN,
        )

        # Verification reminder
        if task.get("verify_url"):
            await query.message.reply_text(
                f"🔍 *Verify it works:*\n{task['verify_url']}\n\n"
                f"Open this link after publishing to check Google sees your changes.",
                parse_mode=ParseMode.MARKDOWN,
            )

    elif action == "skip":
        await query.edit_message_text(
            f"⏭ *{task_name}* — Skipped for now.\n"
            f"It'll come back later. Send /next to continue.",
            parse_mode=ParseMode.MARKDOWN,
        )

    elif action == "reject":
        if task_id not in status.get("rejected", []):
            status.setdefault("rejected", []).append(task_id)
            log_action(status, "rejected", task_id)

        await query.edit_message_text(
            f"❌ *{task_name}* — Rejected.\n"
            f"Send /next to continue.",
            parse_mode=ParseMode.MARKDOWN,
        )

    elif action == "code":
        if task:
            await query.message.reply_text(
                format_code_message(task),
                parse_mode=ParseMode.MARKDOWN,
            )


async def progress_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status = load_status()
    completed = set(status.get("completed", []))
    rejected = set(status.get("rejected", []))
    total = len(TASKS)
    done = len(completed)
    rej = len(rejected)
    remaining = total - done - rej
    pct = round((done / total) * 100) if total > 0 else 0

    msg = f"📊 *ZenSpace SEO Progress Report*\n"
    msg += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    msg += f"{'█' * (pct // 5)}{'░' * (20 - pct // 5)} {pct}%\n\n"
    msg += f"✅ Completed: {done}/{total}\n"
    msg += f"❌ Rejected: {rej}\n"
    msg += f"⏳ Remaining: {remaining}\n\n"

    # By category
    categories = {}
    for task in TASKS:
        cat = task["category"]
        categories.setdefault(cat, {"total": 0, "done": 0})
        categories[cat]["total"] += 1
        if task["id"] in completed:
            categories[cat]["done"] += 1

    msg += f"*By Category:*\n"
    for cat, stats in categories.items():
        emoji = "✅" if stats["done"] == stats["total"] else "⏳"
        msg += f"  {emoji} {cat}: {stats['done']}/{stats['total']}\n"

    msg += f"\n*Recent Actions:*\n"
    for entry in status.get("log", [])[-5:]:
        icon = "✅" if entry["action"] == "completed" else "❌"
        t = entry.get("time", "")[:16]
        msg += f"  {icon} {entry['task_id']} ({t})\n"

    msg += f"\nSend /next to continue working."
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)


async def runall_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status = load_status()
    completed = set(status.get("completed", []))
    rejected = set(status.get("rejected", []))

    remaining = [t for t in TASKS if t["id"] not in completed and t["id"] not in rejected]

    if not remaining:
        await update.message.reply_text("🎉 All tasks are already done!")
        return

    await update.message.reply_text(
        f"🚀 Starting batch mode — {len(remaining)} tasks to go.\n"
        f"I'll send them one at a time. Approve each one when you've pasted it.\n\n"
        f"First task coming up...",
        parse_mode=ParseMode.MARKDOWN,
    )

    # Send first task
    await next_task(update, context)


async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_status({"completed": [], "rejected": [], "current_index": 0, "started": False, "log": []})
    await update.message.reply_text(
        "🔄 *Reset complete!*\nAll progress cleared. Send /next to start fresh.",
        parse_mode=ParseMode.MARKDOWN,
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_command(update, context)


# ─── Main ───

def run_bot():
    config = load_config()
    token = config.get("telegram_token")

    if not token:
        print("ERROR: No Telegram token configured. Run setup.py first.")
        print("See SETUP.md for instructions.")
        return

    print(f"\n{'='*50}")
    print(f"  ZenSpace SEO Agent — Telegram Bot")
    print(f"{'='*50}")
    print(f"  Domain: {config.get('domain')}")
    print(f"  Tasks: {len(TASKS)}")
    print(f"  Bot starting...")
    print(f"{'='*50}\n")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("next", next_task))
    app.add_handler(CommandHandler("progress", progress_command))
    app.add_handler(CommandHandler("runall", runall_command))
    app.add_handler(CommandHandler("reset", reset_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_callback))

    print("✓ Bot is running! Open Telegram and send /start to your bot.\n")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    run_bot()
