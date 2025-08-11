from typing import Union
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from ArchMusic import app


def help_pannel(_, START: Union[bool, int] = None):
    """
    Yardım paneli butonlarını döndürür.
    START parametresi True ise geri butonu da eklenir.
    """

    # Son satırdaki kontrol butonları (geri/kapat)
    control_buttons = [
        InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="settingsback_helper"),
        InlineKeyboardButton(text=_["CLOSEMENU_BUTTON"], callback_data="close"),
    ] if START else [
        InlineKeyboardButton(text=_["CLOSEMENU_BUTTON"], callback_data="close")
    ]

    # Yardım butonları verisi
    button_data = [
        ("H_B_1", "hb1"), ("H_B_2", "hb2"),
        ("H_B_3", "hb3"), ("H_B_4", "hb4"),
        ("H_B_5", "hb5"), ("H_B_6", "hb6"),
        ("H_B_7", "hb7"), ("H_B_8", "hb8"),
        ("H_B_9", "hb9"),
    ]

    # Butonları 3'lü gruplar halinde satırlara yerleştir
    keyboard = []
    for i in range(0, len(button_data), 3):
        row = []
        for j in range(3):
            if i + j < len(button_data):
                text_key, cb_key = button_data[i + j]
                row.append(
                    InlineKeyboardButton(text=_[text_key], callback_data=f"help_callback {cb_key}")
                )
        keyboard.append(row)

    # Kontrol butonunu ekle
    keyboard.append(control_buttons)

    return InlineKeyboardMarkup(keyboard)


def help_back_markup(_):
    """
    Yardım alt menüsünde geri ve kapat butonlarını döndürür.
    """
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"], callback_data="settings_back_helper"
                ),
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"], callback_data="close"
                ),
            ]
        ]
    )


def private_help_panel(_):
    """
    Özel mesajlarda gösterilecek yardım ve geri butonlarını döndürür.
    Kullanıcıyı botla özelde yardıma yönlendirir.
    """
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["S_B_1"],
                    url=f"https://t.me/{app.username}?start=help",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"], callback_data="settingsback_helper"
                ),
                InlineKeyboardButton(
                    text=_["CLOSEMENU_BUTTON"], callback_data="close"
                ),
            ]
        ]
    )
