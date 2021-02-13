FROM python:3.8-buster

# Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED=TRUE

# Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE=TRUE

RUN mkdir /app

COPY mtg_collection/api /app/api
COPY mtg_collection/database /app/database
COPY mtg_collection/constants.py /app/constants.py
COPY mtg_collection/__init__.py /app/__init__.py
COPY requirements.txt /requirements.txt
COPY scripts/flask-entrypoint.sh /app/flask-entrypoint.sh

ENV PYTHONPATH=/app:$PYTHONPATH

RUN pip install --upgrade pip && \
    pip install --no-cache-dir --requirement /requirements.txt

RUN chmod 774 /app/flask-entrypoint.sh
RUN chmod 774 /app -R

EXPOSE 5000

ENTRYPOINT [ "/app/flask-entrypoint.sh" ]
