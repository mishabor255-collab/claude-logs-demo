# Site down? Let Claude read the logs for you

> 🇷🇺 Русская версия: [README.md](README.md)

A tiny practice project from the video: a small website with a login page that is **broken on purpose**.
You'll learn to stop hunting bugs by hand and let Claude Code do it: it reads the logs, finds the cause
and proposes a fix — you just approve it.

**Time:** 10–15 minutes. **You need:** a computer (macOS, Windows or Linux), Python 3.9+, Claude Code.

---

## Step 0. Requirements

1. **Python 3.9 or newer.** Check in a terminal: `python3 --version` (Windows: `python --version`).
   No Python? Get it from [python.org](https://www.python.org/downloads/).
2. **Claude Code** — Claude that works right in your terminal and can read and edit project files.
   Requires a Claude subscription (Pro or higher) or an Anthropic API key.
   Install it with the official guide: <https://code.claude.com/docs/en/setup>. Check: `claude --version`.

## Step 1. Get the project

```bash
git clone https://github.com/mishabor255-collab/claude-logs-demo.git
cd claude-logs-demo
```
No git? On GitHub click **Code → Download ZIP**, unzip it and open the folder in a terminal.

## Step 2. Run the site and see it fail

```bash
python3 app.py
```
Open <http://localhost:8000>, log in as `demo` / `demo123`.
You'll see a red "**Что-то пошло не так**" ("Something went wrong"). The site is down. 😱

Stop it with **Ctrl + C**.

## Step 3. Ask Claude to find the cause

In the same folder start Claude Code:
```bash
claude
```
and just ask in plain words:
```
The site crashes on login. Find in the logs why login fails, and fix it.
```

What happens:
1. Claude opens `logs/app.log` and sees `KeyError: 'DATABASE_URL'`.
2. It notices the `.env` settings file is missing the `DATABASE_URL` line (which exists in `.env.example`).
3. It proposes adding it and **asks for permission** — read the change and approve it.

> Claude Code always asks before changing files or running commands. Reading what it proposes is a good habit.

## Step 4. Check it

```bash
python3 app.py
```
Log in again with `demo / demo123` — now you'll see a green "**Добро пожаловать, demo!**" ("Welcome, demo!"). 🎉

---

## Why this works and how to use it in your projects

- **Logs are the source of truth.** The error is almost always already written down — it's just hard to read by eye.
- **Give context.** Say *what* broke and *where* to look: "login fails, check logs/app.log".
- **Ask for an explanation first.** "Explain the cause in simple words, don't change anything yet."
- **Verify.** Run the project after the fix.
- **Never commit secrets.** `.env` is in this repo only for the demo. In real projects add `.env` to `.gitignore`
  and commit `.env.example` without real passwords.

### More prompts worth saving
```
Explain in simple words what the last error in the logs means.
Find all errors in logs/ from today and group them by cause.
Make the site show a clear error when a setting is missing instead of crashing.
```

---

## What's next

- More breakdowns like this in our Telegram channel: [@neuromentor_en](https://t.me/neuromentor_en) (Russian: [@neuromentorrr](https://t.me/neuromentorrr))
- Full course on Claude Code, Codex and VS Code — coming soon.

MIT licensed — use it however you like. Not an official Anthropic resource.
