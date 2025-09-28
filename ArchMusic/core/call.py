import asyncio
from datetime import datetime, timedelta
from typing import Union

from pyrogram import Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.types import InlineKeyboardMarkup
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.exceptions import (
    AlreadyJoinedError,
    NoActiveGroupCall,
    TelegramServerError,
)
from pytgcalls.types import (
    JoinedGroupCallParticipant,
    LeftGroupCallParticipant,
    Update,
)
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.stream import StreamAudioEnded

import config
from strings import get_string
from ArchMusic import LOGGER, YouTube, app
from ArchMusic.misc import db
from ArchMusic.utils.database import (
    add_active_chat,
    add_active_video_chat,
    get_assistant,
    get_audio_bitrate,
    get_lang,
    get_loop,
    get_video_bitrate,
    group_assistant,
    is_autoend,
    music_on,
    mute_off,
    remove_active_chat,
    remove_active_video_chat,
    set_loop,
)
from ArchMusic.utils.exceptions import AssistantErr
from ArchMusic.utils.inline.play import stream_markup, telegram_markup
from ArchMusic.utils.stream.autoclear import auto_clean

# Otomatik kapanma zamanlayıcıları
autoend = {}
counter = {}
AUTO_END_TIME = 3  # Dakika cinsinden

# Sıfırlama fonksiyonu
async def _clear_(chat_id: int) -> None:
    db[chat_id] = []
    await remove_active_video_chat(chat_id)
    await remove_active_chat(chat_id)

# Otomatik kapanmayı kontrol eden döngü
async def autoend_checker():
    while True:
        now = datetime.now()
        for chat_id, end_time in list(autoend.items()):
            if end_time and now >= end_time:
                await ArchMusic.stop_stream(chat_id)
                autoend.pop(chat_id, None)
        await asyncio.sleep(30)

# Mesaj metni oluşturma fonksiyonu
def now_playing_text(title: str, duration: str, user: str) -> str:
    return (
     f"🎶 **═════ ❀•°❀°•❀ ═════╗
        🎼   M Ü Z İ K   S H O W 
             B A Ş L I Y O R   🎼
        ╚═════ ❀•°❀°•❀ ═════╝*\n"
       f"📌 Parça: {title}\n"
        f"⏱️ Süre: {duration}\n"
        f"👤 Ekleyen: {user}\n"
  f"  🌟 Müziğin Ritmini Hisset • Ruhunu Notaya Bırak ✨"
    )      
        

# Ana Call sınıfı
class Call(PyTgCalls):
    def __init__(self):
        self.userbot1 = Client(
            "ArchMusicString1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1),
        )
        self.one = PyTgCalls(self.userbot1, cache_duration=100)

        self.userbot2 = Client(
            "ArchMusicString2",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING2),
        )
        self.two = PyTgCalls(self.userbot2, cache_duration=100)

        self.userbot3 = Client(
            "ArchMusicString3",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING3),
        )
        self.three = PyTgCalls(self.userbot3, cache_duration=100)

        self.userbot4 = Client(
            "ArchMusicString4",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING4),
        )
        self.four = PyTgCalls(self.userbot4, cache_duration=100)

        self.userbot5 = Client(
            "ArchMusicString5",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING5),
        )
        self.five = PyTgCalls(self.userbot5, cache_duration=100)

    # Akışı durdur
    async def pause_stream(self, chat_id: int) -> None:
        assistant = await group_assistant(self, chat_id)
        await assistant.pause_stream(chat_id)

    # Akışı devam ettir
    async def resume_stream(self, chat_id: int) -> None:
        assistant = await group_assistant(self, chat_id)
        await assistant.resume_stream(chat_id)

    # Sesi kapat
    async def mute_stream(self, chat_id: int) -> None:
        assistant = await group_assistant(self, chat_id)
        await assistant.mute_stream(chat_id)

    # Sesi aç
    async def unmute_stream(self, chat_id: int) -> None:
        assistant = await group_assistant(self, chat_id)
        await assistant.unmute_stream(chat_id)

    # Tamamen durdur ve temizle
    async def stop_stream(self, chat_id: int) -> None:
        assistant = await group_assistant(self, chat_id)
        try:
            await _clear_(chat_id)
            await assistant.leave_group_call(chat_id)
        except Exception:
            pass

    # Zorla durdur
    async def force_stop_stream(self, chat_id: int) -> None:
        assistant = await group_assistant(self, chat_id)
        try:
            check = db.get(chat_id)
            check.pop(0)
        except IndexError:
            pass
        await remove_active_video_chat(chat_id)
        await remove_active_chat(chat_id)
        try:
            await assistant.leave_group_call(chat_id)
        except Exception:
            pass

    # Bir sonraki parçaya geç
    async def skip_stream(
        self, chat_id: int, link: str, video: Union[bool, str] = None
    ) -> None:
        assistant = await group_assistant(self, chat_id)
        audio_stream_quality = await get_audio_bitrate(chat_id)
        video_stream_quality = await get_video_bitrate(chat_id)
        stream = (
            AudioVideoPiped(
                link,
                audio_parameters=audio_stream_quality,
                video_parameters=video_stream_quality,
            )
            if video
            else AudioPiped(link, audio_parameters=audio_stream_quality)
        )
        await assistant.change_stream(chat_id, stream)

    # Belirli bir süreye atla (seek)
    async def seek_stream(
        self,
        chat_id: int,
        file_path: str,
        to_seek: str,
        duration: str,
        mode: str,
    ) -> None:
        assistant = await group_assistant(self, chat_id)
        audio_stream_quality = await get_audio_bitrate(chat_id)
        video_stream_quality = await get_video_bitrate(chat_id)
        stream = (
            AudioVideoPiped(
                file_path,
                audio_parameters=audio_stream_quality,
                video_parameters=video_stream_quality,
                additional_ffmpeg_parameters=f"-ss {to_seek} -to {duration}",
            )
            if mode == "video"
            else AudioPiped(
                file_path,
                audio_parameters=audio_stream_quality,
                additional_ffmpeg_parameters=f"-ss {to_seek} -to {duration}",
            )
        )
        await assistant.change_stream(chat_id, stream)

    # Test amaçlı akış başlat
    async def stream_call(self, link: str) -> None:
        assistant = await group_assistant(self, config.LOG_GROUP_ID)
        await assistant.join_group_call(
            config.LOG_GROUP_ID,
            AudioVideoPiped(link),
            stream_type=StreamType().pulse_stream,
        )
        await asyncio.sleep(0.5)
        await assistant.leave_group_call(config.LOG_GROUP_ID)

    # Asistanı gruba davet et
    async def join_assistant(self, original_chat_id: int, chat_id: int) -> None:
        language = await get_lang(original_chat_id)
        _ = get_string(language)
        userbot = await get_assistant(chat_id)
        try:
            try:
                get = await app.get_chat_member(chat_id, userbot.id)
            except ChatAdminRequired:
                raise AssistantErr("⚠️ Botun bu gruba yönetici izinleri yok.")
            if get.status in (ChatMemberStatus.BANNED, ChatMemberStatus.LEFT):
                raise AssistantErr(
                    f"❌ Asistan [{userbot.first_name}](tg://user?id={userbot.id}) gruptan atılmış veya ayrılmış."
                )
        except UserNotParticipant:
            chat = await app.get_chat(chat_id)
            if chat.username:
                try:
                    await userbot.join_chat(chat.username)
                except UserAlreadyParticipant:
                    pass
                except Exception as e:
                    raise AssistantErr(f"Asistan gruba katılamadı: {e}")
            else:
                try:
                    invitelink = chat.invite_link
                    if invitelink is None:
                        invitelink = await app.export_chat_invite_link(chat_id)
                except ChatAdminRequired:
                    raise AssistantErr("Bot davet bağlantısı oluşturamıyor. Lütfen botu yönetici yapın.")
                except Exception as e:
                    raise AssistantErr(str(e))

                m = await app.send_message(original_chat_id, "⏳ Asistan gruba katılıyor, lütfen bekleyin...")
                if invitelink.startswith("https://t.me/+"):
                    invitelink = invitelink.replace("https://t.me/+", "https://t.me/joinchat/")
                await asyncio.sleep(3)
                await userbot.join_chat(invitelink)
                await asyncio.sleep(4)
                await m.edit(f"✅ Asistan **{userbot.first_name}** gruba katıldı ve müzik çalmaya hazır!")

    # Gruba katıl ve akışı başlat
    async def join_call(
        self,
        chat_id: int,
        original_chat_id: int,
        link,
        video: Union[bool, str] = None,
    ) -> None:
        assistant = await group_assistant(self, chat_id)
        audio_stream_quality = await get_audio_bitrate(chat_id)
        video_stream_quality = await get_video_bitrate(chat_id)
        stream = (
            AudioVideoPiped(
                link,
                audio_parameters=audio_stream_quality,
                video_parameters=video_stream_quality,
            )
            if video
            else AudioPiped(link, audio_parameters=audio_stream_quality)
        )
        try:
            await assistant.join_group_call(
                chat_id,
                stream,
                stream_type=StreamType().pulse_stream,
            )
        except NoActiveGroupCall:
            try:
                await self.join_assistant(original_chat_id, chat_id)
                await assistant.join_group_call(
                    chat_id,
                    stream,
                    stream_type=StreamType().pulse_stream,
                )
            except Exception:
                raise AssistantErr(
                    "📢 **Sesli sohbet başlatılmamış veya görünmüyor.**\n\n"
                    "Lütfen şunları kontrol edin:\n"
                    "• Grubunuzda sesli sohbet aktif mi?\n"
                    "• Varsa, sohbeti kapatıp yeniden açmayı deneyin.\n"
                    "• Sorun devam ederse: /yeniden yazarak botu yeniden başlatmayı deneyin."
                )
        except AlreadyJoinedError:
            raise AssistantErr(
                "🔄 **Asistan zaten sesli sohbette.**\n\n"
                "Bu durum genellikle iki komutu aynı anda kullandığınızda olur.\n"
                "Eğer asistan görünmüyorsa, sesli sohbeti kapatıp yeniden açmayı deneyin."
            )
        except TelegramServerError:
            raise AssistantErr(
                "⚙️ **Telegram sunucusunda geçici bir hata oluştu.**\n\n"
                "Lütfen birkaç saniye sonra tekrar deneyin veya sesli sohbeti yeniden başlatın."
            )

        await add_active_chat(chat_id)
        await mute_off(chat_id)
        await music_on(chat_id)
        if video:
            await add_active_video_chat(chat_id)
        if await is_autoend():
            counter[chat_id] = {}
            users = len(await assistant.get_participants(chat_id))
            if users == 1:
                autoend[chat_id] = datetime.now() + timedelta(minutes=AUTO_END_TIME)

    # Şarkı bittiğinde sıradaki parçaya geç
    async def change_stream(self, client, chat_id: int) -> None:
        check = db.get(chat_id)
        popped = None
        loop = await get_loop(chat_id)
        try:
            if loop == 0:
                popped = check.pop(0)
            else:
                loop -= 1
                await set_loop(chat_id, loop)
            if popped and config.AUTO_DOWNLOADS_CLEAR == str(True):
                await auto_clean(popped)
            if not check:
                await _clear_(chat_id)
                await app.send_message(chat_id, "🎧 Sıra bitti, sesli sohbetten ayrılıyorum.")
                return await client.leave_group_call(chat_id)
        except Exception:
            try:
                await _clear_(chat_id)
                return await client.leave_group_call(chat_id)
            except Exception:
                return

        queued = check[0]["file"]
        title = check[0]["title"].title()
        user = check[0]["by"]
        original_chat_id = check[0]["chat_id"]
        streamtype = check[0]["streamtype"]
        audio_stream_quality = await get_audio_bitrate(chat_id)
        video_stream_quality = await get_video_bitrate(chat_id)
        videoid = check[0]["vidid"]
        check[0]["played"] = 0

        if "live_" in queued:
            n, link = await YouTube.video(videoid, True)
            if n == 0:
                return await app.send_message(original_chat_id, "❌ Canlı yayın başlatılamadı.")
            stream = (
                AudioVideoPiped(
                    link,
                    audio_parameters=audio_stream_quality,
                    video_parameters=video_stream_quality,
                )
                if str(streamtype) == "video"
                else AudioPiped(link, audio_parameters=audio_stream_quality)
            )
            try:
                await client.change_stream(chat_id, stream)
            except Exception:
                return await app.send_message(original_chat_id, "❌ Canlı yayın yüklenemedi.")

        elif "vid_" in queued:
            mystic = await app.send_message(original_chat_id, "📥 Video indiriliyor...")
            try:
                file_path, direct = await YouTube.download(
                    videoid,
                    mystic,
                    videoid=True,
                    video=True if str(streamtype) == "video" else False,
                )
            except Exception:
                return await mystic.edit_text("❌ Video indirilemedi.", disable_web_page_preview=True)

            stream = (
                AudioVideoPiped(
                    file_path,
                    audio_parameters=audio_stream_quality,
                    video_parameters=video_stream_quality,
                )
                if str(streamtype) == "video"
                else AudioPiped(file_path, audio_parameters=audio_stream_quality)
            )
            try:
                await client.change_stream(chat_id, stream)
            except Exception:
                return await app.send_message(original_chat_id, "❌ Video yüklenemedi.")
            await mystic.delete()

        elif "index_" in queued:
            stream = (
                AudioVideoPiped(
                    videoid,
                    audio_parameters=audio_stream_quality,
                    video_parameters=video_stream_quality,
                )
                if str(streamtype) == "video"
                else AudioPiped(videoid, audio_parameters=audio_stream_quality)
            )
            try:
                await client.change_stream(chat_id, stream)
            except Exception:
                return await app.send_message(original_chat_id, "❌ Dosya yüklenemedi.")

        else:
            stream = (
                AudioVideoPiped(
                    queued,
                    audio_parameters=audio_stream_quality,
                    video_parameters=video_stream_quality,
                )
                if str(streamtype) == "video"
                else AudioPiped(queued, audio_parameters=audio_stream_quality)
            )
            try:
                await client.change_stream(chat_id, stream)
            except Exception:
                return await app.send_message(original_chat_id, "❌ Parça yüklenemedi.")

        # ✅ Mesajı tek tip, güvenli ve güzel şekilde gönder
        duration = check[0].get("dur", "Bilinmiyor")
        message_text = now_playing_text(title, duration, user)
        run = await app.send_message(
            chat_id=original_chat_id,
            text=message_text
        )
        db[chat_id][0]["mystic"] = run
        db[chat_id][0]["markup"] = "tg" if videoid in ["telegram", "soundcloud"] else "stream"

    # Ping ölçümü
    async def ping(self) -> str:
        pings = []
        for client in (self.one, self.two, self.three, self.four, self.five):
            if config.STRING1 and client is self.one:
                pings.append(await client.ping)
            if config.STRING2 and client is self.two:
                pings.append(await client.ping)
            if config.STRING3 and client is self.three:
                pings.append(await client.ping)
            if config.STRING4 and client is self.four:
                pings.append(await client.ping)
            if config.STRING5 and client is self.five:
                pings.append(await client.ping)
        return f"📡 Ortalama gecikme: {round(sum(pings) / len(pings), 3)} ms" if pings else "❌ Bot şu anda aktif değil."

    # Tüm client'ları başlat
    async def start(self) -> None:
        LOGGER(__name__).info("🎵 ArchMusic bot başlatılıyor...")
        for client, string in (
            (self.one, config.STRING1),
            (self.two, config.STRING2),
            (self.three, config.STRING3),
            (self.four, config.STRING4),
            (self.five, config.STRING5),
        ):
            if string:
                await client.start()

        # 🔹 Otomatik kapanma döngüsünü başlat
        asyncio.create_task(autoend_checker())

    # Olay dinleyicileri
    async def decorators(self) -> None:
        for client in (self.one, self.two, self.three, self.four, self.five):
            if not hasattr(client, "on_kicked"):
                continue

            @client.on_kicked()
            @client.on_closed_voice_chat()
            @client.on_left()
            async def stream_services_handler(_, chat_id: int):
                await self.stop_stream(chat_id)

            @client.on_stream_end()
            async def stream_end_handler(client, update: Update):
                if isinstance(update, StreamAudioEnded):
                    await self.change_stream(client, update.chat_id)

            @client.on_participants_change()
            async def participants_change_handler(client, update: Update):
                if isinstance(update, (JoinedGroupCallParticipant, LeftGroupCallParticipant)):
                    chat_id = update.chat_id
                    try:
                        users = counter.get(chat_id)
                        if not users:
                            got = len(await client.get_participants(chat_id))
                            counter[chat_id] = got
                            if got == 1:
                                autoend[chat_id] = datetime.now() + timedelta(minutes=AUTO_END_TIME)
                            else:
                                autoend[chat_id] = {}
                        else:
                            final = users + 1 if isinstance(update, JoinedGroupCallParticipant) else users - 1
                            counter[chat_id] = final
                            if final == 1:
                                autoend[chat_id] = datetime.now() + timedelta(minutes=AUTO_END_TIME)
                            else:
                                autoend[chat_id] = {}
                    except Exception:
                        return

# Ana nesne
ArchMusic = Call()
