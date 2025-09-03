from typing import Union

# -------------------------
# ZAMAN DÖNÜŞÜM FONKSİYONLARI
# -------------------------

def okunabilir_zaman(saniye: int) -> str:
    """
    Saniyeyi okunabilir zaman formatına çevirir.
    Örnek: 3661 -> "1h:1m:1s"
    """
    sayac = 0
    zaman_str = ""
    zaman_listesi = []
    zaman_ekleri = ["s", "m", "h", "gün"]

    while sayac < 4:
        sayac += 1
        if sayac < 3:
            kalan, sonuc = divmod(saniye, 60)
        else:
            kalan, sonuc = divmod(saniye, 24)
        if saniye == 0 and kalan == 0:
            break
        zaman_listesi.append(int(sonuc))
        saniye = int(kalan)

    for i in range(len(zaman_listesi)):
        zaman_listesi[i] = str(zaman_listesi[i]) + zaman_ekleri[i]

    if len(zaman_listesi) == 4:
        zaman_str += zaman_listesi.pop() + ", "

    zaman_listesi.reverse()
    zaman_str += ":".join(zaman_listesi)
    return zaman_str


def zaman_saniyeye(zaman: str) -> int:
    """
    "hh:mm:ss" formatındaki zamanı toplam saniyeye çevirir.
    Örnek: "01:02:03" -> 3723
    """
    return sum(
        int(x) * 60**i
        for i, x in enumerate(reversed(str(zaman).split(":")))
    )


def saniye_dakikaya(saniye: Union[int, None]) -> str:
    """
    Saniyeyi dd:hh:mm:ss formatına çevirir.
    Örnek: 3661 -> "01:01:01"
    """
    if saniye is not None:
        saniye = int(saniye)
        gun, saat, dakika, saniye_kalan = (
            saniye // (3600 * 24),
            saniye // 3600 % 24,
            saniye % 3600 // 60,
            saniye % 3600 % 60,
        )
        if gun > 0:
            return "{:02d}:{:02d}:{:02d}:{:02d}".format(gun, saat, dakika, saniye_kalan)
        elif saat > 0:
            return "{:02d}:{:02d}:{:02d}".format(saat, dakika, saniye_kalan)
        elif dakika > 0:
            return "{:02d}:{:02d}".format(dakika, saniye_kalan)
        elif saniye_kalan > 0:
            return "00:{:02d}".format(saniye_kalan)
    return "-"


# -------------------------
# BOYUT DÖNÜŞÜM FONKSİYONLARI
# -------------------------

def bayt_cevir(boyut: float) -> str:
    """
    Bayt değerini okunabilir KiB, MiB, GiB gibi birimlere çevirir.
    Örnek: 1048576 -> "1.00 MiB"
    """
    if not boyut:
        return "0 B"
    katsayi = 1024
    seviye = 0
    birimler = {0: "B", 1: "KiB", 2: "MiB", 3: "GiB", 4: "TiB"}

    while boyut >= katsayi and seviye < 4:
        boyut /= katsayi
        seviye += 1
    return "{:.2f} {}".format(boyut, birimler[seviye])


# -------------------------
# SAYI <-> HARF DÖNÜŞÜM FONKSİYONLARI
# -------------------------

def sayiyi_harfle(user_id: int) -> str:
    """
    Sayısal kullanıcı ID'sini harf koduna çevirir.
    Örnek: 123 -> "bcd"
    """
    alfabe = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    metin = ""
    user_id = str(user_id)
    for rakam in user_id:
        metin += alfabe[int(rakam)]
    return metin


def harfi_sayiya(user_id_harf: str) -> int:
    """
    Harf kodunu sayısal kullanıcı ID'sine çevirir.
    Örnek: "bcd" -> 123
    """
    alfabe = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    user_id = ""
    for harf in user_id_harf:
        index = alfabe.index(harf)
        user_id += str(index)
    return int(user_id)


def int_to_alpha(n: int) -> str:
    """
    Tam sayıyı alfabetik koda çevirir.
    Örnek: 0 -> "A", 25 -> "Z", 26 -> "AA"
    """
    if n < 0:
        raise ValueError("Sayı negatif olamaz")
    result = ""
    while n >= 0:
        result = chr(n % 26 + ord("A")) + result
        n = n // 26 - 1
    return result


# -------------------------
# DESTEKLENEN FORMATLAR
# -------------------------

formatlar = [
    "webm", "mkv", "flv", "vob", "ogv", "ogg", "rrc", "gifv", "mng",
    "mov", "avi", "qt", "wmv", "yuv", "rm", "asf", "amv", "mp4", "m4p",
    "m4v", "mpg", "mp2", "mpeg", "mpe", "mpv", "svi", "3gp", "3g2",
    "mxf", "roq", "nsv", "f4v", "f4p", "f4a", "f4b",
]

