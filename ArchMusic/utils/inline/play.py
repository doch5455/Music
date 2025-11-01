from pyrogram.types import InlineKeyboardButton
import random

# ===============================================
# 💠 Kumsal Bots - Mavi Arayüz (Temiz Bar Sürümü)
# Sade • Net • Anlaşılır • Parıltılı Çizgi Stili
# ===============================================


def clear_bar():
    bars = [
        "━━━━━━━━━━ 💠 ━━━━━━━━━━",
        "━━━▰▰▰▰▰💠▰▰▰▰▰━━━",
        "─────── 💠 ───────",
        "═══════💠══════",
        "━━━━━ 💠 ━━━━━",
        "━━━⋆⋆⋆💠⋆⋆⋆━━━",
    ]
    return random.choice(bars)


# ───────────────────────────────
# 🎵 Stream Menüsü
# ───────────────────────────────
def stream_markup(_, videoid, chat_id):
    bar = clear_bar()
    return [
        [InlineKeyboardButton(text=bar, callback_data="bar_locked")],
        [
            InlineKeyboardButton("🔼 Başlat", callback_data=f"stream_play {videoid}|{chat_id}"),
            InlineKeyboardButton("📺 Görsel", callback_data=f"stream_video {videoid}|{chat_id}")
        ],
        [
            InlineKeyboardButton("⏮️ Geri", callback_data=f"ADMIN Back|{chat_id}"),
            InlineKeyboardButton("⏭️ İleri", callback_data=f"ADMIN Forward|{chat_id}")
        ],
        [
            InlineKeyboardButton("💠 Mavi", url="https://t.me/MaviDuyuru"),
            InlineKeyboardButton("❌ Kapat", callback_data=f"forceclose {videoid}|{chat_id}")
        ],
    ]


# ───────────────────────────────
# 🧩 Track Seçimi
# ───────────────────────────────
def track_markup(_, videoid, user_id, channel, fplay):
    bar = clear_bar()
    return [
        [InlineKeyboardButton(text=bar, callback_data="bar_locked")],
        [
            InlineKeyboardButton("🎧 Sesli", callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}"),
            InlineKeyboardButton("🎥 Görsel", callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}")
        ],
        [
            InlineKeyboardButton("⏮️ Önceki", callback_data=f"slider B|Track|{user_id}|{channel}|{fplay}"),
            InlineKeyboardButton("🔼 Üste", callback_data="bar_locked"),
            InlineKeyboardButton("⏭️ Sonraki", callback_data=f"slider F|Track|{user_id}|{channel}|{fplay}")
        ],
        [
            InlineKeyboardButton("💠 Mavi", url="https://t.me/MaviDuyuru"),
            InlineKeyboardButton("❌ Kapat", callback_data=f"forceclose {videoid}|{user_id}")
        ],
    ]


# ───────────────────────────────
# 📜 Playlist Menüsü
# ───────────────────────────────
def playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    bar = clear_bar()
    return [
        [InlineKeyboardButton(text=bar, callback_data="bar_locked")],
        [
            InlineKeyboardButton("🎧 Sesli", callback_data=f"YukkiPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}"),
            InlineKeyboardButton("🎥 Görsel", callback_data=f"YukkiPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}")
        ],
        [
            InlineKeyboardButton("⏮️ Geri", callback_data=f"ADMIN Back|{channel}"),
            InlineKeyboardButton("🔄 Karıştır", callback_data=f"ADMIN Shuffle|{channel}"),
            InlineKeyboardButton("⏭️ Atla", callback_data=f"ADMIN Skip|{channel}")
        ],
        [
            InlineKeyboardButton("💠 Mavi", url="https://t.me/MaviDuyuru"),
            InlineKeyboardButton("❌ Kapat", callback_data=f"forceclose {videoid}|{user_id}")
        ],
    ]


# ───────────────────────────────
# 📺 Canlı Yayın Menüsü
# ───────────────────────────────
def livestream_markup(_, videoid, user_id, mode, channel, fplay):
    bar = clear_bar()
    return [
        [InlineKeyboardButton(text=bar, callback_data="bar_locked")],
        [
            InlineKeyboardButton("📡 Yayını Başlat", callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}")
        ],
        [
            InlineKeyboardButton("🔼 Sesli Mod", callback_data=f"ADMIN ModeA|{channel}"),
            InlineKeyboardButton("🔽 Görsel Mod", callback_data=f"ADMIN ModeV|{channel}")
        ],
        [
            InlineKeyboardButton("💠 Mavi", url="https://t.me/MaviDuyuru"),
            InlineKeyboardButton("❌ Kapat", callback_data=f"forceclose {videoid}|{user_id}")
        ],
    ]


# ───────────────────────────────
# ⚙️ Kontrol Paneli (Sayfa 1)
# ───────────────────────────────
def panel_markup_1(_, videoid, chat_id):
    bar = clear_bar()
    return [
        [InlineKeyboardButton(text=bar, callback_data="bar_locked")],
        [
            InlineKeyboardButton("⏸ Durdur", callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton("▶️ Devam", callback_data=f"ADMIN Resume|{chat_id}"),
        ],
        [
            InlineKeyboardButton("⏯️ Atla", callback_data=f"ADMIN Skip|{chat_id}"),
            InlineKeyboardButton("⏹️ Bitir", callback_data=f"ADMIN Stop|{chat_id}"),
        ],
        [
            InlineKeyboardButton("💠 Mavi", url="https://t.me/MaviDuyuru"),
            InlineKeyboardButton("❌ Kapat", callback_data=f"forceclose {videoid}|{chat_id}")
        ],
    ]


# ───────────────────────────────
# ⚙️ Kontrol Paneli (Sayfa 2)
# ───────────────────────────────
def panel_markup_2(_, videoid, chat_id):
    bar = clear_bar()
    return [
        [InlineKeyboardButton(text=bar, callback_data="bar_locked")],
        [
            InlineKeyboardButton("🔇 Sessize", callback_data=f"ADMIN Mute|{chat_id}"),
            InlineKeyboardButton("🔊 Aç", callback_data=f"ADMIN Unmute|{chat_id}"),
        ],
        [
            InlineKeyboardButton("🔁 Döngü", callback_data=f"ADMIN Loop|{chat_id}"),
            InlineKeyboardButton("🔀 Karıştır", callback_data=f"ADMIN Shuffle|{chat_id}"),
        ],
        [
            InlineKeyboardButton("💠 Mavi", url="https://t.me/MaviDuyuru"),
            InlineKeyboardButton("❌ Kapat", callback_data=f"forceclose {videoid}|{chat_id}")
        ],
    ]


# ───────────────────────────────
# ⚙️ Kontrol Paneli (Sayfa 3)
# ───────────────────────────────
def panel_markup_3(_, videoid, chat_id):
    bar = clear_bar()
    return [
        [InlineKeyboardButton(text=bar, callback_data="bar_locked")],
        [
            InlineKeyboardButton("⏮️ 10 Sn", callback_data=f"ADMIN 1|{chat_id}"),
            InlineKeyboardButton("⏭️ 10 Sn", callback_data=f"ADMIN 2|{chat_id}"),
        ],
        [
            InlineKeyboardButton("⏮️ 30 Sn", callback_data=f"ADMIN 3|{chat_id}"),
            InlineKeyboardButton("⏭️ 30 Sn", callback_data=f"ADMIN 4|{chat_id}"),
        ],
        [
            InlineKeyboardButton("💠 Mavi", url="https://t.me/MaviDuyuru"),
            InlineKeyboardButton("❌ Kapat", callback_data=f"forceclose {videoid}|{chat_id}")
        ],
    ]