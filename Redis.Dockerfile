FROM redis:latest

RUN mkdir -p /app

COPY mtg_collection/config /app/config

EXPOSE 6379

CMD [ "redis-server", "/app/config/redis_main.conf" ]
