FROM node:latest

RUN mkdir app

COPY frontend/src /app/src
COPY frontend/package.json /app/package.json
COPY frontend/package-lock.json /app/package-lock.json
COPY frontend/vue.config.js /app/vue.config.js
COPY scripts/frontend-entrypoint.sh /app/frontend-entrypoint.sh

RUN chmod 774 /app/frontend-entrypoint.sh

WORKDIR /app/
RUN npm i

EXPOSE 8080

ENTRYPOINT [ "/app/frontend-entrypoint.sh" ]
