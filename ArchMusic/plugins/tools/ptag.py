import random
from pyrogram import filters
from pyrogram.types import Message
from config import BANNED_USERS
from ArchMusic import app

# 50 adet güzel söz
GUZEL_SOZLER = [
    "Sen bir yıldızsın, ışığınla parlıyorsun 🌟",
    "Gülüşün bu dünyaya armağan 😄",
    "Seninle konuşmak huzur veriyor 🕊️",
    "Kalbin kadar güzel birini tanımadım 💖",
    "Senin gibi biri iyi ki var 💫",
    "Sözlerinle içimizi ısıtıyorsun ☀️",
    "Her hâlinle özelsin ✨",
    "Senin varlığın mutluluk kaynağı 😊",
    "Bir tebessümün bile yeter 🌸",
    "Sen olduğun gibi çok güzelsin 💐",
    "Kalbinin güzelliği yüzüne yansımış 😍",
    "Senin dostluğun paha biçilemez 💎",
    "Sen varsan dünya daha güzel 🌍",
    "Senin olduğun yer huzur dolu 🏞️",
    "Gözlerin bir şiir gibi 📖",
    "Senin enerjin etrafı aydınlatıyor 💡",
    "Sıcacık gülüşün içimizi ısıtıyor 🔥",
    "Sen anlatılmaz, yaşanırsın 💌",
    "İyilik seninle anlam kazanıyor 🤲",
    "Düşüncelerinle ilham veriyorsun 🧠",
    "Senin gibi biri bu dünyaya renk katıyor 🌈",
    "Sen her şeyin en güzeline layıksın 👑",
    "Senin samimiyetin kalbe dokunuyor 💓",
    "Varlığın en büyük hediyelerden biri 🎁",
    "Seninle zaman su gibi akıyor ⏳",
    "Senin ışığın karanlıkları aydınlatıyor 🕯️",
    "Kalbin sevgiyle dolu bir liman ⚓",
    "Senin sözlerin yaralara merhem 💭",
    "Sen özel değil, eşsizsin 🌟",
    "Seninle olmak en güzel yolculuk ✈️",
    "Senin adın huzurla anılıyor ☁️",
    "Sen sevgiyle atan bir kalpsin ❤️",
    "Seninle geçirilen anlar unutulmaz 📸",
    "İyiliğin en saf hali sensin 💧",
    "Sen gönül bahçemizin en nadide çiçeğisin 🌷",
    "Senin yanında kendimi değerli hissediyorum 💫",
    "Seninle konuşmak bile terapi gibi 🧘",
    "Gözlerin yıldız, sözlerin masal 🌌",
    "Senin gibi biri hayatımda olduğu için şanslıyım 🍀",
    "Sözlerinde umut, bakışlarında sevgi var ☀️",
    "Senin gülüşün karanlık günlerin güneşi ☀️",
    "Duruşunla bile insanlara ilham veriyorsun ✨",
    "Senin sevgin bir şairin ilhamı kadar derin 🎨",
    "İyilik seninle anlam buluyor 🧿",
    "Gülüşünde çocuk saflığı var 🧸",
    "Senin yanında kendimi güvende hissediyorum 🛡️",
    "Sen hayatın bana sunduğu en güzel sürprizsin 🎁",
    "Seninle olmak kalbin ritmini duymak gibi 🔊",
    "Sen sadece bir isim değil, bir anlam taşıyorsun 🧡",
    "Senin güzelliğin içinden geliyor 🔥"
]

@app.on_message(filters.command("ptag") & filters.group & ~BANNED_USERS)
async def tekli_guzel_soz(client, message: Message):
    if len(message.command) == 1:
        return await message.reply("Bir kullanıcı belirtmelisin: `/ptag @kullanici`", quote=True)

    etiket_sayisi = 0
    basarisiz_sayisi = 0
    etiket_sirasi = 0

    try:
        kullanici_adi = message.text.split()[1]
        user = await client.get_users(kullanici_adi)
        soz = random.choice(GUZEL_SOZLER)
        await message.reply(
            f"{soz} [{user.first_name}](tg://user?id={user.id})",
            quote=True
        )
        etiket_sayisi += 1
        etiket_sirasi += 1
    except Exception:
        basarisiz_sayisi += 1
        await message.reply("❌ Kullanıcıyı bulamadım veya etiket hatalı.", quote=True)

    toplam = etiket_sayisi + basarisiz_sayisi

    await message.reply(
        f"✅ Etiketlenen: `{etiket_sayisi}`\n"
        f"❌ Atlanılan: `{basarisiz_sayisi}`\n"
        f"🏁 Biten Toplam İşlem: `{toplam}`\n"
        f"🔢 Etiket sırası: `{etiket_sirasi}`"
    )


@app.on_message(filters.command("cancel_ptag") & filters.group & ~BANNED_USERS)
async def cancel_ptag(client, message: Message):
    await message.reply("🔹 Tekli etiketleme anlık çalışır, iptal edilecek işlem yok.")
