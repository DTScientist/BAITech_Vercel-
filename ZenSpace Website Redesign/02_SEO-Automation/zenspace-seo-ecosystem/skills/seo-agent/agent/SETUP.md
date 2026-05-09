# SEO Agent — Telegram Setup Guide (2 minutes)

## Step 1: Create Your Telegram Bot

1. Open Telegram on your phone
2. Search for **@BotFather** (the official Telegram bot creator)
3. Send: `/newbot`
4. BotFather will ask for a name. Type: `ZenSpace SEO Agent`
5. BotFather will ask for a username. Type: `zenspace_seo_bot` (or any unique name ending in `bot`)
6. BotFather will give you a **token** like: `7123456789:AAF1234567890abcdef...`
7. **Copy this token** — you'll need it in Step 3

## Step 2: Get Your Chat ID

1. Start a conversation with your new bot (search for it and click "Start")
2. Send it any message (like "hello")
3. Open this URL in your browser (replace YOUR_TOKEN with the token from Step 1):
   ```
   https://api.telegram.org/botYOUR_TOKEN/getUpdates
   ```
4. Find the `"chat":{"id":123456789}` in the response
5. **Copy this chat ID number**

## Step 3: Configure the Agent

Run this command, replacing the values:
```bash
python3 /home/claude/skills/seo-agent/agent/setup.py \
  --token "YOUR_BOT_TOKEN" \
  --chat-id YOUR_CHAT_ID \
  --domain "zenspaceevents.com"
```

## Step 4: Launch the Agent

```bash
python3 /home/claude/skills/seo-agent/agent/agent.py
```

The agent will:
1. Send you a welcome message on Telegram
2. Start sending SEO tasks one by one
3. Each task has: what it does, why it matters, the exact code, and Approve/Reject buttons
4. When you approve, it either auto-executes or sends you step-by-step Wix instructions
5. Tracks everything and sends daily progress reports

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────┐
│  SEO Agent       │────▶│  Telegram     │────▶│  You (phone) │
│  (runs on server)│◀────│  Bot API      │◀────│  Approve/    │
│                  │     │               │     │  Reject      │
│  • Audits site   │     │  • Sends task │     │              │
│  • Generates fix │     │  • Shows code │     │  • Tap button│
│  • Tracks status │     │  • Gets vote  │     │  • See code  │
│  • Verifies fix  │     │  • Reports    │     │  • Copy paste│
└─────────────────┘     └──────────────┘     └─────────────┘
```
