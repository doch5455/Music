from config import LOG, LOG_GROUP_ID
import psutil
from ArchMusic import app
from ArchMusic.utils.database import is_on_off
from ArchMusic.utils.database.memorydatabase import (
    get_active_chats, get_active_video_chats)
from ArchMusic.utils.database import (
    get_global_tops, get_particulars, get_queries,
    get_served_chats, get_served_users,
    get_sudoers, get_top_chats, get_topp_users)


async def play_logs(message, streamtype):
    chat_id = message.chat.id
    user = message.from_user

    # Grup ve sistem bilgileri
    sayı = await app.get_chat_members_count(chat_id)
    toplamgrup = len(await get_served_chats())
    aktifseslisayısı = len(await get_active_chats())
    aktifvideosayısı = len(await get_active_video_chats())
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent

    CPU = f"{cpu}%"
    RAM = f"{mem}%"
    DISK = f"{disk}%"

    # Grup kullanıcı adı kontrolü
    if message.chat.username:
        chatusername = f"@{message.chat.username}"
    else:
        chatusername = "Gizli Grup"

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
├ 🖥️ CPU: `{CPU}`
├ 🧠 RAM: `{RAM}`
└ 💾 Disk: `{DISK}`

📊 **Genel Durum**
├ 🌐 Toplam Grup: `{toplamgrup}`
├ 🔊 Aktif Ses: `{aktifseslisayısı}`
└ 🎥 Aktif Video: `{aktifvideosayısı}`
"""
        # Log mesajını gönder
        if chat_id != LOG_GROUP_ID:
            try:
                await app.send_message(
                    LOG_GROUP_ID,
                    logger_text,
                    disable_web_page_preview=True,
                )
                await app.set_chat_title(LOG_GROUP_ID, f"🔊 Aktif Ses - {aktifseslisayısı}")
            except:
                pass
