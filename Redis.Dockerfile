FROM redis:latest

RUN mkdir -p /app

COPY mtg_collection/config /app/config
COPY mtg_collection/database /app/database

EXPOSE 6379

CMD [ "redis-server", "/app/config/redis.conf" ]
