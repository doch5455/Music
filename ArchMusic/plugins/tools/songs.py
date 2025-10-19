import os
import re

import yt_dlp
from pykeyboard import InlineKeyboard
from pyrogram import filters
from pyrogram.enums import ChatAction
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaAudio,
    InputMediaVideo,
    Message,
)

from config import (
    BANNED_USERS,
    SONG_DOWNLOAD_DURATION,
    SONG_DOWNLOAD_DURATION_LIMIT,
)
from strings import get_command
from ArchMusic import YouTube, app
from ArchMusic.utils.decorators.language import language, languageCB
from ArchMusic.utils.formatters import convert_bytes
from ArchMusic.utils.inline.song import song_markup


# Komut tanımı
SONG_COMMAND = get_command("SONG_COMMAND")

# ✅ Cookies yolu
COOKIES_PATH = "cookies.txt"


@app.on_message(
    filters.command(SONG_COMMAND)
    & filters.private
    & ~BANNED_USERS
)
@language
async def song_commad_private(client, message: Message, _):
    await message.delete()
    url = await YouTube.url(message)
    if url:
        if not await YouTube.exists(url):
            return await message.reply_text(_["song_5"])
        mystic = await message.reply_text(_["play_1"])
        (
            title,
            duration_min,
            duration_sec,
            thumbnail,
            vidid,
        ) = await YouTube.details(url)
        if str(duration_min) == "None":
            return await mystic.edit_text(_["song_3"])
        if int(duration_sec) > SONG_DOWNLOAD_DURATION_LIMIT:
            return await mystic.edit_text(
                _["play_4"].format(
                    SONG_DOWNLOAD_DURATION, duration_min
                )
            )
        buttons = song_markup(_, vidid)
        await mystic.delete()
        return await message.reply_photo(
            thumbnail,
            caption=_["song_4"].format(title),
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        if len(message.command) < 2:
            return await message.reply_text(_["song_2"])
    mystic = await message.reply_text(_["play_1"])
    query = message.text.split(None, 1)[1]
    try:
        (
            title,
            duration_min,
            duration_sec,
            thumbnail,
            vidid,
        ) = await YouTube.details(query)
    except:
        return await mystic.edit_text(_["play_3"])
    if str(duration_min) == "None":
        return await mystic.edit_text(_["song_3"])
    if int(duration_sec) > SONG_DOWNLOAD_DURATION_LIMIT:
        return await mystic.edit_text(
            _["play_6"].format(SONG_DOWNLOAD_DURATION, duration_min)
        )
    buttons = song_markup(_, vidid)
    await mystic.delete()
    return await message.reply_photo(
        thumbnail,
        caption=_["song_4"].format(title),
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(
    filters.regex(pattern=r"song_back") & ~BANNED_USERS
)
@languageCB
async def songs_back_helper(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    stype, vidid = callback_request.split("|")
    buttons = song_markup(_, vidid)
    return await CallbackQuery.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(
    filters.regex(pattern=r"song_helper") & ~BANNED_USERS
)
@languageCB
async def song_helper_cb(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    stype, vidid = callback_request.split("|")
    try:
        await CallbackQuery.answer(_["song_6"], show_alert=True)
    except:
        pass

    # ✅ Cookies kullanarak biçim listesi al
    ytdl_opts = {
        "quiet": True,
        "cookiefile": COOKIES_PATH if os.path.exists(COOKIES_PATH) else None,
        "skip_download": True,
    }

    try:
        with yt_dlp.YoutubeDL(ytdl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={vidid}", download=False)
            formats_available = info.get("formats", [])
    except Exception as e:
        print(f"Format fetch error: {e}")
        return await CallbackQuery.edit_message_text(_["song_7"])

    keyboard = InlineKeyboard()
    if stype == "audio":
        done = []
        for x in formats_available:
            if "audio" in x.get("format", ""):
                form = x.get("format_note", "Unknown").title()
                if form in done:
                    continue
                done.append(form)
                sz = convert_bytes(x.get("filesize")) if x.get("filesize") else "Unknown size"
                keyboard.row(
                    InlineKeyboardButton(
                        text=f"{form} Audio = {sz}",
                        callback_data=f"song_download {stype}|{x['format_id']}|{vidid}",
                    ),
                )
    else:
        # ✅ Burada filesize kontrolü kaldırıldı
        filtered_formats = [x for x in formats_available if "video" in x.get("format", "")]
        if not filtered_formats:
            return await CallbackQuery.edit_message_text(
                "Video için kullanılabilir biçimler alınamadı. Lütfen başka bir parça deneyin."
            )
        for x in filtered_formats:
            sz = convert_bytes(x.get("filesize")) if x.get("filesize") else "Unknown size"
            quality = x.get("format_note") or f"{x.get('height', 'Unknown')}p"
            text = f"{quality} = {sz}"
            keyboard.row(
                InlineKeyboardButton(
                    text=text,
                    callback_data=f"song_download {stype}|{x['format_id']}|{vidid}",
                )
            )

    keyboard.row(
        InlineKeyboardButton(
            text=_["BACK_BUTTON"],
            callback_data=f"song_back {stype}|{vidid}",
        ),
        InlineKeyboardButton(
            text=_["CLOSE_BUTTON"], callback_data=f"close"
        ),
    )
    return await CallbackQuery.edit_message_reply_markup(reply_markup=keyboard)


@app.on_callback_query(
    filters.regex(pattern=r"song_download") & ~BANNED_USERS
)
@languageCB
async def song_download_cb(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer("Downloading")
    except:
        pass
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    stype, format_id, vidid = callback_request.split("|")
    mystic = await CallbackQuery.edit_message_text(_["song_8"])
    yturl = f"https://www.youtube.com/watch?v={vidid}"

    # ✅ Cookies destekli yt_dlp ayarları
    ytdl_opts = {
        "quiet": True,
        "cookiefile": COOKIES_PATH if os.path.exists(COOKIES_PATH) else None,
    }

    with yt_dlp.YoutubeDL(ytdl_opts) as ytdl:
        x = ytdl.extract_info(yturl, download=False)

    title = (x["title"]).title()
    title = re.sub(r"\W+", " ", title)
    thumb_image_path = await CallbackQuery.message.download()
    duration = x["duration"]

    if stype == "video":
        width = CallbackQuery.message.photo.width
        height = CallbackQuery.message.photo.height
        try:
            file_path = await YouTube.download(
                yturl,
                mystic,
                songvideo=True,
                format_id=format_id,
                title=title,
                cookies=COOKIES_PATH if os.path.exists(COOKIES_PATH) else None,
            )
        except Exception as e:
            return await mystic.edit_text(_["song_9"].format(e))
        med = InputMediaVideo(
            media=file_path,
            duration=duration,
            width=width,
            height=height,
            thumb=thumb_image_path,
            caption=title,
            supports_streaming=True,
        )
        await mystic.edit_text(_["song_11"])
        await app.send_chat_action(
            chat_id=CallbackQuery.message.chat.id,
            action=ChatAction.UPLOAD_VIDEO,
        )
        try:
            await CallbackQuery.edit_message_media(media=med)
        except Exception as e:
            print(e)
            return await mystic.edit_text(_["song_10"])
        os.remove(file_path)

    elif stype == "audio":
        try:
            filename = await YouTube.download(
                yturl,
                mystic,
                songaudio=True,
                format_id=format_id,
                title=title,
                cookies=COOKIES_PATH if os.path.exists(COOKIES_PATH) else None,
            )
        except Exception as e:
            return await mystic.edit_text(_["song_9"].format(e))
        med = InputMediaAudio(
            media=filename,
            caption=title,
            thumb=thumb_image_path,
            title=title,
            performer=x.get("uploader", "Unknown Artist"),
        )
        await mystic.edit_text(_["song_11"])
        await app.send_chat_action(
            chat_id=CallbackQuery.message.chat.id,
            action=ChatAction.UPLOAD_AUDIO,
        )
        try:
            await CallbackQuery.edit_message_media(media=med)
        except Exception as e:
            print(e)
            return await mystic.edit_text(_["song_10"])
        os.remove(filename)
