from config import LOG, LOG_GROUP_ID
import psutil
import platform
import json
import os
import time
import socket
import logging
import sqlite3
import contextlib
from datetime import datetime
import pytz
import locale
from asyncio import Queue, create_task, sleep
from typing import Optional, Tuple, Union
from time import perf_counter

from ArchMusic import app
from ArchMusic.utils.database import is_on_off
from ArchMusic.utils.database.memorydatabase import (
    get_active_chats, get_active_video_chats
)
from ArchMusic.utils.database import get_served_chats


# Türkçe locale (opsiyonel)
try:
    locale.setlocale(locale.LC_TIME, "tr_TR.UTF-8")
except Exception:
    pass


# ------------------------------------------------
# 🔧 Global Ayarlar
# ------------------------------------------------
BOT_START_TIME = time.time()
LOG_FORMAT = "markdown"
ALLOWED_USERS = []  # Boş bırakılırsa herkes log üretebilir
DEVELOPER_ID = 123456789  # Opsiyonel hata bildirimi
log_queue = Queue()

logging.basicConfig(
    filename="bot_play_logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# ------------------------------------------------
# 🔧 Yardımcı Fonksiyonlar
# ------------------------------------------------

def rotate_log_file(path="bot_play_logs.txt", limit_mb=5):
    if os.path.exists(path) and os.path.getsize(path) > limit_mb * 1024 * 1024:
        os.rename(path, f"{path}.{int(time.time())}.bak")

def get_system_status() -> Tuple[str, str, str]:
    try:
        cpu = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent
        return f"{cpu}%", f"{mem}%", f"{disk}%"
    except Exception as e:
        print(f"Sistem bilgisi alınamadı: {e}")
        return "0%", "0%", "0%"

def get_system_details() -> str:
    system = platform.system()
    release = platform.release()
    cores = psutil.cpu_count(logical=True)
    return f"{system} {release} | {cores} Çekirdek"

def get_cpu_temp():
    try:
        temps = psutil.sensors_temperatures()
        if "coretemp" in temps:
            t = temps["coretemp"][0].current
            return f"{t}°C"
    except Exception:
        pass
    return "N/A"

def get_io_status():
    try:
        net = psutil.net_io_counters()
        sent = round(net.bytes_sent / 1024 / 1024, 2)
        recv = round(net.bytes_recv / 1024 / 1024, 2)
        return f"⬆️ {sent}MB / ⬇️ {recv}MB"
    except Exception:
        return "N/A"

def get_server_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except Exception:
        return "Bilinmiyor"

def warn_high_usage(value_str: str) -> str:
    value = float(value_str.replace("%", ""))
    if value > 85:
        return "🔥"
    elif value > 70:
        return "⚠️"
    return "✅"

def get_uptime() -> str:
    uptime_seconds = int(time.time() - BOT_START_TIME)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

async def get_ping() -> str:
    start = time.time()
    await app.get_me()
    ping = (time.time() - start) * 1000
    return f"{ping:.0f} ms"

def get_turkish_datetime() -> str:
    istanbul = pytz.timezone("Europe/Istanbul")
    now = datetime.now(istanbul)
    tarih = now.strftime("%d %B %Y")
    saat = now.strftime("%H:%M:%S")
    gun = now.strftime("%A")
    return f"📅 {tarih}\n⏰ {saat} ({gun})"

def safe_username(user) -> str:
    return f"@{user.username}" if getattr(user, "username", None) else "Yok"

def write_log_to_file(log_text: str):
    rotate_log_file()
    try:
        logging.info(log_text)
    except Exception as e:
        print(f"Log dosyasına yazılamadı: {e}")

def mask_sensitive_data(text: str) -> str:
    return text.replace("@", "@*").replace(str(LOG_GROUP_ID), "******")

def increase_query_count():
    try:
        data = json.load(open("query_count.json", "r"))
    except FileNotFoundError:
        data = {"count": 0}
    data["count"] += 1
    json.dump(data, open("query_count.json", "w"))
    return data["count"]

def detect_source(message) -> str:
    if message.text and message.text.startswith("/"):
        return "Komut"
    elif getattr(message, "via_bot", None):
        return "Inline"
    elif getattr(message, "entities", None):
        return "Bağlantı"
    return "Manuel"

def save_query_history(user_id, query):
    try:
        data = json.load(open("query_history.json", "r"))
    except FileNotFoundError:
        data = {}
    data.setdefault(str(user_id), []).append(query)
    json.dump(data, open("query_history.json", "w"), ensure_ascii=False)

def save_to_sqlite(user_id, action, song):
    conn = sqlite3.connect("logs.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS logs (user_id INT, action TEXT, song TEXT, time TEXT)")
    cur.execute("INSERT INTO logs VALUES (?, ?, ?, ?)", (user_id, action, song, datetime.now().isoformat()))
    conn.commit()
    conn.close()

async def report_error(e):
    try:
        await app.send_message(DEVELOPER_ID, f"❗Hata: {e}")
    except Exception:
        pass

@contextlib.contextmanager
def measure_time(name="Process"):
    start = perf_counter()
    yield
    print(f"{name} süresi: {perf_counter() - start:.3f}s")

# ------------------------------------------------
# 🔧 Log Kuyruğu & Otomatik Rapor
# ------------------------------------------------

async def log_worker():
    while True:
        text = await log_queue.get()
        try:
            await app.send_message(LOG_GROUP_ID, text, disable_web_page_preview=True)
        except Exception as e:
            await report_error(e)
        log_queue.task_done()

async def daily_status_report():
    while True:
        CPU, RAM, DISK = get_system_status()
        uptime = get_uptime()
        await app.send_message(
            LOG_GROUP_ID,
            f"📅 Günlük Rapor\n🖥️ CPU: {CPU}\n🧠 RAM: {RAM}\n💾 Disk: {DISK}\n⏳ Uptime: {uptime}"
        )
        await sleep(86400)

# ------------------------------------------------
# 🔧 Ana Fonksiyonlar
# ------------------------------------------------

async def get_chat_info(chat) -> Tuple[Union[int, str], str]:
    try:
        uye_sayisi = await app.get_chat_members_count(chat.id)
    except Exception:
        uye_sayisi = "Bilinmiyor"
    if getattr(chat, "username", None):
        chatusername = f"@{chat.username}"
    else:
        try:
            chatusername = await app.export_chat_invite_link(chat.id)
        except Exception:
            chatusername = "Yok / Özel Grup"
    return uye_sayisi, chatusername


def build_log_text(
    message, user, chatusername, username, uye_sayisi,
    CPU, RAM, DISK, toplam_grup, aktif_sesli, aktif_video,
    uptime, ping, system_info, cpu_temp, net_io, query_count,
    tarih_saat, action_type="play", music_title=None, music_artist=None
) -> str:
    music_info = ""
    if music_title:
        music_info += f"\n🎶 Şarkı   : {music_title}"
    if music_artist:
        music_info += f"\n🎤 Sanatçı: {music_artist}"

    sorgu = getattr(message, "text", None) or getattr(message, "caption", "Yok")
    if isinstance(sorgu, str) and len(sorgu) > 200:
        sorgu = sorgu[:200] + "..."

    baslik = "📥 Yeni Şarkı Sıraya Eklendi" if action_type == "queue" else "🔊 Yeni Müzik Oynatıldı"

    user_mention = getattr(user, "mention", None) or f"{user.first_name} (id: {user.id})"
    chat_title = getattr(message.chat, "title", "Özel Chat")

    log = f"""
{baslik}

🕒 Tarih/Saat:
{tarih_saat}

📚 Grup: {chat_title} [{message.chat.id}]
🔗 Grup Linki: {chatusername}
👥 Üye Sayısı: {uye_sayisi}

👤 Kullanıcı: {user_mention}
✨ Kullanıcı Adı: {username}
🔢 Kullanıcı ID: {user.id}
🔍 Kaynak: {detect_source(message)}

🔎 Sorgu: {sorgu}{music_info}

💻 Sistem Durumu
├ 🧩 Sistem: {system_info}
├ 🖥️ CPU : {CPU} {warn_high_usage(CPU)}
├ 🧠 RAM : {RAM} {warn_high_usage(RAM)}
├ 💾 Disk: {DISK} {warn_high_usage(DISK)}
├ 🌡️ CPU Sıcaklığı: {cpu_temp}
├ 🌐 Ağ Kullanımı : {net_io}
├ 🌍 Sunucu IP : {get_server_ip()}
└ ⏳ Uptime: {uptime}

⚡ Ping: {ping}

📊 Genel Durum
├ 🌐 Toplam Grup : {toplam_grup}
├ 🔊 Aktif Ses   : {aktif_sesli}
├ 🎥 Aktif Video : {aktif_video}
└ 📈 Toplam Sorgu: {query_count}
"""
    return log


async def play_logs(
    message, streamtype=None, music_title=None,
    music_artist=None, action_type="play"
):
    if ALLOWED_USERS and message.from_user.id not in ALLOWED_USERS:
        return

    with measure_time("Log oluşturma"):
        chat_id = message.chat.id
        user = message.from_user
        uye_sayisi, chatusername = await get_chat_info(message.chat)
        username = safe_username(user)
        toplam_grup = len(await get_served_chats())
        aktif_sesli = len(await get_active_chats())
        aktif_video = len(await get_active_video_chats())

        CPU, RAM, DISK = get_system_status()
        uptime = get_uptime()
        ping = await get_ping()
        system_info = get_system_details()
        cpu_temp = get_cpu_temp()
        net_io = get_io_status()
        query_count = increase_query_count()
        tarih_saat = get_turkish_datetime()

        save_query_history(user.id, getattr(message, "text", "Yok"))
        save_to_sqlite(user.id, action_type, music_title or "Yok")

        if await is_on_off(LOG):
            logger_text = build_log_text(
                message, user, chatusername, username, uye_sayisi,
                CPU, RAM, DISK, toplam_grup, aktif_sesli, aktif_video,
                uptime, ping, system_info, cpu_temp, net_io,
                query_count, tarih_saat, action_type, music_title, music_artist
            )
            logger_text = mask_sensitive_data(logger_text)
            write_log_to_file(logger_text)
            if chat_id != LOG_GROUP_ID:
                await log_queue.put(logger_text)

# ------------------------------------------------
# 🔧 Başlangıç
# ------------------------------------------------
if __name__ == "__main__":
    create_task(log_worker())
    create_task(daily_status_report())
    print("✅ play_logs modülü (pro sürüm) yüklendi — Gelişmiş loglama, rapor, güvenlik ve performans özellikleri aktif.")

