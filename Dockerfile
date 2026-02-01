FROM python:3.10

WORKDIR /code

# Copy requirements dan install dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy seluruh file ke dalam container
COPY . /code

# Pengaturan permission folder cache (Wajib untuk Hugging Face)
RUN mkdir -p /code/cache && chmod -R 777 /code/cache
ENV GRADIO_TEMP_DIR="/code/cache"

# Jalankan aplikasi
CMD ["python", "app.py"]