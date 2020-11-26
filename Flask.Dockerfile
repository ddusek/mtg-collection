FROM python:3.8.6-buster

ENV PYTHONUNBUFFERED 1

RUN mkdir app/

WORKDIR /app/

COPY mtg_collection/api /api
COPY requirements.txt requirements.txt
COPY scripts/ scripts/

RUN pip install --upgrade pip && \
    pip install --no-cache-dir --requirement requirements.txt

EXPOSE 5000

ENTRYPOINT [ ./scripts/flask-entrypoint.sh ]
