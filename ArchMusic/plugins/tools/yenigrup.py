import os
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message, ChatMemberUpdated
from pyrogram.enums import ChatMemberStatus
from config import LOG_GROUP_ID
from ArchMusic import app


# 🖼️ Profil resmi indir
async def download_user_photo(user_id: int, save_dir="pfps"):
    try:
        photos = await app.get_profile_photos(user_id)
        if photos.total_count > 0:
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            file_path = f"{save_dir}/{user_id}.jpg"
            await app.download_media(photos[0].file_id, file_path)
            return file_path
    except Exception as e:
        print(f"[HATA] Profil resmi indirilemedi: {e}")
    return None


# 📝 Log gönder ve dosyaya kaydet
async def send_log(text: str, user_id: int = None, chat=None):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if user_id:
            await download_user_photo(user_id)

        # Grup bilgileri
        if chat:
            try:
                members = await app.get_chat_members_count(chat.id)
                text += f"\n👥 Üye Sayısı: {members}"
            except Exception as e:
                text += f"\n👥 Üye Sayısı: Alınamadı ({e})"

            try:
                link = f"https://t.me/{chat.username}" if chat.username else None
                if not link:
                    full_chat = await app.get_chat(chat.id)
                    link = full_chat.invite_link
                text += f"\n🔗 Grup Linki: {link if link else 'Yok veya alınamadı'}"
            except Exception as e:
                text += f"\n🔗 Grup Linki: Alınamadı ({e})"

        await app.send_message(LOG_GROUP_ID, f"🕒 `{timestamp}`\n\n{text}")

        with open("logs.txt", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}]\n{text}\n\n")

    except Exception as e:
        print(f"[HATA] Log gönderilemedi: {e}")


# ✅ Yeni üye geldi
@app.on_message(filters.new_chat_members)
async def on_new_member(client: Client, message: Message):
    bot_id = (await client.get_me()).id
    chat = message.chat

    for user in message.new_chat_members:
        ad = message.from_user.first_name if message.from_user else "Bilinmiyor"
        if user.id == bot_id:
            text = (
                f"✅ <b>Bot Gruba Eklendi</b>\n"
                f"👥 {chat.title} (`{chat.id}`)\n"
                f"➕ Ekleyen: {ad}"
            )
        else:
            text = (
                f"👤 <b>Kullanıcı Gruba Katıldı</b>\n"
                f"👤 {user.mention}\n🆔 `{user.id}`\n"
                f"👥 {chat.title} (`{chat.id}`)\n"
                f"➕ Ekleyen: {ad}"
            )
        await send_log(text, user.id, chat=chat)


# ✅ Üye ayrıldı
@app.on_message(filters.left_chat_member)
async def on_left_member(client: Client, message: Message):
    bot_id = (await client.get_me()).id
    user = message.left_chat_member
    chat = message.chat
    ad = message.from_user.first_name if message.from_user else "Bilinmiyor"

    if user.id == bot_id:
        text = (
            f"🚫 <b>Bot Gruptan Atıldı</b>\n"
            f"👥 {chat.title} (`{chat.id}`)\n"
            f"🚷 Atan: {ad}"
        )
    else:
        text = (
            f"🚷 <b>Kullanıcı Ayrıldı / Atıldı</b>\n"
            f"👤 {user.mention}\n🆔 `{user.id}`\n"
            f"👥 {chat.title} (`{chat.id}`)\n"
            f"👢 Atan: {ad}"
        )
    await send_log(text, user.id, chat=chat)


# ✅ Üyelik değişikliği (admin, ban, vs.)
@app.on_chat_member_updated()
async def on_chat_member_update(client: Client, update: ChatMemberUpdated):
    old = update.old_chat_member
    new = update.new_chat_member
    chat = update.chat

    # Güvenli kullanıcı bilgisi alımı
    try:
        user = new.user
        mention = user.mention if user else "Bilinmeyen"
        uid = user.id if user else None
    except Exception:
        mention = "Bilinmeyen"
        uid = None

    if old.status == new.status:
        return

    if new.status == ChatMemberStatus.ADMINISTRATOR:
        text = (
            f"🛡️ <b>Yönetici Yapıldı</b>\n"
            f"👤 {mention}\n🆔 `{uid}`\n"
            f"👥 {chat.title} (`{chat.id}`)"
        )
    elif old.status == ChatMemberStatus.ADMINISTRATOR and new.status == ChatMemberStatus.MEMBER:
        text = (
            f"⚠️ <b>Yönetici Yetkisi Alındı</b>\n"
            f"👤 {mention}\n🆔 `{uid}`\n"
            f"👥 {chat.title} (`{chat.id}`)"
        )
    elif new.status == ChatMemberStatus.BANNED:
        text = (
            f"⛔ <b>Kullanıcı Banlandı</b>\n"
            f"👤 {mention}\n🆔 `{uid}`\n"
            f"👥 {chat.title} (`{chat.id}`)"
        )
    elif old.status == ChatMemberStatus.BANNED and new.status == ChatMemberStatus.MEMBER:
        text = (
            f"🔓 <b>Ban Kaldırıldı</b>\n"
            f"👤 {mention}\n🆔 `{uid}`\n"
            f"👥 {chat.title} (`{chat.id}`)"
        )
    elif new.status == ChatMemberStatus.LEFT:
        text = (
            f"🚪 <b>Kullanıcı Ayrıldı</b>\n"
            f"👤 {mention}\n🆔 `{uid}`\n"
            f"👥 {chat.title} (`{chat.id}`)"
        )
    else:
        return

    await send_log(text, uid, chat=chat)
