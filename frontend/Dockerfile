FROM node:16-alpine AS build

RUN apk add --no-cache python3 make g++

WORKDIR /app

RUN npm install -g npm@8.19.4 && \
    npm config set fetch-timeout 600000 && \
    npm config set fund false && \
    npm config set update-notifier false

COPY package*.json ./

RUN npm ci --only=production --prefer-offline --no-audit --network-timeout=600000

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]