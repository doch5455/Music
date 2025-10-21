import os
from random import randint
from typing import Union

from pyrogram.types import InlineKeyboardMarkup

import config
from ArchMusic import Carbon, YouTube, app
from ArchMusic.core.call import ArchMusic
from ArchMusic.misc import db
from ArchMusic.utils.database import (
    add_active_chat,
    add_active_video_chat,
    is_active_chat,
    is_video_allowed,
)
from ArchMusic.utils.exceptions import AssistantErr
from ArchMusic.utils.inline.play import stream_markup
from ArchMusic.utils.inline.playlist import close_markup
from ArchMusic.utils.pastebin import ArchMusicbin
from ArchMusic.utils.stream.queue import put_queue, put_queue_index


async def stream(
    _,
    mystic,
    user_id,
    result,
    chat_id,
    user_name,
    original_chat_id,
    video: Union[bool, str] = None,
    streamtype: Union[bool, str] = None,
    spotify: Union[bool, str] = None,
    forceplay: Union[bool, str] = None,
):
    if not result:
        return
    if video:
        if not await is_video_allowed(chat_id):
            raise AssistantErr(_["play_7"])
    if forceplay:
        await ArchMusic.force_stop_stream(chat_id)

    # PLAYLIST STREAM --------------------------------------------------------
    if streamtype == "playlist":
        msg = f"{_['playlist_16']}\n\n"
        count = 0
        for search in result:
            if int(count) == config.PLAYLIST_FETCH_LIMIT:
                continue
            try:
                (
                    title,
                    duration_min,
                    duration_sec,
                    thumbnail,
                    vidid,
                ) = await YouTube.details(search, False if spotify else True)
            except:
                continue

            if str(duration_min) == "None" or duration_sec > config.DURATION_LIMIT:
                continue

            n, stream_url = await YouTube.video(vidid, True)
            if n == 0:
                continue

            if await is_active_chat(chat_id):
                await put_queue(
                    chat_id,
                    original_chat_id,
                    stream_url,
                    title,
                    duration_min,
                    user_name,
                    vidid,
                    user_id,
                    "video" if video else "audio",
                )
                position = len(db.get(chat_id)) - 1
                count += 1
                msg += f"{count}- {title[:70]}\n"
                msg += f"{_['playlist_17']} {position}\n\n"
            else:
                if not forceplay:
                    db[chat_id] = []
                status = True if video else None
                await ArchMusic.join_call(
                    chat_id, original_chat_id, stream_url, video=status
                )
                await put_queue(
                    chat_id,
                    original_chat_id,
                    stream_url,
                    title,
                    duration_min,
                    user_name,
                    vidid,
                    user_id,
                    "video" if video else "audio",
                    forceplay=forceplay,
                )
                button = stream_markup(_, vidid, chat_id)
                run = await app.send_message(
                    original_chat_id,
                    text=_["stream_1"].format(
                        title,
                        f"https://t.me/{app.username}?start=info_{vidid}",
                        duration_min,
                        user_name,
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "stream"

        if count == 0:
            return
        else:
            link = await ArchMusicbin(msg)
            lines = msg.count("\n")
            car = os.linesep.join(msg.split(os.linesep)[:17])
            upl = close_markup(_)
            return await app.send_message(
                original_chat_id,
                text=_["playlist_18"].format(link, position),
                reply_markup=upl,
            )

    # YOUTUBE STREAM --------------------------------------------------------
    elif streamtype == "youtube":
        link = result["link"]
        vidid = result["vidid"]
        title = (result["title"]).title()
        duration_min = result["duration_min"]
        status = True if video else None

        n, stream_url = await YouTube.video(vidid, True)
        if n == 0:
            raise AssistantErr(_["str_3"])

        if await is_active_chat(chat_id):
            await put_queue(
                chat_id,
                original_chat_id,
                stream_url,
                title,
                duration_min,
                user_name,
                vidid,
                user_id,
                "video" if video else "audio",
            )
            position = len(db.get(chat_id)) - 1
            await app.send_message(
                original_chat_id,
                _["queue_4"].format(position, title, duration_min, user_name),
            )
        else:
            if not forceplay:
                db[chat_id] = []
            await ArchMusic.join_call(
                chat_id, original_chat_id, stream_url, video=status
            )
            await put_queue(
                chat_id,
                original_chat_id,
                stream_url,
                title,
                duration_min,
                user_name,
                vidid,
                user_id,
                "video" if video else "audio",
                forceplay=forceplay,
            )
            button = stream_markup(_, vidid, chat_id)
            run = await app.send_message(
                original_chat_id,
                text=_["stream_1"].format(
                    title,
                    f"https://t.me/{app.username}?start=info_{vidid}",
                    duration_min,
                    user_name,
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "stream"

    # SOUNDCLOUD STREAM -----------------------------------------------------
    elif streamtype == "soundcloud":
        file_path = result["filepath"]
        title = result["title"]
        duration_min = result["duration_min"]

        if await is_active_chat(chat_id):
            await put_queue(
                chat_id,
                original_chat_id,
                file_path,
                title,
                duration_min,
                user_name,
                streamtype,
                user_id,
                "audio",
            )
            position = len(db.get(chat_id)) - 1
            await app.send_message(
                original_chat_id,
                _["queue_4"].format(position, title, duration_min, user_name),
            )
        else:
            if not forceplay:
                db[chat_id] = []
            await ArchMusic.join_call(chat_id, original_chat_id, file_path, video=None)
            await put_queue(
                chat_id,
                original_chat_id,
                file_path,
                title,
                duration_min,
                user_name,
                streamtype,
                user_id,
                "audio",
                forceplay=forceplay,
            )
            button = stream_markup(_, "soundcloud", chat_id)
            run = await app.send_message(
                original_chat_id,
                text=_["stream_3"].format(title, duration_min, user_name),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "stream"

    # TELEGRAM STREAM -------------------------------------------------------
    elif streamtype == "telegram":
        file_path = result["path"]
        link = result["link"]
        title = (result["title"]).title()
        duration_min = result["dur"]
        status = True if video else None

        if await is_active_chat(chat_id):
            await put_queue(
                chat_id,
                original_chat_id,
                file_path,
                title,
                duration_min,
                user_name,
                streamtype,
                user_id,
                "video" if video else "audio",
            )
            position = len(db.get(chat_id)) - 1
            await app.send_message(
                original_chat_id,
                _["queue_4"].format(position, title, duration_min, user_name),
            )
        else:
            if not forceplay:
                db[chat_id] = []
            await ArchMusic.join_call(chat_id, original_chat_id, file_path, video=status)
            await put_queue(
                chat_id,
                original_chat_id,
                file_path,
                title,
                duration_min,
                user_name,
                streamtype,
                user_id,
                "video" if video else "audio",
                forceplay=forceplay,
            )
            if video:
                await add_active_video_chat(chat_id)

            button = stream_markup(_, "telegram", chat_id)
            run = await app.send_message(
                original_chat_id,
                text=_["stream_4"].format(title, link, duration_min, user_name),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "stream"

    # INDEX veya M3U8 STREAM ------------------------------------------------
    elif streamtype == "index":
        link = result
        title = "Index or M3u8 Link"
        duration_min = "URL stream"

        if await is_active_chat(chat_id):
            await put_queue_index(
                chat_id,
                original_chat_id,
                "index_url",
                title,
                duration_min,
                user_name,
                link,
                "video" if video else "audio",
            )
            position = len(db.get(chat_id)) - 1
            await mystic.edit_text(
                _["queue_4"].format(position, title, duration_min, user_name)
            )
        else:
            if not forceplay:
                db[chat_id] = []
            await ArchMusic.join_call(
                chat_id, original_chat_id, link, video=True if video else None
            )
            await put_queue_index(
                chat_id,
                original_chat_id,
                "index_url",
                title,
                duration_min,
                user_name,
                link,
                "video" if video else "audio",
                forceplay=forceplay,
            )
            button = stream_markup(_, "index", chat_id)
            run = await app.send_message(
                original_chat_id,
                text=_["stream_2"].format(title, link, duration_min, user_name),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "stream"
            await mystic.delete()
