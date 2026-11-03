FROM python:3.12-slim AS build
WORKDIR /src
COPY maquette/ ./maquette/
COPY design/lick/logo.png ./design/lick/logo.png
RUN python maquette/build.py --output /out/index.html

FROM node:22-bookworm-slim
ENV NODE_ENV=production \
    DATAHUB_HTML_PATH=/app/index.html \
    DATAHUB_BIND_HOST=0.0.0.0
WORKDIR /app
COPY --from=build --chown=node:node /out/index.html ./index.html
COPY --chown=node:node preview/server.cjs ./server.cjs
USER node
EXPOSE 8080
CMD ["node", "server.cjs"]
