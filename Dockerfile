FROM python:3.13.3-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    musl-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ساخت یوزر امن
RUN addgroup --system appuser && adduser --system --ingroup appuser appuser

# ساخت فولدرهای ضروری و دسترسی
RUN mkdir -p /app/staticfiles && \
    mkdir -p /app/media && \
    chown -R appuser:appuser /app

RUN chmod +x entrypoint.sh

USER appuser

EXPOSE 8000

ENTRYPOINT [ "./entrypoint.sh" ]
