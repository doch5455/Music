from typing import Union, Optional
from pyrogram.types import InlineKeyboardButton
from config import GITHUB_REPO, SUPPORT_CHANNEL, SUPPORT_GROUP
from ArchMusic import app


def start_pannel(_):
    buttons = [
        [
            InlineKeyboardButton(text=f"🟦 {_[ 'S_B_1' ]}", url=f"https://t.me/{app.username}?start=help"),
            InlineKeyboardButton(text=f"🟨 {_[ 'S_B_2' ]}", callback_data="settings_helper"),
        ]
    ]

    support_row = _get_support_buttons(_)
    if support_row:
        buttons.append(support_row)

    return buttons


def private_panel(
    _: dict,
    BOT_USERNAME: str,
    OWNER: Union[bool, int] = None,
    header_text: Optional[str] = "📌 Menuden istediğin işlemi seç"
):
    buttons = []

    # Opsiyonel başlık satırı (tıklanabilir callback)
    if header_text:
        buttons.append([
            InlineKeyboardButton(text=header_text, callback_data="header")
        ])

    # 1. Satır: Geri butonu
    buttons.append([
        InlineKeyboardButton(text=f"🔙 {_[ 'S_B_8' ]}", callback_data="settings_back_helper")
    ])

    # 2. Satır: Destek grubu & kanal
    support_row = _get_support_buttons(_)
    if support_row:
        buttons.append(support_row)

    # 3. Satır: Grup ekle
    buttons.append([
        InlineKeyboardButton(
            text=f"🟢 {_[ 'S_B_5' ]}",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true"
        )
    ])

    # 4. Satır: GitHub & Owner
    final_row = []
    if GITHUB_REPO:
        final_row.append(
            InlineKeyboardButton(text=f"🟣 {_[ 'S_B_6' ]}", url=GITHUB_REPO)
        )
    if OWNER:
        final_row.append(
            InlineKeyboardButton(text=f"🔴 {_[ 'S_B_7' ]}", user_id=OWNER)
        )
    if final_row:
        buttons.append(final_row)

    return buttons


def _get_support_buttons(_):
    """Destek butonlarını tek satırda döndürür."""
    row = []
    if SUPPORT_GROUP:
        row.append(InlineKeyboardButton(text=f"🟩 {_[ 'S_B_3' ]}", url=SUPPORT_GROUP))
    if SUPPORT_CHAN_
