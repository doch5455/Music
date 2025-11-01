# ===============================================
# 🌌 Kumsal Bots - Parıltılı Müzik Arayüzü
# Minimal, modern, sade ve güçlü kontrol sistemi
# ===============================================

import math
from pyrogram.types import InlineKeyboardButton

# ───────────────────────────────
# 🔹 Basit ve şık zaman dönüştürücü
# ───────────────────────────────
def time_to_sec(t):
    parts = list(map(int, t.split(":")))
    return parts[0] * 60 + parts[1] if len(parts) == 2 else 0


# ───────────────────────────────
# 💫 Parıltılı ilerleme çubuğu
# ───────────────────────────────
def progress_bar(played, total):
    played_sec = time_to_sec(played)
    total_sec = time_to_sec(total) or 1
    ratio = played_sec / total_sec
    pos = int(ratio * 10)
    bar = ""
    for i in range(10):
        if i == pos:
            bar += "🔹"  # mavi parıltı noktası
        else:
            bar += "⠂"  # zarif çizgi efekti
    return f"{played}  {bar}  {total}"


# ───────────────────────────────
# 🎧 Stream oynatma (YouTube vb.)
# ───────────────────────────────
def stream_markup_timer(_, videoid, chat_id, played, dur):
    buttons = [
        [InlineKeyboardButton("🩵 𝗠𝗮𝘃𝗶 𝗗𝘂𝘆𝘂𝗿𝘂", url="https://t.me/maviduyuru")],
        [InlineKeyboardButton(text=progress_bar(played, dur), callback_data="nonclickable")],
        [
            InlineKeyboardButton("⏮", callback_data=f"ADMIN 1|{chat_id}"),
            InlineKeyboardButton("⏸", callback_data=f"pausevc {chat_id}"),
            InlineKeyboardButton("▶️", callback_data=f"resumevc {chat_id}"),
            InlineKeyboardButton("⏭", callback_data=f"ADMIN 2|{chat_id}"),
            InlineKeyboardButton("⏹", callback_data=f"stopvc {chat_id}"),
        ],
        [
            InlineKeyboardButton("💎 𝗟𝗶𝘀𝘁𝗲𝘆𝗲 𝗘𝗸𝗹𝗲", callback_data=f"add_playlist {videoid}"),
            InlineKeyboardButton("🕹️ 𝗠𝗲𝗻𝘂 𝗣𝗮𝗻𝗲𝗹", callback_data=f"PanelMarkup None|{chat_id}"),
        ],
    ]
    return buttons


# ───────────────────────────────
# 🌀 Telegram stream oynatma
# ───────────────────────────────
def telegram_markup_timer(_, chat_id, played, dur, videoid):
    buttons = [
        [InlineKeyboardButton("🚀  ᴍᴀᴠɪ ᴅᴜʏᴜʀᴜ 🚀", url="https://t.me/the_team_kumsal")],
        [InlineKeyboardButton(progress_bar(played, dur), callback_data="nonclickable")],
        [
            InlineKeyboardButton("⏮", callback_data=f"ADMIN 1|{chat_id}"),
            InlineKeyboardButton("⏸", callback_data=f"pausevc {chat_id}"),
            InlineKeyboardButton("▶️", callback_data=f"resumevc {chat_id}"),
            InlineKeyboardButton("⏭", callback_data=f"ADMIN 2|{chat_id}"),
            InlineKeyboardButton("⏹", callback_data=f"stopvc {chat_id}"),
        ],
        [
            InlineKeyboardButton("💎 Listeye Ekle", callback_data=f"add_playlist {videoid}"),
            InlineKeyboardButton("✨ Kontrol Paneli", callback_data=f"PanelMarkup None|{chat_id}"),
        ],
    ]
    return buttons


# ───────────────────────────────
# 🎛️ Standart kontrol menüsü
# ───────────────────────────────
def telegram_markup(_, chat_id):
    buttons = [
        [
            InlineKeyboardButton("⏮", callback_data=f"ADMIN 1|{chat_id}"),
            InlineKeyboardButton("⏸", callback_data=f"pausevc {chat_id}"),
            InlineKeyboardButton("▶️", callback_data=f"resumevc {chat_id}"),
            InlineKeyboardButton("⏭", callback_data=f"ADMIN 2|{chat_id}"),
            InlineKeyboardButton("⏹", callback_data=f"stopvc {chat_id}"),
        ],
        [
            InlineKeyboardButton("💠 Menüye Dön", callback_data=f"PanelMarkup None|{chat_id}"),
            InlineKeyboardButton("❌ Kapat", callback_data="close"),
        ],
    ]
    return buttons


# ───────────────────────────────
# 🧩 Track seçimi (liste veya sorgu)
# ───────────────────────────────
def track_markup(_, videoid, user_id, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"], callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"], callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        [InlineKeyboardButton("❌ Kapat", callback_data=f"forceclose {videoid}|{user_id}")],
    ]
    return buttons


# ───────────────────────────────
# 📜 Playlist menüsü
# ───────────────────────────────
def playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"], callback_data=f"YukkiPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"], callback_data=f"YukkiPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}",
            ),
        ],
        [InlineKeyboardButton("❌ Kapat", callback_data=f"forceclose {videoid}|{user_id}")],
    ]
    return buttons


# ───────────────────────────────
# 📺 Canlı yayın oynatma menüsü
# ───────────────────────────────
def livestream_markup(_, videoid, user_id, mode, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_3"],
                callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["CLOSEMENU_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
            ),
        ],
    ]
    return buttons


## Slider Query Markup


def slider_markup(
    _, videoid, user_id, query, query_type, channel, fplay
):
    query = f"{query[:20]}"
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="❮",
                callback_data=f"slider B|{query_type}|{query}|{user_id}|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {query}|{user_id}",
            ),
            InlineKeyboardButton(
                text="❯",
                callback_data=f"slider F|{query_type}|{query}|{user_id}|{channel}|{fplay}",
            ),
        ],
    ]
    return buttons


## Cpanel Markup


def panel_markup_1(_, videoid, chat_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="⏸ Pause", callback_data=f"ADMIN Pause|{chat_id}"
            ),
            InlineKeyboardButton(
                text="▶️ Resume",
                callback_data=f"ADMIN Resume|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="⏯ Skip", callback_data=f"ADMIN Skip|{chat_id}"
            ),
            InlineKeyboardButton(
                text="⏹ Stop", callback_data=f"ADMIN Stop|{chat_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="◀️",
                callback_data=f"Pages Back|0|{videoid}|{chat_id}",
            ),
            InlineKeyboardButton(
                text="🔙 Back",
                callback_data=f"MainMarkup {videoid}|{chat_id}",
            ),
            InlineKeyboardButton(
                text="▶️",
                callback_data=f"Pages Forw|0|{videoid}|{chat_id}",
            ),
        ],
    ]
    return buttons


def panel_markup_2(_, videoid, chat_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="🔇 Mute", callback_data=f"ADMIN Mute|{chat_id}"
            ),
            InlineKeyboardButton(
                text="🔊 Unmute",
                callback_data=f"ADMIN Unmute|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔀 Shuffle",
                callback_data=f"ADMIN Shuffle|{chat_id}",
            ),
            InlineKeyboardButton(
                text="🔁 Loop", callback_data=f"ADMIN Loop|{chat_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="◀️",
                callback_data=f"Pages Back|1|{videoid}|{chat_id}",
            ),
            InlineKeyboardButton(
                text="🔙 Back",
                callback_data=f"MainMarkup {videoid}|{chat_id}",
            ),
            InlineKeyboardButton(
                text="▶️",
                callback_data=f"Pages Forw|1|{videoid}|{chat_id}",
            ),
        ],
    ]
    return buttons


def panel_markup_3(_, videoid, chat_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="⏮ 10 Seconds",
                callback_data=f"ADMIN 1|{chat_id}",
            ),
            InlineKeyboardButton(
                text="⏭ 10 Seconds",
                callback_data=f"ADMIN 2|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="⏮ 30 Seconds",
                callback_data=f"ADMIN 3|{chat_id}",
            ),
            InlineKeyboardButton(
                text="⏭ 30 Seconds",
                callback_data=f"ADMIN 4|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="◀️",
                callback_data=f"Pages Back|2|{videoid}|{chat_id}",
            ),
            InlineKeyboardButton(
                text="🔙 Back",
                callback_data=f"MainMarkup {videoid}|{chat_id}",
            ),
            InlineKeyboardButton(
                text="▶️",
                callback_data=f"Pages Forw|2|{videoid}|{chat_id}",
            ),
        ],
    ]
    return buttons


def telegram_markup_timer(_, chat_id, played, dur, videoid):
    bar = random.choice(selection)
    buttons = [
        [
            InlineKeyboardButton(
                text=f"𝙆𝙐𝙈𝙎𝘼𝙇 𝘽𝙊𝙏𝙎 ", 
                url=f"https://t.me/the_team_kumsal"
            )
        ],

        [
            InlineKeyboardButton(
                text=_["PL_B_2"],
                callback_data=f"add_playlist {videoid}",
            ),
            InlineKeyboardButton(
                text=_["PL_B_3"],
                callback_data=f"PanelMarkup None|{chat_id}",
            ),
        ],
    ]
    return buttons


# Rest of the functions remain the same...



## Inline without Timer Bar


def stream_markup(_, videoid, chat_id):
    buttons = [
        [
            InlineKeyboardButton(
                text=f"𝙆𝙐𝙈𝙎𝘼𝙇 𝘽𝙊𝙏𝙎", 
                url=f"https://t.me/the_team_kumsal"
            )
        ],

        [
            InlineKeyboardButton(
                text=_["PL_B_2"],
                callback_data=f"add_playlist {videoid}",
            ),
            InlineKeyboardButton(
                text=_["PL_B_3"],
                callback_data=f"PanelMarkup None|{chat_id}",
            ),
        ],
    ]
    return buttons


def telegram_markup(_, chat_id):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["PL_B_3"],
                callback_data=f"PanelMarkup None|{chat_id}",
            ),
            InlineKeyboardButton(
                text=_["CLOSEMENU_BUTTON"], callback_data="close"
            ),
        ],
    ]
    return buttons


## Search Query Inline


def track_markup(_, videoid, user_id, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text=f"𝙆𝙐𝙈𝙎𝘼𝙇 𝘽𝙊𝙏𝙎", 
                url=f"https://t.me/the_team_kumsal"
            )
        ],

        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
    ]
    return buttons


def playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text=f"⚡ 𝙆𝙐𝙈𝙎𝘼𝙇 𝘽𝙊𝙏𝙎 ⚡", 
                url=f"https://t.me/the_team_kumsal"
            )
        ],

        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"ArchMusicPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"ArchMusicPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}",
            ),
        ],
    ]
    return buttons


## Live Stream Markup


def livestream_markup(_, videoid, user_id, mode, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_3"],
                callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["CLOSEMENU_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
            ),
        ],
    ]
    return buttons


## Slider Query Markup


def slider_markup(
    _, videoid, user_id, query, query_type, channel, fplay
):
    query = f"{query[:20]}"
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="❮",
                callback_data=f"slider B|{query_type}|{query}|{user_id}|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {query}|{user_id}",
            ),
            InlineKeyboardButton(
                text="❯",
                callback_data=f"slider F|{query_type}|{query}|{user_id}|{channel}|{fplay}",
            ),
        ],
    ]
    return buttons


## Cpanel Markup


def panel_markup_1(_, videoid, chat_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="⏸ Pause", callback_data=f"ADMIN Pause|{chat_id}"
            ),
            InlineKeyboardButton(
                text="▶️ Resume",
                callback_data=f"ADMIN Resume|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="⏯ Skip", callback_data=f"ADMIN Skip|{chat_id}"
            ),
            InlineKeyboardButton(
                text="⏹ Stop", callback_data=f"ADMIN Stop|{chat_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="◀️",
                callback_data=f"Pages Back|0|{videoid}|{chat_id}",
            ),
            InlineKeyboardButton(
                text="🔙 Back",
                callback_data=f"MainMarkup {videoid}|{chat_id}",
            ),
            InlineKeyboardButton(
                text="▶️",
                callback_data=f"Pages Forw|0|{videoid}|{chat_id}",
            ),
        ],
    ]
    return buttons


def panel_markup_2(_, videoid, chat_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="🔇 Mute", callback_data=f"ADMIN Mute|{chat_id}"
            ),
            InlineKeyboardButton(
                text="🔊 Unmute",
                callback_data=f"ADMIN Unmute|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔀 Shuffle",
                callback_data=f"ADMIN Shuffle|{chat_id}",
            ),
            InlineKeyboardButton(
                text="🔁 Loop", callback_data=f"ADMIN Loop|{chat_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="◀️",
                callback_data=f"Pages Back|1|{videoid}|{chat_id}",
            ),
            InlineKeyboardButton(
                text="🔙 Back",
                callback_data=f"MainMarkup {videoid}|{chat_id}",
            ),
            InlineKeyboardButton(
                text="▶️",
                callback_data=f"Pages Forw|1|{videoid}|{chat_id}",
            ),
        ],
    ]
    return buttons


def panel_markup_3(_, videoid, chat_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="⏮ 10 Seconds",
                callback_data=f"ADMIN 1|{chat_id}",
            ),
            InlineKeyboardButton(
                text="⏭ 10 Seconds",
                callback_data=f"ADMIN 2|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="⏮ 30 Seconds",
                callback_data=f"ADMIN 3|{chat_id}",
            ),
            InlineKeyboardButton(
                text="⏭ 30 Seconds",
                callback_data=f"ADMIN 4|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="◀️",
                callback_data=f"Pages Back|2|{videoid}|{chat_id}",
            ),
            InlineKeyboardButton(
                text="🔙 Back",
                callback_data=f"MainMarkup {videoid}|{chat_id}",
            ),
            InlineKeyboardButton(
                text="▶️",
                callback_data=f"Pages Forw|2|{videoid}|{chat_id}",
            ),
        ],
    ]
    return buttons