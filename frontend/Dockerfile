FROM node:16-alpine AS build

# Add python and build dependencies for node-gyp
RUN apk add --no-cache python3 make g++

WORKDIR /app

# Set specific npm version and configuration
RUN npm install -g npm@8.19.4 && \
    npm config set fetch-timeout 600000 && \
    npm config set fund false && \
    npm config set update-notifier false

# First copy only package files and install dependencies
COPY package*.json ./

# Install dependencies with specific flags
RUN npm ci --only=production --prefer-offline --no-audit --network-timeout=600000

# Then copy the rest and build
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]