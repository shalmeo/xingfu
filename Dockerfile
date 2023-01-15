FROM python:3.10-slim

WORKDIR /usr

COPY requirements.txt /usr
RUN apt-get update \
 && apt-get install -y gcc \
 && pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir setuptools wheel \
 && pip install --no-cache-dir -r requirements.txt \
 && rm -rf /var/lib/apt/lists/*
COPY . /usr

CMD ["uvicorn", "src.entrypoints.bot:app", "--host", "0.0.0.0", "--port", "80"]