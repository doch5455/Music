import platform
from datetime import datetime, timedelta
import psutil
from ArchMusic import app
from ArchMusic.utils.database import is_on_off
from ArchMusic.utils.database.memorydatabase import (
    get_active_chats, get_active_video_chats)
from ArchMusic.utils.database import (
    get_global_tops, get_particulars, get_queries,
    get_served_chats, get_served_users,
    get_sudoers, get_top_chats, get_topp_users)

# Botun başlangıç zamanı (bot açılırken bir kere set edilmeli)
start_time = datetime.now()

async def play_logs(message, streamtype):
    chat_id = message.chat.id
    user = message.from_user

    # Ping ölçüm başlangıcı
    start_ping = datetime.now()

    # Grup ve sistem bilgileri
    sayı = await app.get_chat_members_count(chat_id)
    toplamgrup = len(await get_served_chats())
    aktifseslisayısı = len(await get_active_chats())
    aktifvideosayısı = len(await get_active_video_chats())
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    disk_free = psutil.disk_usage("/").free // (1024 ** 3)  # GB cinsinden boş alan

    try:
        temps = psutil.sensors_temperatures()
        cpu_temp = temps['coretemp'][0].current if 'coretemp' in temps else "Bilinmiyor"
    except:
        cpu_temp = "Bilinmiyor"

    os_info = platform.system() + " " + platform.release()
    python_version = platform.python_version()

    toplam_kullanıcı_sayısı = 0
    served_chats = await get_served_chats()
    for chat in served_chats:
        try:
            üye_sayısı = await app.get_chat_members_count(chat)
            toplam_kullanıcı_sayısı += üye_sayısı
        except:
            pass

    toplam_kullanıcılar = len(await get_served_users())
    cpu_çekirdek = psutil.cpu_count(logical=True)

    aktif_sesli_grup_mu = chat_id in await get_active_chats()
    aktif_video_grup_mu = chat_id in await get_active_video_chats()

    aktif_sesli_grup_mu_text = "Evet" if aktif_sesli_grup_mu else "Hayır"
    aktif_video_grup_mu_text = "Evet" if aktif_video_grup_mu else "Hayır"

    CPU = f"{cpu}%"
    RAM = f"{mem}%"
    DISK = f"{disk}%"

    if message.chat.username:
        chatusername = f"@{message.chat.username}"
    else:
        chatusername = "Gizli Grup"

    # Aktif grup sayısı (aktif sesli ve video sohbet gruplarının birleşimi)
    aktifsesli_gruplar = set(await get_active_chats())
    aktif_video_gruplar = set(await get_active_video_chats())
    aktif_gruplar_birlesik = aktifsesli_gruplar.union(aktif_video_gruplar)
    aktif_grup_sayisi = len(aktif_gruplar_birlesik)

    # Uptime hesapla
    uptime_seconds = (datetime.now() - start_time).total_seconds()
    uptime_str = str(timedelta(seconds=int(uptime_seconds)))

    # Ping ölçümü (işlem süresi)
    end_ping = datetime.now()
    ping_ms = int((end_ping - start_ping).total_seconds() * 1000)

    # Log aktif mi kontrolü
    if await is_on_off(LOG):
        logger_text = f"""
🔊 **Yeni Müzik Oynatıldı**

📚 **Grup:** {message.chat.title} [`{chat_id}`]  
🔗 **Grup Linki:** {chatusername}  
👥 **Üye Sayısı:** {sayı}  

👤 **Kullanıcı:** {user.mention}  
✨ **Kullanıcı Adı:** @{user.username}  
🔢 **Kullanıcı ID:** `{user.id}`  

🔎 **Sorgu:** {message.text}

💻 **Sistem Durumu**
├ 🖥️ CPU: `{CPU}` ({cpu_çekirdek} çekirdek)
├ 🌡️ CPU Sıcaklığı: `{cpu_temp}°C`
├ 🧠 RAM: `{RAM}`
├ 💾 Disk Kullanımı: `{DISK}`
└ 💽 Boş Disk Alanı: `{disk_free} GB`

🖥️ Sunucu: {os_info}
🐍 Python Versiyonu: {python_version}

⏱️ **Bot Çalışma Süresi:** {uptime_str}
📶 **Ping:** {ping_ms} ms

📊 **Genel Durum**
├ 🌐 Toplam Grup: `{toplamgrup}`
├ ⚡️ Aktif Grup Sayısı: `{aktif_grup_sayisi}`
├ 👥 Toplam Kullanıcı (tüm gruplar): `{toplam_kullanıcı_sayısı}`
├ 🧑‍🤝‍🧑 Hizmet Verilen Kullanıcılar: `{toplam_kullanıcılar}`
├ 🔊 Aktif Ses: `{aktifseslisayısı}`
├ 🎥 Aktif Video: `{aktifvideosayısı}`
├ 📍 Bu Grup Aktif Sesli mi?: {aktif_sesli_grup_mu_text}
└ 📍 Bu Grup Aktif Video mu?: {aktif_video_grup_mu_text}
"""
        if chat_id != LOG_GROUP_ID:
            try:
                await app.send_message(
                    LOG_GROUP_ID,
                    logger_text,
                    disable_web_page_preview=True,
                )
                await app.set_chat_title(LOG_GROUP_ID, f"🔊 Aktif Ses - {aktifseslisayısı}")
            except Exception as e:
                print(f"Log gönderme veya başlık güncelleme hatası: {e}")
