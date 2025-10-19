# Copyright (C) 2021-2023 by ArchBots@Github.
# This file is part of ArchMusic Project.
# Released under GNU v3.0 License.

import asyncio
from pyrogram import filters
from pyrogram.enums import ChatType, ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython.__future__ import VideosSearch

import config
from config import BANNED_USERS
from config.config import OWNER_ID
from strings import get_command, get_string
from ArchMusic import Telegram, YouTube, app
from ArchMusic.misc import SUDOERS
from ArchMusic.plugins.play.playlist import del_plist_msg
from ArchMusic.plugins.sudo.sudoers import sudoers_list
from ArchMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_assistant,
    get_lang,
    get_userss,
    is_on_off,
    is_served_private_chat,
)
from ArchMusic.utils.decorators.language import LanguageStart
from ArchMusic.utils.inline import help_pannel, private_panel, start_pannel

loop = asyncio.get_running_loop()


# ===================== SHOW LOADING ANIMASYONU =====================
async def show_loading(message: Message):
    frames = [
        "⚡🤖 Başlatılıyor… Enerji çekiliyor…",
        "🔋💻 Modüller yükleniyor… Sistem senkronize ediliyor…",
        "🛠️⚙️ Robot çekirdeği optimize ediliyor…",
        "💫🔌 Veriler akıyor… Bağlantılar kuruluyor…",
        "⚡🤖 Hazır! Sisteme giriş tamamlandı! ✅",
    ]

    loading = await message.reply_text(frames[0])
    for frame in frames[1:]:
        await asyncio.sleep(0.8)
        await loading.edit(frame)
    
    pulse_frames = [
        "⚡🤖 Hazır! ✅ 🔋💻",
        "🔌⚡🤖 Hazır! ✅ 🛠️⚙️",
        "💫🔋 Hazır! ✅ ⚡🤖"
    ]
    for _ in range(2):
        for frame in pulse_frames:
            await asyncio.sleep(0.5)
            await loading.edit(frame)
    
    return loading


# ===================== START KOMUTU PARAMETRELERİ =====================
async def handle_start_params(client, message: Message, param: str, _):
    if param.startswith("help"):
        return await message.reply_text(_["help_1"], reply_markup=help_pannel(_))
    if param.startswith("song"):
        return await message.reply_text(_["song_2"])
    if param.startswith("sta"):
        return await show_user_stats(message, _)
    if param.startswith("sud"):
        await sudoers_list(client=client, message=message, _=_)
        if await is_on_off(config.LOG):
            await app.send_message(
                config.LOG_GROUP_ID,
                f"{message.from_user.mention} az önce **SUDO LİSTESİNİ** kontrol etti."
            )
    if param.startswith("lyr"):
        query = param.replace("lyrics_", "", 1)
        lyrics = config.lyrical.get(query)
        return await Telegram.send_split_text(message, lyrics or "Şarkı sözleri bulunamadı.")
    if param.startswith("del"):
        return await del_plist_msg(client=client, message=message, _=_)
    if param.startswith("inf"):
        return await fetch_video_info(message, param, _)


async def show_user_stats(message: Message, _):
    m = await message.reply_text("🔎 Kişisel istatistikleriniz getiriliyor...")
    stats = await get_userss(message.from_user.id)
    if not stats:
        await asyncio.sleep(1)
        return await m.edit(_["ustats_1"])

    def get_stats():
        msg = ""
        limit = 0
        results = {i: stats[i]["spot"] for i in stats}
        list_arranged = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))
        if not results:
            return None, None
        total = sum(list_arranged.values())
        videoid = None
        for vidid, count in list_arranged.items():
            if limit == 10:
                continue
            if limit == 0:
                videoid = vidid
            limit += 1
            details = stats.get(vidid)
            title = (details["title"][:35]).title()
            if vidid == "telegram":
                msg += f"🎧 [Telegram Dosyaları](https://t.me/telegram) **{count} kez oynatıldı**\n\n"
            else:
                msg += f"🎵 [{title}](https://www.youtube.com/watch?v={vidid}) **{count} kez oynatıldı**\n\n"
        msg = _["ustats_2"].format(len(stats), total, limit) + msg
        return videoid, msg

    try:
        videoid, msg = await loop.run_in_executor(None, get_stats)
        if not videoid:
            return await m.edit(_["ustats_1"])
        thumbnail = await YouTube.thumbnail(videoid, True)
        await m.delete()
        return await message.reply_photo(photo=thumbnail, caption=msg)
    except Exception as e:
        print(e)


async def fetch_video_info(message: Message, param: str, _):
    m = await message.reply_text("🔎 Bilgi Alınıyor...")
    query = f"https://www.youtube.com/watch?v={param.replace('info_', '', 1)}"
    results = VideosSearch(query, limit=1)
    result = (await results.next())["result"][0]

    caption = f"""
🎬 **{result['title']}**
⏳ Süre: {result['duration']}
👀 Görüntüleme: {result['viewCount']['short']}
🕒 Yayın: {result['publishedTime']}
📺 Kanal: [{result['channel']['name']}]({result['channel']['link']})
🔗 [YouTube'da İzle]({result['link']})
"""
    key = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("🎥 İzle", url=result['link']),
            InlineKeyboardButton("❌ Kapat", callback_data="close")
        ]]
    )
    await m.delete()
    return await app.send_photo(message.chat.id, photo=result['thumbnails'][0]['url'].split("?")[0], caption=caption, reply_markup=key)


# ===================== START KOMUTU =====================
@app.on_message(
    filters.command(get_command("START_COMMAND"))
    & filters.private
    & ~BANNED_USERS
)
@LanguageStart
async def start_comm(client, message: Message, _):
    loading = await show_loading(message)

    # Kullanıcıyı veritabanına ekle
    await add_served_user(message.from_user.id)

    # ------------------ KULLANICI İSTATİSTİK ÖZETİ ------------------
    try:
        stats = await get_userss(message.from_user.id)
        if stats:
            def calc_brief():
                total = 0
                top = (None, 0, "")
                for vidid, details in stats.items():
                    cnt = details.get("spot", 0)
                    total += cnt
                    title = details.get("title", "") or ""
                    if cnt > top[1]:
                        top = (vidid, cnt, title)
                return total, top

            total_plays, top_item = await loop.run_in_executor(None, calc_brief)
            top_vidid, top_count, top_title = top_item

            if total_plays > 0 and top_vidid:
                if top_vidid == "telegram":
                    stat_text = (
                        f"🎧 Toplam oynatma sayın: **{total_plays}**\n"
                        f"📌 En çok oynattığın: Telegram dosyaları — **{top_count}** kez"
                    )
                    await message.reply_text(stat_text, parse_mode=ParseMode.MARKDOWN)
                else:
                    try:
                        thumb = await YouTube.thumbnail(top_vidid, True)
                    except:
                        thumb = None
                    stat_caption = (
                        f"🎧 Toplam oynatma sayın: **{total_plays}**\n"
                        f"🎵 En çok oynattığın: [{top_title[:60]}]("
                        f"https://www.youtube.com/watch?v={top_vidid}) — **{top_count}** kez"
                    )
                    if thumb:
                        await message.reply_photo(photo=thumb, caption=stat_caption, parse_mode=ParseMode.MARKDOWN)
                    else:
                        await message.reply_text(stat_caption, parse_mode=ParseMode.MARKDOWN)
    except:
        pass
    # ------------------ /KULLANICI İSTATİSTİK ÖZETİ BİTTİ ------------------

    params = message.text.split(None, 1)
    if len(params) > 1:
        await loading.delete()
        return await handle_start_params(client, message, params[1], _)

    await loading.delete()
    try:
        await app.resolve_peer(OWNER_ID[0])
        OWNER = OWNER_ID[0]
    except:
        OWNER = None
    out = private_panel(_, app.username, OWNER)
    caption = f"✨ {config.MUSIC_BOT_NAME} seni karşıladı!\n\n🎶 Tüm müzik komutları için aşağıdaki paneli kullanabilirsin."
    if config.START_IMG_URL:
        try:
            await message.reply_photo(photo=config.START_IMG_URL, caption=caption, reply_markup=InlineKeyboardMarkup(out))
        except:
            await message.reply_text(caption, reply_markup=InlineKeyboardMarkup(out))
    else:
        await message.reply_text(caption, reply_markup=InlineKeyboardMarkup(out))

    # ------------------ LOG GRUBUNA BİLDİRİM ------------------
    if await is_on_off(config.LOG):
        log_text = (
            f"👤 {message.from_user.mention} (@{message.from_user.username}) "
            f"({message.from_user.id}) /start komutunu kullandı."
        )
        await app.send_message(config.LOG_GROUP_ID, log_text)
    # ------------------ LOG BİLDİRİM BİTTİ ------------------


# ===================== GRUPA EKLENİNCE HOŞGELDİN MESAJI =====================
welcome_group = 2

@app.on_message(filters.new_chat_members, group=welcome_group)
async def welcome(client, message: Message):
    chat_id = message.chat.id
    if config.PRIVATE_BOT_MODE == "True":
        if not await is_served_private_chat(chat_id):
            await message.reply_text(
                "**Özel Müzik Botu**\n\nYalnızca sahibinden yetkili sohbetlerde kullanılabilir."
            )
            return await app.leave_chat(chat_id)
    else:
        await add_served_chat(chat_id)

    for member in message.new_chat_members:
        try:
            language = await get_lang(chat_id)
            _ = get_string(language)
            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_6"])
                    return await app.leave_chat(chat_id)
                if chat_id in await blacklisted_chats():
                    await message.reply_text(_["start_7"].format(f"https://t.me/{app.username}?start=sudolist"))
                    return await app.leave_chat(chat_id)

                userbot = await get_assistant(chat_id)
                out = start_pannel(_)
                video_url = "https://telegra.ph/file/acfb445238b05315f0013.mp4"
                video_caption = _["start_3"].format(config.MUSIC_BOT_NAME, userbot.username, userbot.id)
                await app.send_video(chat_id, video_url, caption=video_caption, reply_markup=InlineKeyboardMarkup(out))

            elif member.id in config.OWNER_ID:
                await message.reply_text(_["start_4"].format(config.MUSIC_BOT_NAME, member.mention))
            elif member.id in SUDOERS:
                await message.reply_text(_["start_5"].format(config.MUSIC_BOT_NAME, member.mention))
        except:
            continue
