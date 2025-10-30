FROM node:20-alpine

WORKDIR /app

ENTRYPOINT ["sh", "-c", "npm ci && npm run build"]
