import datetime
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from screenshot_bot_db import db

load_dotenv()

intents = discord.Intents.default()
intents.messages = True
intents.reactions = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

import commands_app


@bot.event
async def on_reaction_add(reaction, user):
    config = db.get_config(reaction.message.guild.id)

    if str(reaction.emoji) == config['emoji'] and reaction.count >= config['threshold']:
        message = reaction.message

        if getattr(message, 'processed', False):
            return

        screenshot_channel = bot.get_channel(config['channel'])
        if not screenshot_channel:
            return

        try:
            from html_constructor import take_screenshot
            screenshot = await take_screenshot(message)
        except Exception as e:
            print(f"Ошибка создания скриншота: {e}")
            return

        file = discord.File(screenshot, filename=f"screenshot_{message.id}.png")

        embed = discord.Embed(
            title=f"{message.author} ({message.author.id})",
            color=discord.Color(int(config['color'], 16) if config['color'] else 0x00FF00),
            timestamp=datetime.datetime.now()
        )

        embed.add_field(name="Автор", value=f"<@{message.author.id}>", inline=True)
        embed.add_field(name="Канал", value=f"https://discord.com/channels/{message.guild.id}/{message.channel.id}", inline=True)
        embed.add_field(name="Сообщение", value=f"[Перейти к сообщению]({message.jump_url})", inline=True)
        embed.set_image(url=f"attachment://screenshot_{message.id}.png")

        await screenshot_channel.send(embed=embed, file=file)
        message.processed = True


@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="за работой станка"),
        status=discord.Status.idle
    )
    print(f"Синхронизировано {len(synced)} команд")
    print(f'Бот {bot.user} готов к работе!')


if __name__ == "__main__":
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        raise ValueError("Токен не найден! Создайте .env файл с DISCORD_BOT_TOKEN=ваш_токен")
    bot.run(token)
