# Python resmi imajını kullanarak başlayın
FROM python:3.9

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
ENV NAME Chatsever

# Uygulama dosyalarını kopyalayın
COPY chatsever_server2.py .

# Sunucu başlatma komutunu belirtin
CMD ["python", "chatsever_server2.py"]
