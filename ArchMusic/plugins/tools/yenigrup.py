# group_events.py

from pyrogram import Client, filters
from pyrogram.types import Message, ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatMemberStatus
from config import LOG_GROUP_ID
from ArchMusic import app


async def new_message(chat_id: int, message: str, reply_markup=None):
    await app.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)


# 1. Bot veya kullanıcı gruba eklendi
@app.on_message(filters.new_chat_members)
async def on_new_member(client: Client, message: Message):
    bot_id = (await client.get_me()).id
    for user in message.new_chat_members:
        added_by = message.from_user.first_name if message.from_user else "Bilinmiyor"
        chat_id = message.chat.id
        title = message.chat.title
        chat_link = f"@{message.chat.username}" if message.chat.username else "Yok"

        if user.id == bot_id:
            text = (
                f"<u>#**Bot Gruba Eklendi**</u>\n\n"
                f"**Grup Adı:** {title}\n"
                f"**Grup ID:** `{chat_id}`\n"
                f"**Grup Linki:** {chat_link}\n"
                f"**Ekleyen:** {added_by}"
            )
        else:
            text = (
                f"<u>#**Kullanıcı Eklendi**</u>\n\n"
                f"**Adı:** {user.mention}\n"
                f"**ID:** `{user.id}`\n"
                f"**Grup:** {title}\n"
                f"**Ekleyen:** {added_by}"
            )

        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(added_by, user_id=message.from_user.id)]] if message.from_user else []
        )

        await new_message(LOG_GROUP_ID, text, reply_markup)


# 2. Bot veya kullanıcı gruptan çıkarıldı
@app.on_message(filters.left_chat_member)
async def on_left_member(client: Client, message: Message):
    bot_id = (await client.get_me()).id
    user = message.left_chat_member
    remover = message.from_user.first_name if message.from_user else "Bilinmiyor"
    title = message.chat.title
    chat_id = message.chat.id

    if user.id == bot_id:
        text = (
            f"<u>#**Bot Gruptan Atıldı**</u>\n\n"
            f"**Grup Adı:** {title}\n"
            f"**Grup ID:** `{chat_id}`\n"
            f"**Atan Kişi:** {remover}"
        )
    else:
        text = (
            f"<u>#**Kullanıcı Çıkarıldı**</u>\n\n"
            f"**Adı:** {user.mention}\n"
            f"**ID:** `{user.id}`\n"
            f"**Grup:** {title}\n"
            f"**Çıkaran:** {remover}"
        )

    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton(remover, user_id=message.from_user.id)]] if message.from_user else []
    )

    await new_message(LOG_GROUP_ID, text, reply_markup)


# 3. Üyelik, ban ve yetki değişikliklerini algıla
@app.on_chat_member_updated()
async def on_chat_member_update(client: Client, update: ChatMemberUpdated):
    old = update.old_chat_member
    new = update.new_chat_member
    user = new.user
    chat = update.chat
    actor = update.from_user.first_name if update.from_user else "Bilinmiyor"
    actor_id = update.from_user.id if update.from_user else None

    action = None

    # Bot'a yapılan işlem
    if user.is_self:
        if new.status == ChatMemberStatus.KICKED:
            action = "Bot gruptan **banlandı**"
        elif old.status == ChatMemberStatus.KICKED and new.status == ChatMemberStatus.MEMBER:
            action = "Bot gruba **geri alındı** (ban kaldırıldı)"

    else:
        # Kullanıcı banlandı veya ban kaldırıldı
        if new.status == ChatMemberStatus.KICKED:
            action = f"{user.mention} gruptan **banlandı**"
        elif old.status == ChatMemberStatus.KICKED and new.status == ChatMemberStatus.MEMBER:
            action = f"{user.mention} gruba **geri alındı** (ban kaldırıldı)"

        # Yönetici yapıldı / alındı
        elif old.status == ChatMemberStatus.MEMBER and new.status == ChatMemberStatus.ADMINISTRATOR:
            action = f"{user.mention} grubun **yöneticisi yapıldı**"
        elif old.status == ChatMemberStatus.ADMINISTRATOR and new.status == ChatMemberStatus.MEMBER:
            action = f"{user.mention} **yöneticilikten alındı**"

    if not action:
        return

    text = (
        f"<u>#**Grup Üyelik Güncellemesi**</u>\n\n"
        f"**Grup:** {chat.title}\n"
        f"**Kullanıcı:** {user.mention} (`{user.id}`)\n"
        f"**İşlem:** {action}\n"
        f"**İşlemi Yapan:** {actor}"
    )

    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton(actor, user_id=actor_id)]] if actor_id else []
    )

    await new_message(LOG_GROUP_ID, text, reply_markup)
