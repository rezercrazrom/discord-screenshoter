# Screenshot-Bot
A Python (discord.py) Discord bot that creates embedded "screenshots" of messages in a specified channel once the original message reaches a set number of reactions. Features include customizable color, time zone, emoji, and reaction threshold, as well as slash command support.

## Mikhail Andreevich

A Python Discord bot inspired by the "Miss Whimsical Wobin" bot from the NTTS server.

### What it does
Creates "screenshots" of messages in a dedicated channel once the original message reaches a specified number of reactions.

### Features
- customizable reaction emoji;
- configurable reaction threshold;
- customizable embed color;
- timezone-aware timestamp display;
- slash commands.

### For proper operation:
- Create a bot at [this site](https://discord.com/api), grant it all the necessary requested permissions, and generate a token.
- Insert the token into the .env file, filling in the blank space in the "DISCORD_BOT_TOKEN=" line.
- Launch the bot using the screenshot_bot.py file in any way you prefer.
