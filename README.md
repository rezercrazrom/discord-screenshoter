<div align="center">

# Discord Screenshoter

**A Discord bot that turns messages into clean screenshots — just add a reaction.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![discord.py](https://img.shields.io/badge/discord.py-2.x-5865F2?logo=discord&logoColor=white)](https://github.com/Rapptz/discord.py)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-brightgreen)]()

[Demo](#demo) • [Features](#features) • [Quick Start](#quick-start) • [Project Structure](#project-structure)

</div>

---

## ❓ What is it?

**Discord Screenshoter** is a Python-based Discord bot that creates clean, shareable screenshots of messages when users react to them. It renders the message through HTML/CSS, crops it intelligently, and sends the result back to the channel.

It was inspired by **Miss Whimsical Wobin** on the **NTTS** Discord server — and built as a pet project to make message sharing outside Discord easier and prettier.

---

## Demo

| Step | Preview |
|------|---------|
| 1. Add a reaction to a message | <img width="506" height="461" alt="image" src="https://github.com/user-attachments/assets/1e51b5c7-388a-4bda-9ff4-13526aca8927" /> |
| 2. Bot processes the message | <img width="947" height="181" alt="image" src="https://github.com/user-attachments/assets/1adb7d37-aba7-485f-98f8-7e353e5260e5" /> |
| 3. Screenshot is sent back | <img width="549" height="413" alt="image" src="https://github.com/user-attachments/assets/fc733227-cf12-4a4b-bc88-6bdc1ad5e13d" /> |

---

## Features

| Feature | Description |
|---------|-------------|
| 🎯 **Reaction trigger** | Add a specific reaction to any message and the bot creates a screenshot. |
| 🖼️ **HTML rendering** | Messages are rendered via HTML/CSS for a pixel-perfect Discord-like look. |
| ✂️ **Smart cropping** | Automatically crops empty space while preserving message context. |
| 🧵 **Context preservation** | Keeps replies, attachments, embeds, and custom emojis intact. |
| ⚡ **Fast & lightweight** | Built on `discord.py` with minimal dependencies. |

---

## Quick Start

<details>
<summary><strong>Click to expand setup instructions</strong></summary>

### Prerequisites

- Python 3.10+
- A Discord bot token
- Basic permissions: Read Messages, Send Messages, Add Reactions, Attach Files, Read Message History

### 1. Clone the repository

```bash
git clone https://github.com/rezercrazrom/discord-screenshoter.git
cd discord-screenshoter
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment
Create a .env file in the project root:

```env
DISCORD_TOKEN=your_token_here
```
### 4. Run the bot

```bash
python screenshot_bot.py
```

### 5. Invite the bot

Use the OAuth2 URL from the Discord Developer Portal with the permissions listed above.

</details>

## Project Structure

```text
discord-screenshoter/
├── screenshot_bot.py      # Main bot logic and event handlers
├── screenshot_bot_db.py   # Database maker system
├── html_constructor.py    # Builds HTML/CSS for message rendering
├── smart_crop.py          # Crops rendered images intelligently
├── commands_app.py        # Add Discord slash-commands suooirt
├── requirements.txt
├── .env
└── LICENSE
```

## Acknowledgements

Inspired by Miss Whimsical Wobin on the NTTS Discord server.

Built with discord.py.
