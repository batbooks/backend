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

RUN addgroup --system appuser && adduser --system --ingroup appuser --shell /bin/bash appuser

RUN mkdir -p /app/staticfiles && \
    mkdir -p /app/media && \
    chown -R appuser:appuser /app
RUN touch /app/django_errors.log && chmod 666 /app/django_errors.log

RUN chmod +x entrypoint.sh


EXPOSE 8000
USER root

ENTRYPOINT [ "./entrypoint.sh" ]
