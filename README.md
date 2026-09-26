
   <div align="center">
     <h1>📸 Discord Screenshot Bot</h1>
     <p><i>A Python (discord.py) Discord bot that creates embedded "screenshots" of messages in a specified channel once the original message reaches a set number of reactions. Features include customizable color, time zone, emoji, and reaction threshold, as well as slash command support.</i></p>
   </div>
   

## What is it?

A Python Discord bot, named "Mikhail Andreevich", inspired by the "Miss Whimsical Wobin" bot from the NTTS server.

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)

Mikhail creates "screenshots" of messages in a dedicated channel once the original message reaches a specified number of reactions.

### ✨ Features
- customizable reaction emoji;
- configurable reaction threshold;
- customizable embed color;
- timezone-aware timestamp display;
- slash commands.

### 🚀 Quick Start
- Create a bot at [this site](https://discord.com/api), grant it all the necessary requested permissions, and generate a token.
- Insert the token into the .env file, filling in the blank space in the "DISCORD_BOT_TOKEN=" line.
- Launch the bot using the screenshot_bot.py file in any way you prefer.

Also check out requirements.txt and install all needed packages.

## 🧩 Demo

Let's put on requirements skull emoji and 1 reaction threshold ->

Then write message:

<img width="506" height="461" alt="image" src="https://github.com/user-attachments/assets/1e51b5c7-388a-4bda-9ff4-13526aca8927" />

Now, bot makes screenshot using HTML ->

<img width="549" height="413" alt="image" src="https://github.com/user-attachments/assets/fc733227-cf12-4a4b-bc88-6bdc1ad5e13d" />

Preseving top role color, avatar decoration and attachment files as well
