# GEREKLİ KÜTÜPHANELER
import asyncio  # Otomatik mesaj silme için eklendi
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message, ChatMemberUpdated, DeletedMessages
# MessageEntityType ve ChatMembersFilter eklendi
from pyrogram.enums import ChatMemberStatus, MessageEntityType, ChatMembersFilter 
from config import LOG_GROUP_ID
from ArchMusic import app

# --- GENEL AYARLAR VE ÖNBELLEKLER ---

# Silinen mesajları yakalamak için mesajları geçici olarak saklayacağımız bir sözlük
message_cache = {}
# Ping komutunun başlangıç zamanı için
bot_start_time = datetime.now()
# Anti-flood için önbellek
flood_cache = {}
FLOOD_LIMIT = 5  # 5 saniye içinde
FLOOD_COUNT = 5  # 5 mesajdan fazla atarsa


# --- ANA FONKSİYONLAR ---

# 📝 Log mesajı gönder ve dosyaya kaydet (Çekirdek Fonksiyon)
async def send_log(text: str, user_id: int = None, chat=None):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Gruba log mesajını gönder
        await app.send_message(LOG_GROUP_ID, f"🕒 `{timestamp}`\n\n{text}")
        # Yerel dosyaya yaz
        with open("logs.txt", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}]\n{text}\n\n")
    except Exception as e:
        # Ana log fonksiyonu hata verirse, sonsuz döngüye girmemek için konsola yaz
        print(f"[ANA LOG HATASI] Log gönderilemedi: {e}")


# --- KULLANICI KOMUTLARI ---

# 핑 / Durum Kontrol Komutu
@app.on_message(filters.command("ping") & filters.group)
async def ping_command(client: Client, message: Message):
    start = datetime.now()
    await message.reply_chat_action("typing")
    end = datetime.now()
    latency = (end - start).microseconds / 1000
    uptime = str(datetime.now() - bot_start_time).split('.')[0]
    
    await message.reply_text(
        f"🔔 **Pong!**\n"
        f"⚡️ Gecikme: `{latency:.2f} ms`\n"
        f"⏳ Çalışma Süresi: `{uptime}`"
    )

# 👤 Kullanıcı Bilgisi Komutu
@app.on_message(filters.command("info") & filters.group)
async def user_info(client: Client, message: Message):
    target_user = message.reply_to_message.from_user if message.reply_to_message else message.from_user
    info_text = (
        f"👤 **Kullanıcı Bilgileri**\n\n"
        f"**İsim:** {target_user.first_name}\n"
        f"**Kullanıcı Adı:** @{target_user.username or 'Yok'}\n"
        f"**ID:** `{target_user.id}`\n"
        f"**Mention:** {target_user.mention}\n"
        f"**Bot mu?:** {'Evet' if target_user.is_bot else 'Hayır'}"
    )
    await message.reply_text(info_text)

# 🆔 GRUP/KULLANICI ID KOMUTU (YENİ!)
@app.on_message(filters.command("id") & filters.group)
async def id_command(client: Client, message: Message):
    chat_id = message.chat.id
    text = f"🔹 **Bu Grubun ID'si:** `{chat_id}`\n"
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        text += f"🔹 **Yanıtlanan Kullanıcının ID'si:** `{user_id}`"
    else:
        user_id = message.from_user.id
        text += f"🔹 **Sizin ID'niz:** `{user_id}`"
        
    await message.reply_text(text)

# 🛡️ YÖNETİCİ LİSTESİ KOMUTU (YENİ!)
@app.on_message(filters.command("admins") & filters.group)
async def admins_list(client: Client, message: Message):
    admin_list = []
    try:
        async for admin in app.get_chat_members(message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS):
            if not admin.user.is_bot:
                admin_list.append(f"• {admin.user.mention}")
        
        if not admin_list:
            await message.reply_text("Bu grupta bot olmayan yönetici bulunamadı.")
            return

        await message.reply_text(
            "👑 **Grup Yöneticileri:**\n\n" + "\n".join(admin_list)
        )
    except Exception as e:
        await message.reply_text(f"Yöneticiler alınamadı: `{e}`")


# --- MESAJ İÇERİĞİ LOGLAMA ---

# 1. Adım: Gelen her mesajı silinme ihtimaline karşı önbelleğe al
@app.on_message(filters.group, group=1)
async def cache_messages(client: Client, message: Message):
    if message.text or message.caption:
        message_cache[message.id] = {
            "user_id": message.from_user.id if message.from_user else 0,
            "user_mention": message.from_user.mention if message.from_user else "Bilinmiyor",
            "chat_id": message.chat.id,
            "chat_title": message.chat.title,
            "text": message.text or message.caption,
            "date": message.date,
        }
    if len(message_cache) > 1000:
        old_keys = list(message_cache.keys())[:100]
        for key in old_keys:
            del message_cache[key]

# 🤖 Kullanılan Komutları Loglama
@app.on_message(filters.regex(r"^[./!]") & filters.group & ~filters.via_bot)
async def log_commands(client: Client, message: Message):
    if not message.from_user or len(message.text) < 2: return
    text = (
        f"🤖 **Komut Kullanıldı**\n"
        f"👤 Yapan: {message.from_user.mention}\n🆔 `{message.from_user.id}`\n"
        f"👥 Grup: {message.chat.title} (`{message.chat.id}`)\n"
        f"💬 Komut: `{message.text}`\n"
        f"🔗 [Mesaja Git]({message.link})"
    )
    await send_log(text, message.from_user.id, chat=message.chat)

# 🔗 Bağlantı (Link) Paylaşımlarını Loglama
@app.on_message((filters.entity(MessageEntityType.URL) | filters.entity(MessageEntityType.TEXT_LINK)) & filters.group & ~filters.via_bot & ~filters.administrator)
async def log_links(client: Client, message: Message):
    if not message.from_user: return
    text = (
        f"🔗 **Bağlantı Paylaşıldı**\n"
        f"👤 Yapan: {message.from_user.mention}\n🆔 `{message.from_user.id}`\n"
        f"👥 Grup: {message.chat.title} (`{message.chat.id}`)\n"
        f"💬 Mesaj: `{message.text}`\n"
        f"🔗 [Mesaja Git]({message.link})"
    )
    await send_log(text, message.from_user.id, chat=message.chat)
    
# 📣 Önemli Bahsetmeleri (Mention) Yakalama
@app.on_message(filters.regex(r"(?i)@admin|@everyone") & filters.group & ~filters.via_bot)
async def log_mentions(client: Client, message: Message):
    if not message.from_user: return
    text = (
        f"📣 **Önemli Etiket Kullanıldı!**\n"
        f"👤 Yapan: {message.from_user.mention}\n🆔 `{message.from_user.id}`\n"
        f"👥 Grup: {message.chat.title} (`{message.chat.id}`)\n"
        f"💬 Mesaj: `{message.text}`\n"
        f"🔗 [Mesaja Git]({message.link})"
    )
    await send_log(text, message.from_user.id, chat=message.chat)

# 🖼️ Medya Paylaşımlarını Loglama
@app.on_message(filters.media & filters.group & ~filters.via_bot)
async def log_media(client: Client, message: Message):
    if not message.from_user: return
    media_type = message.media.value.split('_')[0] if message.media else "Bilinmeyen Medya"
    text = (
        f"🖼️ **Medya Paylaşıldı**\n"
        f"👤 Yapan: {message.from_user.mention}\n🆔 `{message.from_user.id}`\n"
        f"👥 Grup: {message.chat.title} (`{message.chat.id}`)\n"
        f"📄 Medya Türü: `{media_type.capitalize()}`\n"
        f"🔗 [Mesaja Git]({message.link})"
    )
    await send_log(text, message.from_user.id, chat=message.chat)

# ➡️ Yönlendirilen Mesajları Loglama
@app.on_message(filters.forwarded & filters.group & ~filters.via_bot)
async def log_forwards(client: Client, message: Message):
    if not message.from_user: return
    forward_from = "Bilinmeyen Kaynak"
    if message.forward_from_chat:
        forward_from = f"{message.forward_from_chat.title} (`{message.forward_from_chat.id}`)"
    elif message.forward_from:
        forward_from = f"{message.forward_from.mention} (`{message.forward_from.id}`)"
    
    text = (
        f"➡️ **Mesaj Yönlendirildi**\n"
        f"👤 Yönlendiren: {message.from_user.mention}\n"
        f"👥 Grup: {message.chat.title} (`{message.chat.id}`)\n"
        f"↪️ Kaynak: {forward_from}\n"
        f"🔗 [Mesaja Git]({message.link})"
    )
    await send_log(text, message.from_user.id, chat=message.chat)
    
# --- MESAJ HAREKETLERİNİ LOGLAMA ---

# ✏️ Düzenlenen Mesajları Loglama
@app.on_edited_message(filters.group & ~filters.via_bot)
async def on_edited_message(client: Client, message: Message):
    if not message.from_user or (datetime.now() - message.date).total_seconds() > 3600: return
    text = (
        f"✏️ **Mesaj Düzenlendi**\n"
        f"👤 Düzenleyen: {message.from_user.mention}\n🆔 `{message.from_user.id}`\n"
        f"👥 Grup: {message.chat.title} (`{message.chat.id}`)\n"
        f"🔗 [Mesaja Git]({message.link})"
    )
    await send_log(text, message.from_user.id, chat=message.chat)

# 🗑️ Silinen Mesajları Loglama
@app.on_deleted_messages()
async def on_deleted_message(client: Client, deleted_messages: DeletedMessages):
    for msg in deleted_messages.messages:
        if msg.id in message_cache:
            cached_msg = message_cache[msg.id]
            if (datetime.now() - cached_msg["date"]).total_seconds() > 3600:
                del message_cache[msg.id]
                continue
            text = (
                f"🗑️ **Mesaj Silindi**\n"
                f"👤 Gönderen: {cached_msg['user_mention']}\n🆔 `{cached_msg['user_id']}`\n"
                f"👥 Grup: {cached_msg['chat_title']} (`{cached_msg['chat_id']}`)\n"
                f"💬 Mesaj: `{cached_msg['text']}`"
            )
            await send_log(text, cached_msg["user_id"])
            del message_cache[msg.id]

# 🌊 ANTI-FLOOD UYARISI LOGLAMASI
@app.on_message(filters.group & ~filters.service, group=2)
async def log_flood_warning(client: Client, message: Message):
    if not message.from_user: return
    user_id, chat_id, now = message.from_user.id, message.chat.id, datetime.now()
    if user_id not in flood_cache: flood_cache[user_id] = []
    flood_cache[user_id] = [t for t in flood_cache[user_id] if (now - t).total_seconds() < FLOOD_LIMIT]
    flood_cache[user_id].append(now)
    if len(flood_cache[user_id]) == FLOOD_COUNT + 1: # Sadece 1 kez uyar
        text = (
            f"🚨 **Flood Uyarısı!**\n"
            f"👤 Yapan: {message.from_user.mention}\n🆔 `{user_id}`\n"
            f"👥 Grup: {message.chat.title} (`{chat_id}`)\n"
            f"💬 {FLOOD_LIMIT} saniyede {len(flood_cache[user_id])} mesaj attı."
        )
        await send_log(text, user_id, chat=message.chat)

# --- GRUP YÖNETİMİ VE ÜYELİK LOGLAMA ---

# ℹ️ Grup Bilgisi Değişikliklerini Loglama (GÜNCELLENDİ: Unpin eklendi)
@app.on_message(filters.group & filters.service)
async def on_service_message(client: Client, message: Message):
    if not message.from_user: return
    text = None
    if message.new_chat_title:
        text = f"✏️ **Grup Başlığı Değiştirildi**\n👤 Yapan: {message.from_user.mention}\n💬 Yeni Başlık: `{message.new_chat_title}`\n👥 Grup: {message.chat.title} (`{message.chat.id}`)"
    elif message.new_chat_photo:
        text = f"🖼️ **Grup Fotoğrafı Değiştirildi**\n👤 Yapan: {message.from_user.mention}\n👥 Grup: {message.chat.title} (`{message.chat.id}`)"
    elif message.pinned_message:
        text = f"📌 **Mesaj Sabitlendi**\n👤 Yapan: {message.from_user.mention}\n👥 Grup: {message.chat.title} (`{message.chat.id}`)\n🔗 [Mesaja Git]({message.pinned_message.link})"
    # --- YENİ EKLENEN KISIM ---
    elif message.unpinned_message:
        text = f"📌 **Sabitlenmiş Mesaj Kaldırıldı**\n👤 Yapan: {message.from_user.mention}\n👥 Grup: {message.chat.title} (`{message.chat.id}`)"
    # --- YENİ KISIM BİTTİ ---
    if text: await send_log(text, message.from_user.id, chat=message.chat)

# ✅ Üye Katılımını Loglama ve Karşılama (GÜNCELLENDİ: Oto-silme ve Hata Raporlama eklendi)
@app.on_message(filters.new_chat_members)
async def on_new_member(client: Client, message: Message):
    bot_id = (await client.get_me()).id
    chat = message.chat
    for user in message.new_chat_members:
        ad = message.from_user.first_name if message.from_user else "Bilinmiyor"
        text = ""
        if user.id == bot_id:
            text = f"✅ **Bot Gruba Eklendi**\n👥 {chat.title} (`{chat.id}`)\n➕ Ekleyen: {ad}"
            await send_log(text)
        elif user.is_bot:
            text = f"🚨 **Gruba Bot Eklendi!**\n🤖 Bot: {user.mention} (`{user.id}`)\n👥 Grup: {chat.title} (`{chat.id}`)\n➕ Ekleyen: {ad}"
            await send_log(text, user.id)
        else:
            text = f"👤 **Kullanıcı Gruba Katıldı**\n👤 {user.mention}\n🆔 `{user.id}`\n👥 {chat.title} (`{chat.id}`)\n➕ Ekleyen: {ad}"
            await send_log(text, user.id)
            try:
                # --- GÜNCELLENEN KISIM ---
                sent_message = await message.reply_text(f"👋 Aramıza hoş geldin {user.mention}!")
                await asyncio.sleep(300) # 5 dakika (300 saniye) bekle
                await sent_message.delete()
                # --- GÜNCELLENDİ ---
            except Exception as e:
                # Hata olursa log grubuna bildir
                await send_log(
                    f"⚠️ **Bot Hatası**\n"
                    f"**Fonksiyon:** `on_new_member` (Hoş geldin mesajı)\n"
                    f"**Grup:** {chat.title} (`{chat.id}`)\n"
                    f"**Hata:** `{e}`"
                )

# 🚪 Üye Ayrılışını Loglama
@app.on_message(filters.left_chat_member)
async def on_left_member(client: Client, message: Message):
    bot_id = (await client.get_me()).id
    user = message.left_chat_member
    chat = message.chat
    ad = message.from_user.first_name if message.from_user else "Bilinmiyor"
    text = ""
    if user.id == bot_id:
        text = f"🚫 **Bot Gruptan Atıldı**\n👥 {chat.title} (`{chat.id}`)\n🚷 Atan: {ad}"
    else:
        text = f"🚷 **Kullanıcı Ayrıldı / Atıldı**\n👤 {user.mention}\n🆔 `{user.id}`\n👥 {chat.title} (`{chat.id}`)\n👢 Atan: {ad}"
    await send_log(text, user.id)

# 🛡️ Üyelik Durumu Değişikliklerini Loglama (GÜNCELLENDİ: Mute/Kısıtlama eklendi)
@app.on_chat_member_updated()
async def on_chat_member_update(client: Client, update: ChatMemberUpdated):
    if not (update.old_chat_member and update.new_chat_member): return
    old_status = getattr(update.old_chat_member, "status", None)
    new_status = getattr(update.new_chat_member, "status", None)
    if old_status == new_status: return
    
    user = update.new_chat_member.user
    yapan_yonetici = update.performed_by.user if update.performed_by else None
    chat = update.chat
    text = ""
    
    base_text = f"👤 {user.mention}\n🆔 `{user.id}`\n👥 {chat.title} (`{chat.id}`)"
    if yapan_yonetici: base_text += f"\n✨ Yapan: {yapan_yonetici.mention}"

    if new_status == ChatMemberStatus.ADMINISTRATOR:
        text = f"🛡️ **Yönetici Yapıldı**\n{base_text}"
    elif old_status == ChatMemberStatus.ADMINISTRATOR and new_status != ChatMemberStatus.ADMINISTRATOR:
        text = f"⚠️ **Yönetici Yetkisi Alındı**\n{base_text}"
    elif new_status == ChatMemberStatus.BANNED:
        text = f"⛔ **Kullanıcı Banlandı**\n{base_text}"
    elif old_status == ChatMemberStatus.BANNED and new_status != ChatMemberStatus.BANNED:
        text = f"🔓 **Ban Kaldırıldı**\n{base_text}"
    # --- YENİ EKLENEN KISIM ---
    elif new_status == ChatMemberStatus.RESTRICTED:
        detay = " (Susturuldu)" if not update.new_chat_member.privileges.can_send_messages else ""
        text = f"🔇 **Kullanıcı Kısıtlandı{detay}**\n{base_text}"
    elif old_status == ChatMemberStatus.RESTRICTED and new_status == ChatMemberStatus.MEMBER:
        text = f"🔊 **Kullanıcı Kısıtlaması Kaldırıldı**\n{base_text}"
    # --- YENİ KISIM BİTTİ ---

    if text: await send_log(text, user.id, chat=chat)
