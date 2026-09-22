import discord
import os
from io import BytesIO
from html2image import Html2Image
from screenshot_bot_db import db
from smart_crop import smart_crop
import pytz


async def take_screenshot(message: discord.Message) -> BytesIO:
    attachments_html = ""
    for attachment in message.attachments:
        ext = attachment.filename.lower()
        if ext.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
            attachments_html += f"""
                <div class="attachment image">
                    <img src="{attachment.url}" alt="{attachment.filename}">
                </div>"""
        elif ext.endswith(('.mp4', '.webm', '.mov')):
            attachments_html += f"""
                <div class="attachment video">
                    <video controls width="400">
                        <source src="{attachment.url}" type="video/{'mp4' if ext.endswith('.mp4') else 'webm'}">
                    </video>
                </div>"""
        else:
            attachments_html += f"""
                <div class="attachment file">
                    <a href="{attachment.url}" target="_blank">{attachment.filename}</a>
                </div>"""

    # Цвет автора (если есть роль с цветом)
    try:
        role_color = message.author.top_role.color
        author_color = f"#{role_color.value:06x}" if role_color.value else "#FFFFFF"
    except Exception:
        author_color = "#FFFFFF"

    # Аватарка
    avatar_url = message.author.display_avatar.url if message.author.display_avatar else ""

    # Декорация аватарки (если есть)
    decoration_url = ""
    try:
        if message.author.avatar_decoration:
            decoration_url = message.author.avatar_decoration.url
    except Exception:
        pass

    # Часовой пояс и время
    try:
        timezone_str = db.get_config(message.guild.id).get("timezone", "Europe/Moscow")
        tz = pytz.timezone(timezone_str)
    except Exception:
        tz = pytz.timezone("Europe/Moscow")
    formatted_time = message.created_at.astimezone(tz).strftime('%H:%M')

    html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{
                    background: #313338;
                    color: #dbdee1;
                    font-family: "gg sans", "Whitney", "Helvetica Neue", Helvetica, Arial, sans-serif;
                    padding: 20px;
                    width: 800px;
                }}
                .message-container {{
                    display: flex;
                    gap: 16px;
                }}
                .avatar-container {{
                    position: relative;
                    width: 44px;
                    height: 44px;
                    flex-shrink: 0;
                }}
                .avatar {{
                    width: 44px;
                    height: 44px;
                    border-radius: 50%;
                    object-fit: cover;
                }}
                .avatar-decoration {{
                    position: absolute;
                    top: -6px;
                    left: -6px;
                    width: 56px;
                    height: 56px;
                    object-fit: contain;
                    pointer-events: none;
                }}
                .message-content {{
                    display: flex;
                    flex-direction: column;
                    gap: 2px;
                    flex-grow: 1;
                    overflow: hidden;
                }}
                .message-header {{
                    display: flex;
                    align-items: baseline;
                    gap: 8px;
                    margin-bottom: 3px;
                }}
                .author {{
                    color: {author_color};
                }}
                .timestamp {{
                    color: #949ba4;
                    font-size: 0.8em;
                }}
                .message-text {{
                    line-height: 1.4;
                    white-space: pre-wrap;
                    word-break: break-word;
                    color: #dbdee1;
                }}
                .attachments {{
                    margin-top: 7px;
                    display: flex;
                    flex-direction: column;
                    gap: 8px;
                    width: 100%;
                }}
                .attachment {{
                    border-radius: 8px;
                    overflow: hidden;
                    background: #2b2d31;
                    max-width: 520px;
                }}
                .attachment.image {{
                    width: fit-content;
                    min-width: 0;
                    background: transparent;
                }}
                .attachment.image img {{
                    max-height: 350px;
                    max-width: 520px;
                    border-radius: 8px;
                    display: block;
                }}
                .attachment.video video {{
                    max-height: 300px;
                    background: #000;
                    border-radius: 8px;
                }}
                .attachment.file a {{
                    color: #00a8fc;
                    text-decoration: none;
                    padding: 10px 12px;
                    display: block;
                }}
                .attachment.file a:hover {{
                    text-decoration: underline;
                }}
            </style>
        </head>
        <body>
            <div class="message-container">
                <div class="avatar-container">
                    <img class="avatar" src="{avatar_url}" alt="">
                    {f'<img class="avatar-decoration" src="{decoration_url}" alt="">' if decoration_url else ""}
                </div>
                <div class="message-content">
                    <div class="message-header">
                        <span class="author">{message.author.display_name}</span>
                        <span class="timestamp">{formatted_time}</span>
                    </div>
                    <div class="message-text">{message.content}</div>
                    <div class="attachments">{attachments_html if message.attachments else ""}</div>
                </div>
            </div>
        </body>
        </html>
        """

    hti = Html2Image()
    raw_path = f"screenshot_raw_{message.id}.png"
    hti.screenshot(
        html_str=html_template,
        save_as=raw_path,
        size=(800, 2000)
    )

    cropped_path = f"screenshot_{message.id}.png"
    has_attachments = bool(message.attachments)
    smart_crop(raw_path, cropped_path, padding=15, crop_right=not has_attachments, right_padding=30)

    with open(cropped_path, 'rb') as f:
        img_bytes = BytesIO(f.read())

    for path in [raw_path, cropped_path]:
        try:
            os.remove(path)
        except OSError:
            pass

    return img_bytes
