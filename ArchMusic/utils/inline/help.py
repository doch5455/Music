# Copyright (C) 2021-2023 by ArchBots
# License: GNU v3.0 License (see https://github.com/ArchBots/ArchMusic/blob/master/LICENSE)

from typing import Union, Dict
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ArchMusic import app

# Reusable buttons
def get_close_button(text: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(text=text, callback_data="close")

def get_back_button(text: str, callback: str = "settings_back_helper") -> InlineKeyboardButton:
    return InlineKeyboardButton(text=text, callback_data=callback)


def help_panel(localized: Dict[str, str], START: Union[bool, int] = None):
    # Define navigation row based on START flag
    nav_row = [
        get_back_button(localized["BACK_BUTTON"], "settingsback_helper"),
        get_close_button(localized["CLOSEMENU_BUTTON"]),
    ] if START else [get_close_button(localized["CLOSEMENU_BUTTON"])]

    # Help topic buttons
    help_buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text=localized["H_B_1"], callback_data="help_callback hb1"),
            InlineKeyboardButton(text=localized["H_B_2"], callback_data="help_callback hb2"),
        ],
        [
            InlineKeyboardButton(text=localized["H_B_3"], callback_data="help_callback hb3"),
            InlineKeyboardButton(text=localized["H_B_4"], callback_data="help_callback hb4"),
        ],
        [
            InlineKeyboardButton(text=localized["H_B_5"], callback_data="help_callback hb5"),
            InlineKeyboardButton(text=localized["H_B_6"], callback_data="help_callback hb6"),
        ],
        [
            InlineKeyboardButton(text=localized["H_B_7"], callback_data="help_callback hb7"),
            InlineKeyboardButton(text=localized["H_B_8"], callback_data="help_callback hb8"),
        ],
        [
            InlineKeyboardButton(text=localized["H_B_9"], callback_data="help_callback hb9"),
        ],
        nav_row,
    ])
    return help_buttons


def help_back_markup(localized: Dict[str, str]):
    return InlineKeyboardMarkup([
        [
            get_back_button(localized["BACK_BUTTON"]),
            get_close_button(localized["CLOSE_BUTTON"]),
        ]
    ])


def private_help_panel(localized: Dict[str, str]):
    return [
        [
            InlineKeyboardButton(
                text=localized["S_B_1"],
                url=f"https://t.me/{app.username}?start=help",
            )
        ]
    ]
