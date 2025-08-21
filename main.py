import discord
from discord import app_commands
from PIL import Image, ImageDraw, ImageFont
import io
import os

TOKEN = os.getenv("TOKEN")
admin_ids_str = os.getenv("ADMIN_IDS", "")
ADMIN_IDS = [int(i) for i in admin_ids_str.split(",") if i.strip().isdigit()]

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

@tree.command(name="draw", description="テキストを画像に描画します")
@app_commands.describe(text="画像に描くテキスト")
async def draw(interaction: discord.Interaction, text: str):
    # キャンバス作成
    img = Image.new("RGB", (500, 200), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    # フォント指定（エラー時は標準フォント）
    try:
        font = ImageFont.truetype("HigureGothic-Black.ttf", 40)
    except:
        font = ImageFont.load_default()
    d.text((10, 80), text, fill=(0, 0, 0), font=font)
    
    # 画像をバイト配列に
    with io.BytesIO() as image_binary:
        img.save(image_binary, 'PNG')
        image_binary.seek(0)
        file = discord.File(fp=image_binary, filename='draw.png')
        await interaction.response.send_message(file=file)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    await tree.sync()
    print('スラッシュコマンドが同期されました。')

bot.run(TOKEN)
