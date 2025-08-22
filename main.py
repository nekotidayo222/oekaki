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


# カラーパース関数
def get_color(color: str):
    print(f"受け取ったcolor={color}")  # 確認用
    # 色名やHEXカラー対応
    try:
        return ImageColor.getrgb(color)
    except Exception as e:
        print(f"getrgb error: {e}")
    # カンマ区切りRGB対応
    try:
        parts = [int(x.strip()) for x in color.split(",")]
        if len(parts) == 3:
            return tuple(parts)
    except Exception as e:
        print(f"split error: {e}")
    return (0, 0, 0)  # fallback:黒


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
    print(f"最終的に使う色: {get_color}")  # 確認用
    d.text((10, 80), text, fill=text_color, font=font)
    
    # 画像をバイト配列に
    with io.BytesIO() as image_binary:
        img.save(image_binary, 'PNG')
        image_binary.seek(0)
        file = discord.File(fp=image_binary, filename='draw.png')
        await interaction.response.send_message(file=file)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)

bot.run(TOKEN)
