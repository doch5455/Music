import random
from pyrogram import filters
from pyrogram.types import Message
from config import BANNED_USERS
from ArchMusic import app

# Slap (tokat) mesajları listesi
SLAP_TEXTS = [
    "👋 {user1}, {user2}'ye öyle bir tokat attı ki yankısı hâlâ duyuluyor!",
    "😤 {user1}, {user2}'ye ninja gibi sessiz bir tokat attı!",
    "🔥 {user1}, {user2}'ye uçan tekme niyetine tokat attı!",
    "🤣 {user1}, {user2}'yi tokat manyağı yaptı!",
    "💥 {user1}, {user2}'yi uzaya fırlatacak bir tokat attı!",
    "⚡ {user1}, {user2}'yi şimşek gibi çaktı!",
    "🥊 {user1}, {user2}'ye profesyonel boksör gibi vurdu!",
    "😈 {user1}, {user2}'ye 'akıllansın' diye tokat yapıştırdı!"
]

# /slap komutu — bir kullanıcıya tokat atar
@app.on_message(filters.command("slap") & filters.group & ~BANNED_USERS)
async def slap(client, message: Message):
    if len(message.command) < 2:
        return await message.reply("Bir kullanıcıyı etiketlemelisin: `/slap @kullanici`")

    try:
        hedef_username = message.command[1]
        hedef = await client.get_users(hedef_username)
        slap_text = random.choice(SLAP_TEXTS)

        await message.reply(
            slap_text.format(
                user1=f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})",
                user2=f"[{hedef.first_name}](tg://user?id={hedef.id})"
            ),
            quote=False
        )
    except Exception as e:
        await message.reply(f"❌ Kullanıcı bulunamadı veya bir hata oluştu.\n\n`{e}`")
