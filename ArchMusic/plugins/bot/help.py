# Copyright (C) 2021-2023 by ArchBots@Github, < https://github.com/ArchBots >
# This file is part of < https://github.com/ArchBots/ArchMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/ArchBots/ArchMusic/blob/master/LICENSE >

from typing import Union

from pyrogram import filters, types
from pyrogram.types import InlineKeyboardMarkup, Message

from config import BANNED_USERS
from strings import get_command, get_string, helpers
from ArchMusic import app
from ArchMusic.misc import SUDOERS
from ArchMusic.utils import help_pannel
from ArchMusic.utils.database import get_lang, is_commanddelete_on
from ArchMusic.utils.decorators.language import LanguageStart, languageCB
from ArchMusic.utils.inline.help import help_back_markup, private_help_panel

# Komut sabiti
HELP_COMMAND = get_command("HELP_COMMAND")


# Özel sohbette yardım komutu veya geri dönüş butonu
@app.on_message(filters.command(HELP_COMMAND) & filters.private & ~BANNED_USERS)
@app.on_callback_query(filters.regex("settings_back_helper") & ~BANNED_USERS)
async def helper_private(client: app, update: Union[types.Message, types.CallbackQuery]):
    is_callback = isinstance(update, types.CallbackQuery)

    if is_callback:
        try:
            await update.answer()
        except Exception as e:
            print(f"Callback cevaplanamadı: {e}")
        
        chat_id = update.message.chat.id
        language = await get_lang(chat_id)
        _ = get_string(language)
        keyboard = help_pannel(_, private=True)

        # Fotoğraf varsa sil ve tekrar gönder
        if update.message.photo:
            await update.message.delete()
            await update.message.reply_text(_["help_1"], reply_markup=keyboard)
        else:
            await update.edit_message_text(_["help_1"], reply_markup=keyboard)
    
    else:
        chat_id = update.chat.id

        if await is_commanddelete_on(chat_id):
            try:
                await update.delete()
            except Exception as e:
                print(f"Mesaj silinemedi: {e}")
        
        language = await get_lang(chat_id)
        _ = get_string(language)
        keyboard = help_pannel(_)

        await update.reply_text(_["help_1"], reply_markup=keyboard)


# Grup sohbetinde yardım komutu
@app.on_message(filters.command(HELP_COMMAND) & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_com_group(client, message: Message, _):
    keyboard = private_help_panel(_)
    await message.reply_text(_["help_2"], reply_markup=InlineKeyboardMarkup(keyboard))


# Yardım paneli içinde gezinme (callback işlemleri)
@app.on_callback_query(filters.regex("help_callback") & ~BANNED_USERS)
@languageCB
async def helper_cb(client, callback: types.CallbackQuery, _):
    try:
        await callback.answer()
    except Exception as e:
        print(f"Callback cevabı hatalı: {e}")

    # Güvenli ayrıştırma
    parts = callback.data.strip().split(None, 1)
    if len(parts) < 2:
        return await callback.answer("Geçersiz yardım isteği!", show_alert=True)

    cb = parts[1]
    keyboard = help_back_markup(_)

    # Sadece sudo kullanıcıları için
    if cb == "hb7":
        if callback.from_user.id not in SUDOERS:
            return await callback.answer("Sadece Sudo Kullanıcıları İçin", show_alert=True)
        await callback.edit_message_text(helpers.HELP_7, reply_markup=keyboard)
        return

    # Yardım kategorileri
    help_sections = {
        "hb1": helpers.HELP_1,
        "hb2": helpers.HELP_2,
        "hb3": helpers.HELP_3,
        "hb4": helpers.HELP_4,
        "hb5": helpers.HELP_5,
        "hb6": helpers.HELP_6,
        "hb8": helpers.HELP_8,
        "hb9": helpers.HELP_9,
    }

    if cb in help_sections:
        await callback.edit_message_text(help_sections[cb], reply_markup=keyboard)
    else:
        await callback.answer("Bilinmeyen yardım bölümü!", show_alert=True)
