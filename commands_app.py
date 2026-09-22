import discord
from discord import app_commands
from screenshot_bot_db import db
from screenshot_bot import bot


@bot.tree.command(name="config_threshold", description="Определяет пороговое количество реакций для сообщений")
@app_commands.describe(value="Число реакций")
@app_commands.checks.has_permissions(administrator=True)
async def threshold(interaction: discord.Interaction, value: int):
    db.set_server_config(interaction.guild.id, threshold=value)
    await interaction.response.send_message(
        content=f"Пороговое количество реакций изменено на **{value}**",
        ephemeral=True
    )


@bot.tree.command(name="config_emoji", description="Определяет эмодзи для работы бота")
@app_commands.describe(emoji="Эмодзи (или unicode, или :name:)")
@app_commands.checks.has_permissions(administrator=True)
async def config_emoji(interaction: discord.Interaction, emoji: str):
    db.set_server_config(interaction.guild.id, emoji=emoji)
    await interaction.response.send_message(
        content=f"Эмодзи для срабатывания изменено на {emoji}",
        ephemeral=True
    )


@bot.tree.command(name="config_channel", description="Определяет канал для скриншотов")
@app_commands.describe(channel_id="ID канала (ПКМ по каналу -> Copy Channel ID)")
@app_commands.checks.has_permissions(administrator=True)
async def config_channel(interaction: discord.Interaction, channel_id: str):
    db.set_server_config(interaction.guild.id, channel=int(channel_id))
    await interaction.response.send_message(
        content=f"Канал <#{channel_id}> успешно установлен",
        ephemeral=True
    )


@bot.tree.command(name="config_timezone", description="Определяет ваш часовой пояс")
@app_commands.describe(zone="Формат: Часть_света/Город (например Europe/Moscow)")
@app_commands.checks.has_permissions(administrator=True)
async def timezone(interaction: discord.Interaction, zone: str):
    db.set_server_config(interaction.guild.id, timezone=zone)
    await interaction.response.send_message(
        content=f"Время выставлено по зоне **{zone}**",
        ephemeral=True
    )


@bot.tree.command(name="config_color", description="Определяет цвет embed-сообщения со скриншотом")
@app_commands.describe(colour="HEX-цвет (например 7276AD или #7276AD)")
@app_commands.checks.has_permissions(administrator=True)
async def embed_color(interaction: discord.Interaction, colour: str):
    clean_colour = colour.lstrip("#")
    if len(clean_colour) != 6 or not all(c in "0123456789abcdefABCDEF" for c in clean_colour):
        await interaction.response.send_message(
            content="Некорректный HEX-цвет. Укажите 6 символов (например 7276AD)",
            ephemeral=True
        )
        return

    db.set_server_config(interaction.guild.id, color=clean_colour)
    embed = discord.Embed(
        title=f"Цвет **#{clean_colour}**",
        color=int(clean_colour, 16)
    )
    embed.add_field(name="", value="Цвет для embed сообщений установлен", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="config", description="Показать текущие настройки сервера")
@app_commands.checks.has_permissions(administrator=True)
async def config_command(interaction: discord.Interaction):
    config = db.get_config(interaction.guild.id)

    channel_info = "Не установлен"
    if config['channel']:
        channel = interaction.guild.get_channel(config['channel'])
        channel_info = channel.mention if channel else "Канал не найден"

    embed = discord.Embed(
        title="Текущие настройки сервера",
        color=int(config['color'], 16) if config['color'] else 0x00ff00
    )
    embed.add_field(name="Канал для скриншотов", value=channel_info, inline=False)
    embed.add_field(name="Порог реакций", value=config['threshold'], inline=True)
    embed.add_field(name="Эмодзи", value=config['emoji'], inline=True)
    embed.add_field(name="Цвет embed", value=f"#{config['color']}", inline=False)
    embed.add_field(name="Часовой пояс", value=config['timezone'], inline=True)

    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="reset_config", description="Сбросить настройки сервера к значениям по умолчанию")
@app_commands.checks.has_permissions(administrator=True)
async def reset_config_command(interaction: discord.Interaction):
    deleted = db.delete_server_config(interaction.guild.id)
    if deleted:
        await interaction.response.send_message(
            "Настройки сервера сброшены к значениям по умолчанию!",
            ephemeral=True
        )
    else:
        await interaction.response.send_message(
            "Настройки уже были сброшены или не существовали",
            ephemeral=True
        )
