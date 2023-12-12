# Python resmi imajını kullanarak başlayın
FROM python:3.11

# Çalışma dizinini belirleyin
WORKDIR /app



# Uygulama dosyalarını kopyalayın
COPY chatserver_server.py chatserver_server.py

# Sunucu başlatma komutunu belirtin
CMD ["python", "chatserver_server.py"]
