import random
from pyrogram.types import InlineKeyboardButton

selection = [
    "▁▄▂▇▄▅▄▅▃",
    "▁▃▇▂▅▇▄▅▃",
    "▃▁▇▂▅▃▄▃▅",
    "▃▄▂▄▇▅▃▅▁",
    "▁▃▄▂▇▃▄▅▃",
    "▃▁▄▂▅▃▇▃▅",
    "▁▇▄▂▅▄▅▃▄",
    "▁▃▅▇▂▅▄▃▇",
    "▃▅▂▅▇▁▄▃▁",
    "▇▅▂▅▃▄▃▁▃",
    "▃▇▂▅▁▅▄▃▁",
    "▅▄▇▂▅▂▄▇▁",
    "▃▅▂▅▃▇▄▅▃",
]

# 🔹 Basit zaman dönüştürücü
def time_to_sec(time_str):
    parts = list(map(int, time_str.split(":")))
    return parts[0] * 60 + parts[1] if len(parts) == 2 else 0


# ───────────────────────────────
# 🎧 Stream oynatma (YouTube vb.)
# ───────────────────────────────
def stream_markup_timer(_, videoid, chat_id, played, dur):
    played_sec = time_to_sec(played)
    total_sec = time_to_sec(dur) or 1
    ratio = played_sec / total_sec
    pos = int(ratio * 8)

    bar_symbols = ["➖"] * 8
    pos = min(pos, len(bar_symbols) - 1)
    bar_symbols[pos] = "🔘"
    bar = "".join(bar_symbols)

    buttons = [
        [InlineKeyboardButton("🩵 Mavi Duyuru", url="https://t.me/MaviDuyuru")],
        [InlineKeyboardButton(f"{played} ⟪ {bar} ⟫ {dur}", callback_data="nonclickable")],
        [
            InlineKeyboardButton("⏮", callback_data=f"ADMIN_1|{chat_id}"),
            InlineKeyboardButton("⏸", callback_data=f"pausevc|{chat_id}"),
            InlineKeyboardButton("▶️", callback_data=f"resumevc|{chat_id}"),
            InlineKeyboardButton("⏭", callback_data=f"ADMIN_2|{chat_id}"),
            InlineKeyboardButton("⏹", callback_data=f"stopvc|{chat_id}"),
        ],
        [
            InlineKeyboardButton("✅ Listeye Ekle", callback_data=f"add_playlist {videoid}"),
            InlineKeyboardButton("🔮 Kontrol Paneli", callback_data=f"PanelMarkup None|{chat_id}"),
        ],
    ]
    return buttons


# ───────────────────────────────
# 🌀 Telegram stream oynatma
# ───────────────────────────────
def telegram_markup_timer(_, chat_id, played, dur, videoid):
    played_sec = time_to_sec(played)
    total_sec = time_to_sec(dur) or 1
    ratio = played_sec / total_sec
    pos = int(ratio * 8)

    bar_symbols = ["➖"] * 8
    pos = min(pos, len(bar_symbols) - 1)
    bar_symbols[pos] = "🔘"
    bar = "".join(bar_symbols)

    buttons = [
        [InlineKeyboardButton("🩵 Mavi Duyuru", url="https://t.me/MaviDuyuru")],
        [InlineKeyboardButton(f"{played} ⟪ {bar} ⟫ {dur}", callback_data="nonclickable")],
        [
            InlineKeyboardButton("⏮", callback_data=f"ADMIN_1|{chat_id}"),
            InlineKeyboardButton("⏸", callback_data=f"pausevc|{chat_id}"),
            InlineKeyboardButton("▶️", callback_data=f"resumevc|{chat_id}"),
            InlineKeyboardButton("⏭", callback_data=f"ADMIN_2|{chat_id}"),
            InlineKeyboardButton("⏹", callback_data=f"stopvc|{chat_id}"),
        ],
        [
            InlineKeyboardButton("✅ Listeye Ekle", callback_data=f"add_playlist {videoid}"),
            InlineKeyboardButton("🔮 Kontrol Paneli", callback_data=f"PanelMarkup None|{chat_id}"),
        ],
    ]
    return buttons


# ───────────────────────────────
# Inline without Timer Bar
# ───────────────────────────────
def stream_markup(_, videoid, chat_id):
    buttons = [
        [InlineKeyboardButton("🩵 Mavi Duyuru", url="https://t.me/MaviDuyuru")],
        [
            InlineKeyboardButton(text=_["PL_B_2"], callback_data=f"add_playlist {videoid}"),
            InlineKeyboardButton(text=_["PL_B_3"], callback_data=f"PanelMarkup None|{chat_id}"),
        ],
    ]
    return buttons


def telegram_markup(_, chat_id):
    buttons = [
        [
            InlineKeyboardButton(text=_["PL_B_3"], callback_data=f"PanelMarkup None|{chat_id}"),
            InlineKeyboardButton(text=_["CLOSEMENU_BUTTON"], callback_data="close"),
        ],
    ]
    return buttons


# ───────────────────────────────
# 🔍 Arama / Track seçimi
# ───────────────────────────────
def track_markup(_, videoid, user_id, channel, fplay):
    buttons = [
        [InlineKeyboardButton("🩵 Mavi Duyuru", url="https://t.me/MaviDuyuru")],
        [
            InlineKeyboardButton(
                text=_["P_B_1"], callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}"
            ),
            InlineKeyboardButton(
                text=_["P_B_2"], callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}"
            ),
        ],
    ]
    return buttons


# ───────────────────────────────
# 📜 Playlist Markup
# ───────────────────────────────
def playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    buttons = [
        [InlineKeyboardButton("🩵 Mavi Duyuru", url="https://t.me/MaviDuyuru")],
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


# ───────────────────────────────
# 📺 Canlı Yayın Menüsü
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
        [InlineKeyboardButton("🩵 Mavi Duyuru", url="https://t.me/MaviDuyuru")],
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


def telegram_markup_timer(_, chat_id, played, dur, videoid):
    bar = random.choice(selection)
    buttons = [
        [
            InlineKeyboardButton(
                text="🩵 Mavi Duyuru",
                url="https://t.me/MaviDuyuru"
            ),
            InlineKeyboardButton(
                text="🗑️ Kapat",
                callback_data="close"
            ),
        ],
    ]
    return buttons



def stream_markup(_, videoid, chat_id, played="00:00", total="03:00"):
    # 🔹 Basit ilerleme çubuğu
    parts_p = list(map(int, played.split(":")))
    parts_t = list(map(int, total.split(":")))
    played_sec = parts_p[0] * 60 + parts_p[1] if len(parts_p) == 2 else 0
    total_sec = parts_t[0] * 60 + parts_t[1] if len(parts_t) == 2 else 1
    ratio = played_sec / total_sec
    pos = int(ratio * 10)
    bar = "".join("🔹" if i == pos else "⠂" for i in range(10))
    bar_text = f"{played}  {bar}  {total}"

    # 🔘 Butonlar
    buttons = [
        [InlineKeyboardButton(text=bar_text, callback_data="nonclickable")],
        [
            InlineKeyboardButton(
                text="🩵 𝗞𝗮𝗻𝗮𝗹",
                url="https://t.me/MaviDuyuru"
            ),
            InlineKeyboardButton(
                text="🗑️ 𝗞𝗮𝗽𝗮𝘁",
                callback_data="close"
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