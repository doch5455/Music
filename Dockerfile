# Base image: Python + Node.js
FROM nikolaik/python-nodejs:python3.10-nodejs19-bullseye

# Sistem bağımlılıklarını yükle
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       ffmpeg \
       build-essential \
       libffi-dev \
       libssl-dev \
       python3-dev \
       git \
       wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Çalışma dizinini ayarla
WORKDIR /app

# Önce sadece requirements.txt’i kopyala, böylece cache kullanılabilir
COPY requirements.txt .

# Pip güncelle ve paketleri yükle
RUN python3 -m pip install --upgrade pip \
    && pip3 install --no-cache-dir -U -r requirements.txt

# Sonra tüm uygulama dosyalarını kopyala
COPY . .

# Başlatma komutu
CMD ["bash", "start"]
