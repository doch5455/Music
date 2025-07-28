from pyrogram import Client, filters
from pyrogram.types import Message, ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatMemberStatus
from config import LOG_GROUP_ID
from ArchMusic import app


async def send_log(text: str, reply_markup=None):
    try:
        await app.send_message(chat_id=LOG_GROUP_ID, text=text, reply_markup=reply_markup)
    except Exception as e:
        print(f"[HATA] Log grubuna mesaj gönderilemedi:\n{e}")


# ✅ Yeni üye eklendiğinde
@app.on_message(filters.new_chat_members)
async def on_new_member(client: Client, message: Message):
    bot_id = (await client.get_me()).id
    for user in message.new_chat_members:
        ad = message.from_user.first_name if message.from_user else "Bilinmiyor"
        chat = message.chat
        chat_link = f"@{chat.username}" if chat.username else "Yok"

        if user.id == bot_id:
            text = (
                f"<u>#✅ **Bot Gruba Eklendi**</u>\n\n"
                f"**Grup:** {chat.title}\n"
                f"**Grup ID:** `{chat.id}`\n"
                f"**Link:** {chat_link}\n"
                f"**Ekleyen:** {ad}"
            )
        else:
            text = (
                f"<u>#👤 **Kullanıcı Eklendi**</u>\n\n"
                f"**Adı:** {user.mention}\n"
                f"**ID:** `{user.id}`\n"
                f"**Grup:** {chat.title}\n"
                f"**Ekleyen:** {ad}"
            )

        markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(ad, user_id=message.from_user.id)]] if message.from_user else []
        )

        await send_log(text, markup)


# ✅ Bot veya kullanıcı ayrıldığında
@app.on_message(filters.left_chat_member)
async def on_left_member(client: Client, message: Message):
    bot_id = (await client.get_me()).id
    user = message.left_chat_member
    ad = message.from_user.first_name if message.from_user else "Bilinmiyor"
    chat = message.chat

    if user.id == bot_id:
        text = (
            f"<u>#🚫 **Bot Gruptan Atıldı**</u>\n\n"
            f"**Grup:** {chat.title}\n"
            f"**Grup ID:** `{chat.id}`\n"
            f"**Atan:** {ad}"
        )
    else:
        text = (
            f"<u>#🚷 **Kullanıcı Çıkarıldı**</u>\n\n"
            f"**Adı:** {user.mention}\n"
            f"**ID:** `{user.id}`\n"
            f"**Grup:** {chat.title}\n"
            f"**Çıkaran:** {ad}"
        )

    markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton(ad, user_id=message.from_user.id)]] if message.from_user else []
    )

    await send_log(text, markup)


# ✅ Üyelik, ban, yönetici değişiklikleri
@app.on_chat_member_updated()
async def on_chat_member_update(client: Client, update: ChatMemberUpdated):
    old = update.old_chat_member
    new = update.new_chat_member
    user = new.user
    chat = update.chat

    if old.status != new.status:
        if new.status == ChatMemberStatus.ADMINISTRATOR:
            text = (
                f"<u>#🛡️ **Yönetici Yapıldı**</u>\n\n"
                f"**Kullanıcı:** {user.mention}\n"
                f"**ID:** `{user.id}`\n"
                f"**Grup:** {chat.title}\n"
                f"**Grup ID:** `{chat.id}`"
            )
        elif old.status == ChatMemberStatus.ADMINISTRATOR and new.status == ChatMemberStatus.MEMBER:
            text = (
                f"<u>#⚠️ **Yönetici Alındı**</u>\n\n"
                f"**Kullanıcı:** {user.mention}\n"
                f"**ID:** `{user.id}`\n"
                f"**Grup:** {chat.title}\n"
                f"**Grup ID:** `{chat.id}`"
            )
        elif new.status == ChatMemberStatus.BANNED:
            text = (
                f"<u>#⛔️ **Kullanıcı Banlandı**</u>\n\n"
                f"**Kullanıcı:** {user.mention}\n"
                f"**ID:** `{user.id}`\n"
                f"**Grup:** {chat.title}\n"
                f"**Grup ID:** `{chat.id}`"
            )
        elif old.status == ChatMemberStatus.BANNED and new.status == ChatMemberStatus.MEMBER:
            text = (
                f"<u>#🔓 **Kullanıcı Ban Kaldırıldı**</u>\n\n"
                f"**Kullanıcı:** {user.mention}\n"
                f"**ID:** `{user.id}`\n"
                f"**Grup:** {chat.title}\n"
                f"**Grup ID:** `{chat.id}`"
            )
        elif new.status == ChatMemberStatus.LEFT:
            text = (
                f"<u>#🚪 **Kullanıcı Ayrıldı veya Atıldı**</u>\n\n"
                f"**Kullanıcı:** {user.mention}\n"
                f"**ID:** `{user.id}`\n"
                f"**Grup:** {chat.title}\n"
                f"**Grup ID:** `{chat.id}`"
            )
        else:
            return

        await send_log(text)
