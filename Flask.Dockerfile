FROM python:3.8-buster

# Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED=TRUE

# Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE=TRUE

RUN mkdir /app

COPY mtg_collection/api /app/api
COPY requirements.txt /app/requirements.txt
COPY scripts/flask-entrypoint.sh /app/flask-entrypoint.sh

RUN pip install --upgrade pip && \
    pip install --no-cache-dir --requirement /app/requirements.txt

RUN chmod 774 /app/flask-entrypoint.sh

EXPOSE 5000

ENTRYPOINT [ "/app/flask-entrypoint.sh" ]
