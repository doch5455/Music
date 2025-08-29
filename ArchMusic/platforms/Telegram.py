#
# Copyright (C) 2021-2023 by ArchBots@Github, < https://github.com/ArchBots >.
#
# This file is part of < https://github.com/ArchBots/ArchMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/ArchBots/ArchMusic/blob/master/LICENSE >
#
# All rights reserved.
#

import asyncio
import os
import time
import logging
from datetime import datetime, timedelta
from typing import Union
from collections import deque

from pyrogram.types import (InlineKeyboardButton,
                            InlineKeyboardMarkup, Voice)
from pyrogram import filters
from pyrogram.types import CallbackQuery

import config
from config import MUSIC_BOT_NAME, lyrical
from ArchMusic import app

from ..utils.formatters import (convert_bytes, get_readable_time,
                                seconds_to_min)

downloader = {}
download_queue = deque()
MAX_ACTIVE_DOWNLOADS = 10

logging.basicConfig(level=logging.INFO)


# 🔥 Kuyrukta bekleyen kullanıcıların gerçek zamanlı ETA güncellemesi
async def update_queue_messages():
    while True:
        active_downloads = list(downloader.values())
        total_active_eta = sum(active_downloads) if active_downloads else 0

        for pos, (_, message, mystic, fname) in enumerate(download_queue, start=1):
            # 🔥 Her kullanıcı için tahmini bekleme süresi
            est_wait = total_active_eta + sum(list(downloader.values())[:pos-1])
            est_wait_readable = get_readable_time(int(est_wait)) if est_wait else "0 sec"
            try:
                await mystic.edit_text(
                    f"⏳ İndirme kuyruğunda. Sıra: {pos}\nTahmini bekleme süresi: {est_wait_readable}"
                )
            except:
                pass
        await asyncio.sleep(10)

# 🔥 Kuyruk güncelleme başlat
asyncio.create_task(update_queue_messages())


class TeleAPI:
    def __init__(self):
        self.chars_limit = 4096
        self.sleep = config.TELEGRAM_DOWNLOAD_EDIT_SLEEP

    async def send_split_text(self, message, string):
        n = self.chars_limit
        out = [(string[i : i + n]) for i in range(0, len(string), n)]
        j = 0
        for x in out:
            if j <= 2:
                j += 1
                await message.reply_text(x)
        return True

    async def get_link(self, message):
        if message.chat.username:
            link = f"https://t.me/{message.chat.username}/{message.reply_to_message.id}"
        else:
            xf = str((message.chat.id))[4:]
            link = f"https://t.me/c/{xf}/{message.reply_to_message.id}"
        return link

    async def get_filename(
        self, file, audio: Union[bool, str] = None
    ):
        try:
            file_name = file.file_name
            if file_name is None:
                file_name = (
                    "Telegram Audio File"
                    if audio
                    else "Telegram Video File"
                )

        except Exception as e:
            logging.error(f"Filename error: {e}")
            file_name = (
                "Telegram Audio File"
                if audio
                else "Telegram Video File"
            )
        return file_name

    async def get_duration(self, file):
        try:
            dur = seconds_to_min(file.duration)
        except Exception as e:
            logging.error(f"Duration error: {e}")
            dur = "Unknown"
        return dur

    async def get_filepath(
        self,
        audio: Union[bool, str] = None,
        video: Union[bool, str] = None,
    ):
        if audio:
            try:
                file_name = (
                    audio.file_unique_id
                    + "."
                    + (
                        (audio.file_name.split(".")[-1])
                        if (not isinstance(audio, Voice))
                        else "ogg"
                    )
                )
            except Exception as e:
                logging.error(f"Audio filepath error: {e}")
                file_name = audio.file_unique_id + ".ogg"
            file_name = os.path.join(
                os.path.realpath("downloads"), file_name
            )
        if video:
            try:
                file_name = (
                    video.file_unique_id
                    + "."
                    + (video.file_name.split(".")[-1])
                )
            except Exception as e:
                logging.error(f"Video filepath error: {e}")
                file_name = video.file_unique_id + ".mp4"
            file_name = os.path.join(
                os.path.realpath("downloads"), file_name
            )
        return file_name

    async def download(self, _, message, mystic, fname):
        left_time = {}
        speed_counter = {}
        if os.path.exists(fname):
            return True

        # 🔥 Kuyruğa ekleme ve sıra gösterimi
        if len(downloader) >= MAX_ACTIVE_DOWNLOADS:
            queue_position = len(download_queue) + 1
            await mystic.edit_text(
                f"⏳ İndirme kuyruğa alındı. Sıra: {queue_position}\nTahmini bekleme süresi: hesaplanıyor..."
            )
            download_queue.append((_, message, mystic, fname))
            return False

        async def down_load():
            async def progress(current, total):
                if current == total:
                    return
                current_time = time.time()
                start_time = speed_counter.get(message.id)
                check_time = current_time - start_time
                upl = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="🚦 İndirmeyi Durdur",
                                callback_data="stop_downloading",
                            ),
                        ]
                    ]
                )
                if datetime.now() > left_time.get(message.id):
                    percentage = current * 100 / total
                    percentage = str(round(percentage, 2))
                    speed = current / check_time
                    eta = int((total - current) / speed)
                    downloader[message.id] = eta
                    eta = get_readable_time(eta)
                    if not eta:
                        eta = "0 sec"
                    total_size = convert_bytes(total)
                    completed_size = convert_bytes(current)
                    speed = convert_bytes(speed)
                    text = f"""
**{MUSIC_BOT_NAME} Telegram Medya İndiricisi**


**Total FileSize:** {total_size}
**Completed:** {completed_size} 
**Percentage:** {percentage[:5]}%

**Speed:** {speed}/s
**ETA:** {eta}"""
                    try:
                        await mystic.edit_text(text, reply_markup=upl)
                    except Exception as e:
                        logging.error(f"Progress update error: {e}")
                    left_time[
                        message.id
                    ] = datetime.now() + timedelta(seconds=self.sleep)

            speed_counter[message.id] = time.time()
            left_time[message.id] = datetime.now()

            try:
                await app.download_media(
                    message.reply_to_message,
                    file_name=fname,
                    progress=progress,
                )
                await mystic.edit_text("✅ Başarıyla İndirildi. Dosya şimdi işleniyor")

                # Dosya otomatik temizleme
                asyncio.get_event_loop().call_later(
                    60, lambda: os.remove(fname) if os.path.exists(fname) else None
                )

                downloader.pop(message.id)

                # Kuyruktaki bir sonraki indirmeyi başlat
                if download_queue:
                    next_task = download_queue.popleft()
                    asyncio.create_task(self.download(*next_task))

            except Exception as e:
                logging.error(f"Download error: {e}")
                await mystic.edit_text(_["tg_2"])

        task = asyncio.create_task(down_load())
        lyrical[mystic.id] = task
        await task
        downloaded = downloader.get(message.id)
        if downloaded:
            downloader.pop(message.id)
            return False
        verify = lyrical.get(mystic.id)
        if not verify:
            return False
        lyrical.pop(mystic.id)
        return True


@app.on_callback_query(filters.regex("stop_downloading"))
async def stop_downloading(_, query: CallbackQuery):
    task = lyrical.get(query.message.id)
    if task:
        task.cancel()
        lyrical.pop(query.message.id, None)
        await query.answer("⏹️ İndirme iptal edildi!", show_alert=True)
        await query.message.edit_text("❌ İndirme kullanıcı tarafından iptal edildi.")
    else:
        await query.answer("⚠️ Aktif bir indirme yok!", show_alert=True)
