import math
from pyrogram.types import InlineKeyboardButton
from ArchMusic.utils.formatters import time_to_seconds


def get_progress_bar(percentage):
    """
    Yüzdeye göre 10 blokluk sade ilerleme çubuğu oluşturur.
    Sadece dolu bloklar gösterilir (), boş blok yok.
    """
    umm = min(math.floor(percentage / 10), 10)
    filled_blocks = "" * umm
    return f"{percentage:.0f}% {filled_blocks}"


def format_duration(duration):
    """
    Süreyi dakika: saniye formatında döndürür.
    Örn: 125 saniye -> 02:05
    """
    total_seconds = time_to_seconds(duration)
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes:02d}:{seconds:02d}"


# ---------- Stream Markup ----------

def stream_markup_timer(_, videoid, chat_id, played, dur):
    played_time = format_duration(played)
    total_time = format_duration(dur)
    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)
    percentage = (played_sec / duration_sec) * 100 if duration_sec else 0
    bar = get_progress_bar(percentage)

    buttons = [
        # Başlık
        

        # Süre barı
        [InlineKeyboardButton(text=f"{played_time} ❤️ {bar} {total_time}", callback_data="GetTimer")],

        

        # Alt satır
        [

        
            InlineKeyboardButton(text="🔮 Kontrol Paneli", callback_data=f"PanelMarkup None|{chat_id}"),
        ],
    ]
    return buttons



def stream_markup(_, videoid, chat_id):
    return []


# ---------- Telegram Markup ----------

def telegram_markup_timer(_, chat_id, played, dur):
    played_time = format_duration(played)
    total_time = format_duration(dur)
    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)
    percentage = (played_sec / duration_sec) * 100 if duration_sec else 0
    bar = get_progress_bar(percentage)

    buttons = [
        [InlineKeyboardButton(text=f"{played_time} {bar} {total_time}", callback_data="GetTimer")],
        [InlineKeyboardButton(text=_["PL_B_3"], callback_data=f"PanelMarkup None|{chat_id}")],
    ]
        return buttons


def telegram_markup(_, chat_id):
    buttons = [
        [InlineKeyboardButton(text=_["PL_B_3"], callback_data=f"PanelMarkup None|{chat_id}")],
          ]
    return buttons


# ---------- Track / Playlist / Live ----------

def track_markup(_, videoid, user_id, channel, fplay):
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
]
    return buttons


def playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"YukkiPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"YukkiPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}",
            ),

        ],
]
    return buttons


def livestream_markup(_, videoid, user_id, mode, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_3"],
                callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}",
            ),
            InlineKeyboardButton return buttons


# ---------- Slider ----------

def slider_markup(_, videoid, user_id, query, query_type, channel, fplay):
    query = query[:20]
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
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"forceclose {query}|{user_id}"),
            InlineKeyboardButton(
                text="❯",
                callback_data=f"slider F|{query_type}|{query}|{user_id}|{channel}|{fplay}",
            ),
        ],
    ]
    return buttons


# ---------- Panel Markup ----------

def panel_markup_1(_, videoid, chat_id):
    buttons = [
        [
            InlineKeyboardButton(text="⏸ Pause", callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton(text="▶️ Resume", callback_data=f"ADMIN Resume|{chat_id}"),
        ],
        [
            InlineKeyboardButton(text="⏯ Skip", callback_data=f"ADMIN Skip|{chat_id}"),
            InlineKeyboardButton(text="⏹ Stop", callback_data=f"ADMIN Stop|{chat_id}"),
        ],
        [InlineKeyboardButton(text="🔁 Replay", callback_data=f"ADMIN Replay|{chat_id}")],
        [
            InlineKeyboardButton(text="◀️", callback_data=f"Pages Back|0|{videoid}|{chat_id}"),
            InlineKeyboardButton(text="🔙 Back", callback_data=f"MainMarkup {videoid}|{chat_id}"),
            InlineKeyboardButton(text="▶️", callback_data=f"Pages Forw|0|{videoid}|{chat_id}"),
        ],
    ]
    return buttons


def panel_markup_2(_, videoid, chat_id):
    buttons = [
        [
            InlineKeyboardButton(text="🔇 Mute", callback_data=f"ADMIN Mute|{chat_id}"),
            InlineKeyboardButton(text="🔊 Unmute", callback_data=f"ADMIN Unmute|{chat_id}"),
        ],
        [
            InlineKeyboardButton(text="🔀 Shuffle", callback_data=f"ADMIN Shuffle|{chat_id}"),
            InlineKeyboardButton(text="🔁 Loop", callback_data=f"ADMIN Loop|{chat_id}"),
        ],
        [
            InlineKeyboardButton(text="◀️", callback_data=f"Pages Back|1|{videoid}|{chat_id}"),
            InlineKeyboardButton(text="🔙 Back", callback_data=f"MainMarkup {videoid}|{chat_id}"),
            InlineKeyboardButton(text="▶️", callback_data=f"Pages Forw|1|{videoid}|{chat_id}"),
        ],
    ]
    return buttons


def panel_markup_3(_, videoid, chat_id):
    buttons = [
        [
            InlineKeyboardButton(text="⏮ 10 seconds", callback_data=f"ADMIN 1|{chat_id}"),
            InlineKeyboardButton(text="⏭ 10 seconds", callback_data=f"ADMIN 2|{chat_id}"),
        ],
        [
            InlineKeyboardButton(text="⏮ 30 seconds", callback_data=f"ADMIN 3|{chat_id}"),
            InlineKeyboardButton(text="⏭ 30 seconds", callback_data=f"ADMIN 4|{chat_id}"),
        ],
        [
            InlineKeyboardButton(text="◀️", callback_data=f"Pages Back|2|{videoid}|{chat_id}"),
            InlineKeyboardButton(text="🔙 Back", callback_data=f"MainMarkup {videoid}|{chat_id}"),
            InlineKeyboardButton(text="▶️", callback_data=f"Pages Forw|2|{videoid}|{chat_id}"),
        ],
    ]
    return buttons
