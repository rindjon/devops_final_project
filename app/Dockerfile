FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    libx11-6 libglib2.0-0 libsm6 libxext6 libxrender1 \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1

RUN pip install flask boto3 pymysql

WORKDIR /app

COPY . /app

EXPOSE 5000

CMD ["python", "app.py"]
