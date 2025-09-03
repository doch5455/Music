from config import LOG, LOG_GROUP_ID
import psutil
from ArchMusic import app
from ArchMusic.utils.database import is_on_off
from ArchMusic.utils.database.memorydatabase import (
    get_active_chats, get_active_video_chats
)
from ArchMusic.utils.database import (
    get_global_tops, get_particulars, get_queries,
    get_served_chats, get_served_users,
    get_sudoers, get_top_chats, get_topp_users
)


# 📌 Sistem bilgilerini döndüren yardımcı fonksiyon
def get_system_status():
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    return f"{cpu}%", f"{mem}%", f"{disk}%"


# 📌 Grup bilgilerini döndüren yardımcı fonksiyon
async def get_chat_info(chat):
    uye_sayisi = await app.get_chat_members_count(chat.id)
    chatusername = f"@{chat.username}" if chat.username else "Yok / Özel Grup"
    return uye_sayisi, chatusername


# 📌 Kullanıcı adı güvenli kontrol
def safe_username(user):
    return f"@{user.username}" if user.username else "Yok"


# 📌 Log mesajı şablonu
def build_log_text(message, user, chatusername, username, uye_sayisi,
                   CPU, RAM, DISK, toplam_grup, aktif_sesli, aktif_video,
                   streamtype, duration, filesize, start_time, end_time, requester):
    return f"""
🔊 **Yeni Müzik Oynatıldı**

📚 **Grup:** {message.chat.title} [`{message.chat.id}`]  
🔗 **Grup Linki:** {chatusername}  
👥 **Üye Sayısı:** {uye_sayisi}  

👤 **Kullanıcı:** {user.mention}  
✨ **Kullanıcı Adı:** {username}  
🔢 **Kullanıcı ID:** `{user.id}`  

🔎 **Sorgu:** {message.text}  
🎶 **Oynatma Türü:** `{streamtype}`  
⏱️ **Süre:** `{duration}`  
💾 **Dosya Boyutu:** `{filesize}`  
🕒 **Başlatılma Zamanı:** `{start_time}`  
🔚 **Bitiş Zamanı:** `{end_time}`  
🙋 **Ekleyen Kullanıcı:** `{requester}`

💻 **Sistem Durumu**
├ 🖥️ CPU: `{CPU}`
├ 🧠 RAM: `{RAM}`
└ 💾 Disk: `{DISK}`

📊 **Genel Durum**
├ 🌐 Toplam Grup: `{toplam_grup}`
├ 🔊 Aktif Ses: `{aktif_sesli}`
└ 🎥 Aktif Video: `{aktif_video}`
"""


# 📌 Ana fonksiyon
async def play_logs(message, streamtype, duration, filesize, start_time, end_time, requester):
    chat_id = message.chat.id
    user = message.from_user

    # Grup ve kullanıcı bilgileri
    uye_sayisi, chatusername = await get_chat_info(message.chat)
    username = safe_username(user)

    # Veritabanı bilgileri
    toplam_grup = len(await get_served_chats())
    aktif_sesli = len(await get_active_chats())
    aktif_video = len(await get_active_video_chats())

    # Sistem durumu
    CPU, RAM, DISK = get_system_status()

    # Log aktif mi kontrolü
    if await is_on_off(LOG):
        logger_text = build_log_text(
            message, user, chatusername, username, uye_sayisi,
            CPU, RAM, DISK, toplam_grup, aktif_sesli, aktif_video,
            streamtype, duration, filesize, start_time, end_time, requester
        )

        # Log mesajını gönder
        if chat_id != LOG_GROUP_ID:
            try:
                await app.send_message(
                    LOG_GROUP_ID,
                    logger_text,
                    disable_web_page_preview=True,
                )
                await app.set_chat_title(
                    LOG_GROUP_ID,
                    f"🔊 Aktif Ses - {aktif_sesli}"
                )
            except Exception as e:
                print(f"Log gönderilemedi: {e}")
