   from datetime import datetime
import io

from pyrogram import filters
from pyrogram.types import Message
from PIL import Image, ImageDraw, ImageFont

from config import BANNED_USERS, MUSIC_BOT_NAME
from strings import get_command
from ArchMusic import app
from ArchMusic.core.call import ArchMusic
from ArchMusic.utils.decorators.language import language

import psutil

### Commands
PING_COMMAND = get_command("PING_COMMAND")


# Güvenli sistem istatistik fonksiyonu
async def bot_sys_stats():
    try:
        disk_io = psutil.disk_io_counters()
        disk_read = disk_io.read_bytes if disk_io else 0
        disk_write = disk_io.write_bytes if disk_io else 0
    except Exception:
        disk_read = disk_write = 0

    try:
        cpu = psutil.cpu_percent()
    except Exception:
        cpu = 0

    try:
        ram = psutil.virtual_memory().percent
    except Exception:
        ram = 0

    uptime = "1 gün"

    try:
        import GPUtil
        gpus = GPUtil.getGPUs()
        gpu_usage = sum(g.load for g in gpus) / len(gpus) * 100 if gpus else 0
    except Exception:
        gpu_usage = 0

    try:
        total_chats = 0
        total_users = 0
        async for dialog in app.get_dialogs():
            total_chats += 1
            if dialog.chat.type in ["group", "supergroup"]:
                try:
                    total_users += await app.get_chat_members_count(dialog.chat.id)
                except Exception:
                    continue
    except Exception:
        total_chats = 0
        total_users = 0

    return uptime, cpu, ram, f"Read:{disk_read} Write:{disk_write}", gpu_usage, total_chats, total_users


# Ping görseli oluşturma fonksiyonu
def create_ping_image(cpu, ram, gpu, disk, ping_ms):
    width, height = 600, 250
    image = Image.new("RGB", (width, height), color=(30, 30, 30))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    draw.text((20, 20), f"CPU: {cpu}%", fill="white", font=font)
    draw.text((20, 50), f"RAM: {ram}%", fill="white", font=font)
    draw.text((20, 80), f"GPU: {gpu:.1f}%", fill="white", font=font)
    draw.text((20, 110), f"Disk: {disk}", fill="white", font=font)
    draw.text((20, 140), f"Ping: {ping_ms:.2f} ms", fill="white", font=font)

    # Görseli byteIO olarak döndür
    bio = io.BytesIO()
    bio.name = "ping.png"
    image.save(bio, "PNG")
    bio.seek(0)
    return bio


@app.on_message(
    filters.command(PING_COMMAND)
    & filters.group
    & ~BANNED_USERS
)
@language
async def ping_com(client, message: Message, _):
    response = await message.reply_text(_["ping_1"])
    start = datetime.now()
    pytgping = await ArchMusic.ping()
    UP, CPU, RAM, DISK, GPU, TOTAL_CHATS, TOTAL_USERS = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000

    # Ping görselini oluştur
    ping_image = create_ping_image(CPU, RAM, GPU, DISK, resp)

    # Mesajı güncelle ve görsel ile gönder
    await response.delete()
    await message.reply_photo(
        photo=ping_image,
        caption=(
            f"{MUSIC_BOT_NAME} Ping!\n"
            f"Uptime: {UP}\n"
            f"Ping: {resp:.2f} ms\n"
            f"Telegram Ping: {pytgping}\n"
            f"Toplam Sohbet: {TOTAL_CHATS}\n"
            f"Toplam Kullanıcı: {TOTAL_USERS}\n"
            "⚡ Hızlı Ping | 📊 Sistem Durumu ✅"
        )
    )

