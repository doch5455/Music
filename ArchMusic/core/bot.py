import sys

from pyrogram import Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import (
    BotCommand,
    BotCommandScopeAllPrivateChats,
    BotCommandScopeAllGroupChats,
)

import config
from ..logging import LOGGER


# 🔹 Komutlar: Spotify havası, sade ve net
PRIVATE_COMMANDS = [
    BotCommand("start", "🌟 Botu başlat ve müzik keyfine başla"),
    BotCommand("yardim", "🧠 Komut rehberini göster"),
]

GROUP_COMMANDS = [
    BotCommand("oynat", "🎶 Seçilen şarkıyı çalmaya başlar"),
    BotCommand("voynat", "🎬 Video oynatımını başlatır"),
    BotCommand("atla", "➡️ Sonraki şarkıya geç"),
    BotCommand("duraklat", "⏸️ Şarkıyı duraklat"),
    BotCommand("devam", "▶️ Şarkıyı devam ettir"),
    BotCommand("son", "⛔ Oynatmayı durdur"),
    BotCommand("karistir", "🔁 Listeyi rastgele sırala"),
    BotCommand("dongu", "🔂 Aynı parçayı döngüye al"),
    BotCommand("sira", "📋 Sıradaki parçaları göster"),
    BotCommand("ilerisar", "⏩ Şarkıyı ileri sar"),
    BotCommand("gerisar", "⏪ Şarkıyı geri sar"),
    BotCommand("playlist", "🎼 Kişisel playlistini göster"),
    BotCommand("bul", "🔍 Müzik ara ve indir"),
    BotCommand("ayarlar", "⚙️ Grup ayarlarını yapılandır"),
    BotCommand("restart", "♻️ Botu yeniden başlat"),
    BotCommand("reload", "🚨 Admin önbelleğini yenile"),
]


# 🔧 Komutları Telegram botuna tanımlama
async def set_commands(client: Client):
    await client.set_bot_commands(PRIVATE_COMMANDS, scope=BotCommandScopeAllPrivateChats())
    await client.set_bot_commands(GROUP_COMMANDS, scope=BotCommandScopeAllGroupChats())


# 🔊 Ana Bot Sınıfı
class ArchMusic(Client):
    def __init__(self):
        self.logger = LOGGER(__name__)
        self.logger.info("🎧 Bot başlatılıyor...")

        super().__init__(
            "ArchMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
        )

    async def start(self):
        await super().start()

        try:
            me = await self.get_me()
            self.username = me.username
            self.id = me.id
            self.name = f"{me.first_name} {me.last_name}" if me.last_name else me.first_name

            await self._send_startup_message()
            await self._check_log_group_permissions()
            await set_commands(self)

            self.logger.info(f"✅ MusicBot **{self.name}** olarak başlatıldı.")

        except Exception as e:
            self.logger.error(f"❌ Bot başlatılırken bir hata oluştu: {e}")
            sys.exit()

    async def _send_startup_message(self):
        """🎬 Log grubuna botun aktif olduğunu bildiren mesaj gönder."""
        try:
            await self.send_video(
                chat_id=config.LOG_GROUP_ID,
                video="https://telegra.ph/file/36221d40afde82941ffff.mp4",
                caption=(
                    "✅ **ArchMusic Bot Aktif!**\n\n"
                    "🎶 Müzik sistemleri başarıyla başlatıldı.\n"
                    "📡 Komutlar yüklendi, hazırız!\n\n"
                    "_İyi dinlemeler dileriz._"
                ),
            )
        except Exception:
            self.logger.error(
                "🚫 Bot log grubuna mesaj gönderemedi. "
                "Botu log grubuna eklediğinizden ve yönetici yaptığınızdan emin olun."
            )
            sys.exit()

    async def _check_log_group_permissions(self):
        """🔐 Botun log grubunda yönetici olup olmadığını kontrol et."""
        member = await self.get_chat_member(config.LOG_GROUP_ID, self.id)
        if member.status != ChatMemberStatus.ADMINISTRATOR:
            self.logger.error("⚠️ Lütfen log grubunda botu yönetici yapın.")
            sys.exit()
try:
    me = await self.get_me()
    self.username = me.username
    self.id = me.id
except Exception as e:
    self.logger.error(f"❌ Bot başlatılırken bir hata oluştu: {e}")
    sys.exit()



        
