# Mevcut projeyi yedekle veya sil
rm -rf o

# ArchMusic botu klonla
git clone https://github.com/ArchBots/ArchMusic.git

cd ArchMusic

# Gereken paketleri kur
pip install -r requirements.txt

# Botu başlat
python3 main.py
