from datetime import datetime

from pyrogram import filters
from pyrogram.types import Message

from config import BANNED_USERS, MUSIC_BOT_NAME, LOG_GROUP_ID
from strings import get_command
from ArchMusic import app
from ArchMusic.core.call import ArchMusic
from ArchMusic.utils import bot_sys_stats
from ArchMusic.utils.decorators.language import language

### Commands
PING_COMMAND = get_command("PING_COMMAND")


def generate_bar(usage: float, length: int = 20) -> str:
    """Yüzdelik değere göre dolu ve boş bloklardan oluşan mini çubuk oluşturur."""
    filled_length = int(length * usage / 100)
    empty_length = length - filled_length
    bar = "█" * filled_length + "░" * empty_length
    return bar


@app.on_message(
    filters.command(PING_COMMAND)
    & filters.group
    & ~BANNED_USERS
)
@language
async def ping_com(client, message: Message, _):
    try:
        # Ping mesajı (sadece metin)
        response = await message.reply_text(_["ping_1"])

        start_time = datetime.now()

        # Bot ve sistem pingleri
        pytg_ping = await ArchMusic.ping()
        uptime, cpu, ram, disk = await bot_sys_stats()

        # Yanıt süresini hesapla (ms cinsinden)
        end_time = datetime.now()
        response_time_ms = (end_time - start_time).microseconds / 1000

        # Ping sonucu mesajı
        ping_message = f"""
**🎵 {MUSIC_BOT_NAME} Ping Sonuçları**

⏱ Yanıt Süresi: `{response_time_ms:.2f} ms`
📶 Bot Ping: `{pytg_ping} ms`
🖥 CPU Kullanımı: `{cpu}%`
💾 RAM Kullanımı: `{ram}%`
🗄 Disk Kullanımı: `{disk}%`
⏳ Uptime: `{uptime}`
"""
        await response.edit_text(ping_message)

        # Mini çubuk göstergeleri
        cpu_bar = generate_bar(cpu)
        ram_bar = generate_bar(ram)
        disk_bar = generate_bar(disk)

        # Log grubuna mesaj
        log_text = (
            f"📌 **Ping Log**\n"
            f"---------------------------------\n"
            f"👤 Kullanıcı: {message.from_user.mention} (`{message.from_user.id}`)\n"
            f"🏠 Grup: {message.chat.title} (`{message.chat.id}`)\n"
            f"🕒 Zaman: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"---------------------------------\n"
            f"**📊 Ping ve Sistem Bilgileri:**\n"
            f"⏱ Yanıt Süresi: `{response_time_ms:.2f} ms`\n"
            f"📶 Bot Ping: `{pytg_ping} ms`\n"
            f"🖥 CPU: `{cpu}%` {cpu_bar}\n"
            f"💾 RAM: `{ram}%` {ram_bar}\n"
            f"🗄 Disk: `{disk}%` {disk_bar}\n"
            f"⏳ Uptime: `{uptime}`\n"
            f"---------------------------------"
        )
        await client.send_message(LOG_GROUP_ID, log_text, parse_mode="markdown")

    except Exception as e:
        await message.reply_text(f"❌ Ping alınırken bir hata oluştu.\nHata: {e}")

