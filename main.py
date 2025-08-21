import discord
from discord import app_commands
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import io
import os

TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def draw(ctx, *, text: str):
    # キャンバス作成
    img = Image.new("RGB", (500, 200), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    # フォント指定（エラー時は標準フォント）
    try:
    font = ImageFont.truetype("NotoSansJP-Regular.otf", 40)  # ←インデントあり
    except:
    font = ImageFont.load_default()
    d.text((10, 80), text, fill=(0, 0, 0), font=font)
    
    # 画像をバイト配列に
    with io.BytesIO() as image_binary:
        img.save(image_binary, 'PNG')
        image_binary.seek(0)
        await ctx.send(file=discord.File(fp=image_binary, filename='draw.png'))

bot.run(TOKEN)
