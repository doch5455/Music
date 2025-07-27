# Copyright (C) 2021-2023 by ArchBots@Github, <https://github.com/ArchBots>.
# This file is part of <https://github.com/ArchBots/ArchMusic> project,
# and is released under the "GNU v3.0 License Agreement".
# Please see <https://github.com/ArchBots/ArchMusic/blob/master/LICENSE>
#
# All rights reserved.

from typing import Union
from pyrogram.types import InlineKeyboardButton
from config import GITHUB_REPO, SUPPORT_CHANNEL, SUPPORT_GROUP
from ArchMusic import app
14: from ArchMusic import app
15: InlineKeyboardButton(text=_["CLOSEMENU_BUTTON"], callback_data="close")

        [
            InlineKeyboardButton(
                text=strings["S_B_1"],
                url=f"https://t.me/{app.username}?start=help"
            ),
            InlineKeyboardButton(
                text=strings["S_B_2"],
                callback_data="settings_helper"
            ),
        ]
    ]

    support_buttons = []
    if SUPPORT_CHANNEL:
        support_buttons.append(
            InlineKeyboardButton(
                text=strings["S_B_4"],
                url=SUPPORT_CHANNEL
            )
        )
    if SUPPORT_GROUP:
        support_buttons.append(
            InlineKeyboardButton(
                text=strings["S_B_3"],
                url=SUPPORT_GROUP
            )
        )
    if support_buttons:
        buttons.append(support_buttons)

    return buttons


def private_panel(strings: dict, bot_username: str, owner: Union[bool, int] = None):
    buttons = [
        [
            InlineKeyboardButton(
                text=strings["S_B_8"],
                callback_data="settings_back_helper"
            )
        ]
    ]

    support_buttons = []
    if SUPPORT_CHANNEL:
        support_buttons.append(
            InlineKeyboardButton(
                text=strings["S_B_4"],
                url=SUPPORT_CHANNEL
            )
        )
    if SUPPORT_GROUP:
        support_buttons.append(
            InlineKeyboardButton(
                text=strings["S_B_3"],
                url=SUPPORT_GROUP
            )
        )
    if support_buttons:
        buttons.append(support_buttons)

    buttons.append(
        [
            InlineKeyboardButton(
                text=strings["S_B_5"],
                url=f"https://t.me/{bot_username}?startgroup=true"
            )
        ]
    )

    # GitHub veya Owner bilgisi varsa, gerekli düğmeleri ekle
    extra_buttons = []
    if GITHUB_REPO:
        extra_buttons.append(
            InlineKeyboardButton(
                text=strings["S_B_6"],
                url=GITHUB_REPO
            )
        )
    if owner:
        extra_buttons.append(
            InlineKeyboardButton(
                text=strings["S_B_7"],
                user_id=owner
            )
        )
    if extra_buttons:
        buttons.append(extra_buttons)

    return buttons
