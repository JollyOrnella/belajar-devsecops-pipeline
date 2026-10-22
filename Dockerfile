
FROM python:3.10-slim

WORKDIR /app

# Membuat user non-root untuk keamanan
RUN useradd -m appuser

# Menginstal dependensi aplikasi
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin file aplikasi
COPY . .

# Memberikan kepemilikan file kepada appuser
RUN chown -R appuser:appuser /app

# Menjalankan container sebagai non-root
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
