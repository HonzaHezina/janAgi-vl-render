FROM python:3.11-slim

# Fonty pro hezčí výstup (DejaVu pokryje většinu glyphů)
RUN apt-get update && apt-get install -y --no-install-recommends \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8000

# Uvicorn běží na 0.0.0.0, aby byl dostupný z container sítě i přes proxy.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
