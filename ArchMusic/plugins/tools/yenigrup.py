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


# 📝 Log mesajı gönder ve dosyaya kaydet
async def send_log(text: str, user_id: int = None, chat=None):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Profil fotoğrafı indir (kullanıcı id'si varsa)
        if user_id:
            await download_user_photo(user_id)

        # Gruba mesaj at
        await app.send_message(LOG_GROUP_ID, f"🕒 `{timestamp}`\n\n{text}")

        # Dosyaya yaz
        with open("logs.txt", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}]\n{text}\n\n")
    except Exception as e:
        print(f"[HATA] Log gönderilemedi: {e}")


# ✅ BOT GRUBA EKLENDİ – KULLANICI EKLENDİ
@app.on_message(filters.new_chat_members)
async def on_new_member(client: Client, message: Message):
    bot_id = (await client.get_me()).id
    chat = message.chat

    try:
        members = await app.get_chat_members_count(chat.id)
    except Exception:
        members = "Bilinmiyor"

    # Grup linki alma
    link = None
    try:
        if chat.username:
            link = f"https://t.me/{chat.username}"
        else:
            full_chat = await app.get_chat(chat.id)
            link = full_chat.invite_link
    except Exception:
        pass

    for user in message.new_chat_members:
        ad = message.from_user.first_name if message.from_user else "Bilinmiyor"
        if user.id == bot_id:
            text = (
                f"✅ <b>Bot Gruba Eklendi</b>\n"
                f"👥 {chat.title} (`{chat.id}`)\n"
                f"👥 Üye Sayısı: {members}\n"
                f"🔗 Grup Linki: {link if link else 'Bilinmiyor'}\n"
                f"➕ Ekleyen: {ad}"
            )
        else:
            text = (
                f"👤 <b>Kullanıcı Gruba Katıldı</b>\n"
                f"👤 {user.mention}\n🆔 `{user.id}`\n"
                f"👥 {chat.title} (`{chat.id}`)\n"
                f"👥 Üye Sayısı: {members}\n"
                f"🔗 Grup Linki: {link if link else 'Bilinmiyor'}\n"
                f"➕ Ekleyen: {ad}"
            )
        await send_log(text, user.id)


# ✅ BOT / KULLANICI AYRILDI
@app.on_message(filters.left_chat_member)
async def on_left_member(client: Client, message: Message):
    bot_id = (await client.get_me()).id
    user = message.left_chat_member
    chat = message.chat

    try:
        members = await app.get_chat_members_count(chat.id)
    except Exception:
        members = "Bilinmiyor"

    # Grup linki alma
    link = None
    try:
        if chat.username:
            link = f"https://t.me/{chat.username}"
        else:
            full_chat = await app.get_chat(chat.id)
            link = full_chat.invite_link
    except Exception:
        pass

    ad = message.from_user.first_name if message.from_user else "Bilinmiyor"

    if user.id == bot_id:
        text = (
            f"🚫 <b>Bot Gruptan Atıldı</b>\n"
            f"👥 {chat.title} (`{chat.id}`)\n"
            f"👥 Üye Sayısı: {members}\n"
            f"🔗 Grup Linki: {link if link else 'Bilinmiyor'}\n"
            f"🚷 Atan: {ad}"
        )
    else:
        text = (
            f"🚷 <b>Kullanıcı Ayrıldı / Atıldı</b>\n"
            f"👤 {user.mention}\n🆔 `{user.id}`\n"
            f"👥 {chat.title} (`{chat.id}`)\n"
            f"👥 Üye Sayısı: {members}\n"
            f"🔗 Grup Linki: {link if link else 'Bilinmiyor'}\n"
            f"👢 Atan: {ad}"
        )
    await send_log(text, user.id)


# ✅ TÜM ÜYELİK DEĞİŞİKLİKLERİ
@app.on_chat_member_updated()
async def on_chat_member_update(client: Client, update: ChatMemberUpdated):
    old = update.old_chat_member
    new = update.new_chat_member
    chat = update.chat

    if not old or not new or not chat:
        return

    old_status = getattr(old, "status", None)
    new_status = getattr(new, "status", None)
    user = getattr(new, "user", None)

    if not user or old_status == new_status:
        return

    bot_id = (await client.get_me()).id
    mention = user.mention or user.first_name or "Bilinmiyor"
    uid = user.id if user else None

    # Bot banlandıysa özel log at, hata verme
    if uid == bot_id and new_status == ChatMemberStatus.BANNED:
        text = (
            f"⛔ <b>Bot Gruptan Banlandı</b>\n"
            f"👥 {chat.title} (`{chat.id}`)"
        )
        try:
            if chat.username:
                link = f"https://t.me/{chat.username}"
            else:
                full_chat = await app.get_chat(chat.id)
                link = full_chat.invite_link
            if link:
                text += f"\n🔗 Grup Linki: {link}"
        except Exception:
            pass

        await send_log(text, uid, chat=chat)
        return

    # Diğer üyelik değişiklikleri
    if new_status == ChatMemberStatus.ADMINISTRATOR:
        text = (
            f"🛡️ <b>Yönetici Yapıldı</b>\n"
            f"👤 {mention}\n🆔 `{uid}`\n"
            f"👥 {chat.title} (`{chat.id}`)"
        )
    elif old_status == ChatMemberStatus.ADMINISTRATOR and new_status == ChatMemberStatus.MEMBER:
        text = (
            f"⚠️ <b>Yönetici Yetkisi Alındı</b>\n"
            f"👤 {mention}\n🆔 `{uid}`\n"
            f"👥 {chat.title} (`{chat.id}`)"
        )
    elif new_status == ChatMemberStatus.BANNED:
        text = (
            f"⛔ <b>Kullanıcı Banlandı</b>\n"
            f"👤 {mention}\n🆔 `{uid}`\n"
            f"👥 {chat.title} (`{chat.id}`)"
        )
    elif old_status == ChatMemberStatus.BANNED and new_status == ChatMemberStatus.MEMBER:
        text = (
            f"🔓 <b>Ban Kaldırıldı</b>\n"
            f"👤 {mention}\n🆔 `{uid}`\n"
            f"👥 {chat.title} (`{chat.id}`)"
        )
    elif new_status == ChatMemberStatus.LEFT:
        text = (
            f"🚪 <b>Kullanıcı Ayrıldı</b>\n"
            f"👤 {mention}\n🆔 `{uid}`\n"
            f"👥 {chat.title} (`{chat.id}`)"
        )
    else:
        return

    try:
        members = await app.get_chat_members_count(chat.id)
        text += f"\n👥 Üye Sayısı: {members}"
    except Exception:
        pass

    try:
        if chat.username:
            link = f"https://t.me/{chat.username}"
        else:
            full_chat = await app.get_chat(chat.id)
            link = full_chat.invite_link
        if link:
            text += f"\n🔗 Grup Linki: {link}"
    except Exception:
        pass

    await send_log(text, uid, chat=chat)
