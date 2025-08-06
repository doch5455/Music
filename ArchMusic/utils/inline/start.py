  
from pyrogram import Client, filters
from pyrogram.types import Message

BOT_USERNAME = "YourBotUsername"  # Buraya kendi bot kullanıcı adını yaz

@Client.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    from ArchMusic.utils.inline.start import start_panel  # fonksiyon içi import, döngüyü önler

    _ = {
        "S_B_1": "Yardım",
        "S_B_2": "Ayarlar",
        "S_B_3": "Destek Grubu",
        "S_B_4": "Destek Kanalı",
        "S_B_5": "Gruba Ekle",
        "S_B_6": "GitHub",
        "S_B_7": "Sahip",
        "S_B_8": "Geri"
    }

    buttons = start_panel(_)

    await message.reply_text(
        "Hoşgeldin! Yardım almak için aşağıdaki butonları kullanabilirsin.",
        reply_markup=buttons
    )
