from typing import Union, Dict
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ArchMusic import app

def get_close_button(text: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(text=text, callback_data="close")

def get_back_button(text: str, callback: str = "settingsback_helper") -> InlineKeyboardButton:
    return InlineKeyboardButton(text=text, callback_data=callback)

def help_panel(localized: Dict[str, str], START: Union[bool, int] = None):
    help_keys = [
        "H_B_1", "H_B_2", "H_B_3", "H_B_4",
        "H_B_5", "H_B_6", "H_B_7", "H_B_8", "H_B_9"
    ]

    buttons = []

    # Otomatik 2’li gruplama
    for i in range(0, len(help_keys), 2):
        row = []
        for j in range(2):
            if i + j < len(help_keys):
                key = help_keys[i + j]
                row.append(
                    InlineKeyboardButton(
                        text=localized.get(key, key),
                        callback_data=f"help_callback {key.lower()}"
                    )
                )
        buttons.append(row)

    # Navigasyon satırı
    nav_row = (
        [
            get_back_button(localized.get("BACK_BUTTON", "⬅️ Geri")),
            get_close_button(localized.get("CLOSEMENU_BUTTON", "❌ Kapat")),
        ]
        if START else [get_close_button(localized.get("CLOSEMENU_BUTTON", "❌ Kapat"))]
    )

    buttons.append(nav_row)
    return InlineKeyboardMarkup(buttons)
