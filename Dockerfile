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

COPY . /app/

RUN chmod 755 /app/entrypoint.sh

#RUN addgroup --system appuser && adduser --system --ingroup appuser appuser
#RUN chown -R appuser:appuser /app
#
#USER appuser

EXPOSE 8000

ENTRYPOINT ["bash","/app/entrypoint.sh"]
