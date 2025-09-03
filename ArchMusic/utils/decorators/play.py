from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import PLAYLIST_IMG_URL, PRIVATE_BOT_MODE, adminlist
from strings import get_string
from ArchMusic import YouTube, app
from ArchMusic.misc import SUDOERS
from ArchMusic.utils.database import (get_cmode, get_lang,
                                       get_playmode, get_playtype,
                                       is_active_chat,
                                       is_commanddelete_on,
                                       is_served_private_chat)
from ArchMusic.utils.database.memorydatabase import is_maintenance
from ArchMusic.utils.inline.playlist import botplaylist_markup
import time

# ----------------------
# play_logs stub (yer tutucu)
# ----------------------
async def play_logs(message, streamtype, duration=None, filesize=None, start_time=None, end_time=None, requester=None):
    """
    Test ve debug amaçlı basit play_logs fonksiyonu.
    Gerçek ArchMusic play_logs fonksiyonu yoksa bunu kullan.
    """
    await message.reply_text(
        f"Playing {streamtype}...\n"
        f"Duration: {duration}\n"
        f"Filesize: {filesize}\n"
        f"Start: {start_time}\n"
        f"End: {end_time}\n"
        f"Requested by: {requester}"
    )

# ----------------------
# PlayWrapper Dekoratörü
# ----------------------
def PlayWrapper(command):
    async def wrapper(client, message, *args, **kwargs):
        # Bakım modu kontrolü
        if await is_maintenance() is False:
            if message.from_user.id not in SUDOERS:
                return await message.reply_text("Bot bakımda. Lütfen bir süre bekleyin...")

        # Özel bot modu
        if PRIVATE_BOT_MODE == str(True):
            if not await is_served_private_chat(message.chat.id):
                await message.reply_text(
                    "**Özel Müzik Botu**\nYalnızca sahibinden gelen yetkili sohbetler için."
                )
                return await app.leave_chat(message.chat.id)

        # Komut otomatik silme
        if await is_commanddelete_on(message.chat.id):
            try: await message.delete()
            except: pass

        # Dil
        language = await get_lang(message.chat.id)
        _ = get_string(language)

        # Telegram medyası veya YouTube linki
        audio_telegram = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
        video_telegram = (message.reply_to_message.video or message.reply_to_message.document) if message.reply_to_message else None
        url = await YouTube.url(message)

        # Playlist veya stream kontrolü
        if audio_telegram is None and video_telegram is None and url is None:
            if len(message.command) < 2:
                buttons = botplaylist_markup(_)
                return await message.reply_photo(
                    photo=PLAYLIST_IMG_URL,
                    caption=_["playlist_1"],
                    reply_markup=InlineKeyboardMarkup(buttons),
                )

        # Kanal veya chat
        if message.command[0][0] == "c":
            chat_id = await get_cmode(message.chat.id)
            if chat_id is None: return await message.reply_text(_["setting_12"])
            try:
                chat = await app.get_chat(chat_id)
            except: return await message.reply_text(_["cplay_4"])
            channel = chat.title
        else:
            chat_id = message.chat.id
            channel = None

        # Yetki
        playmode = await get_playmode(message.chat.id)
        playty = await get_playtype(message.chat.id)
        if playty != "Everyone" and message.from_user.id not in SUDOERS:
            admins = adminlist.get(message.chat.id)
            if not admins or message.from_user.id not in admins:
                return await message.reply_text(_["play_4"])

        # Video kontrolü
        video = True if message.command[0][0] == "v" or "-v" in message.text else None
        fplay = True if message.command[0][-1] == "e" and await is_active_chat(chat_id) else None

        # Duration, FileSize, Start/End Time
        duration = None
        filesize = None
        start_time = time.time()
        end_time = None

        if url:  # YouTube
            info = await YouTube.get_info(url)
            duration = info.get("duration")
            filesize = info.get("filesize")
        elif audio_telegram:
            duration = audio_telegram.duration
            filesize = audio_telegram.file_size
        elif video_telegram:
            duration = getattr(video_telegram, "duration", None)
            filesize = video_telegram.file_size

        if duration:
            end_time = start_time + duration

        requester = message.from_user.id

        # Komutu çalıştır
        return await command(
            client,
            message,
            _,
            chat_id,
            video,
            channel,
            playmode,
            url,
            fplay,
            duration=duration,
            filesize=filesize,
            start_time=start_time,
            end_time=end_time,
            requester=requester,
            *args,
            **kwargs
        )

    return wrapper

# ----------------------
# play_command Fonksiyonu
# ----------------------
@PlayWrapper
async def play_command(client, message, _, chat_id, video, channel, playmode, url, fplay, *args, **kwargs):
    """
    Müzik oynatma komutu
    """
    streamtype = "video" if video else "audio"

    return await
