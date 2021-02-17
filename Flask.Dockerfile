FROM python:3.9-buster

# Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED=TRUE

# Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE=TRUE

RUN mkdir /mtg_collection

COPY mtg_collection/api /mtg_collection/api
COPY mtg_collection/database /mtg_collection/database
COPY mtg_collection/constants.py /mtg_collection/constants.py
COPY mtg_collection/__init__.py /mtg_collection/__init__.py
COPY requirements.txt /requirements.txt
COPY scripts/flask-entrypoint.sh /mtg_collection/flask-entrypoint.sh

ENV PYTHONPATH=./:$PYTHONPATH

RUN pip install --upgrade pip && \
    pip install --no-cache-dir --requirement /requirements.txt

RUN chmod 774 /mtg_collection/flask-entrypoint.sh
RUN chmod 774 /mtg_collection -R

EXPOSE 5000

ENTRYPOINT [ "/mtg_collection/flask-entrypoint.sh" ]
