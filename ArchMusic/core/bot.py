import sys
from pyrogram import Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import BotCommand, BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats

import config
from ..logging import LOGGER  # Proje içi özel logger modülü


# 🌐 Özel sohbetlerde çalışacak komutlar
PRIVATE_COMMANDS = [
    BotCommand("start", "🌟 Botu başlat ve müzik keyfine başla"),
    BotCommand("yardim", "🧠 Yardım menüsünü göster"),
]

# 💬 Gruplarda çalışacak komutlar
GROUP_COMMANDS = [
    BotCommand("oynat", "🎶 Seçilen şarkıyı çalmaya başlar"),
    BotCommand("voynat", "🎬 Video oynatımını başlatır"),
    BotCommand("atla", "⏭️ Sonraki şarkıya geç"),
    BotCommand("duraklat", "⏸️ Şarkıyı duraklat"),
    BotCommand("devam", "▶️ Şarkıyı devam ettir"),
    BotCommand("son", "⛔ Oynatmayı durdur"),
    BotCommand("karistir", "🔀 Çalma listesini karıştır"),
    BotCommand("dongu", "🔁 Tekrar modunu etkinleştir"),
    BotCommand("sira", "📋 Kuyruğu göster"),
    BotCommand("ilerisar", "⏩ Şarkıyı ileri sar"),
    BotCommand("gerisar", "⏪ Şarkıyı geri sar"),
    BotCommand("playlist", "🎼 Kendi çalma listen"),
    BotCommand("bul", "🔍 Müzik ara ve indir"),
    BotCommand("ayarlar", "⚙️ Grup ayarlarını göster"),
    BotCommand("restart", "♻️ Botu yeniden başlat"),
    BotCommand("reload", "🔄 Admin önbelleğini yenile"),
]


async def set_bot_commands(client: Client):
    """Telegram'a bot komutlarını yükler."""
    await client.set_bot_commands(PRIVATE_COMMANDS, scope=BotCommandScopeAllPrivateChats())
    await client.set_bot_commands(GROUP_COMMANDS, scope=BotCommandScopeAllGroupChats())


# 🎧 Ana bot sınıfı
class ArchMusic(Client):
    def __init__(self):
        self.logger = LOGGER(__name__)
        self.logger.info("🚀 ArchMusic başlatılıyor...")

        super().__init__(
            name="ArchMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
        )

    async def start(self):
        await super().start()

        try:
            await self._load_bot_info()
            await self._check_logger_group_admin()
            await self._send_startup_notice()
            await set_bot_commands(self)

            self.logger.info(f"✅ {self.name} (@{self.username}) başarıyla başlatıldı.")

        except Exception as e:
            self.logger.error(f"❌ Başlatma hatası: {e}")
            sys.exit()

    async def _load_bot_info(self):
        """Botun kendi bilgilerini alır."""
        me = await self.get_me()
        self.username = me.username
        self.id = me.id
        self.name = f"{me.first_name} {me.last_name}" if me.last_name else me.first_name

    async def _check_logger_group_admin(self):
        """Log grubunda yönetici yetkisi kontrolü yapar."""
        member = await self.get_chat_member(config.LOG_GROUP_ID, self.id)
        if member.status != ChatMemberStatus.ADMINISTRATOR:
            self.logger.error("⚠️ Lütfen log grubunda botu yönetici yapın.")
            sys.exit()

    async def _send_startup_notice(self):
        """Log grubuna botun aktif olduğunu bildirir."""
        try:
            await self.send_video(
                chat_id=config.LOG_GROUP_ID,
                video="https://telegra.ph/file/802dbdcdd7e5653ef135a.mp4",  # ✅ Şık müzik dalgası videosu
                caption=(
                    "✅ **AMED Bot Aktif!**\n\n"
                    "🎵 Müzik sistemleri başarıyla başlatıldı.\n"
                    "📡 Komutlar yüklendi ve çalışıyor.\n\n"
                    "✨ Keyifli dinlemeler!"
                ),
            )
        except Exception:
            self.logger.error(
                "🚫 Log grubuna video gönderilemedi. Botu gruba eklediğinizden ve yönetici yaptığınızdan emin olun."
            )
            sys.exit()
