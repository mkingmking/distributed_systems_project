# Python resmi imajını kullanarak başlayın
FROM python:3.11

# Çalışma dizinini belirleyin
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
# Assuming you have a requirements.txt file with kafka-python and any other dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Make port 90 available to the world outside this container
EXPOSE 90

# Define environment variable
ENV NAME Chatserver

# Uygulama dosyalarını kopyalayın
COPY chatserver_server.py chatserver_server.py

# Sunucu başlatma komutunu belirtin
CMD ["python", "chatserver_server.py"]
