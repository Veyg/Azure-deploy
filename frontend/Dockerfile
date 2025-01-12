FROM node:16-alpine AS build

WORKDIR /app

# Set npm to run in production and CI mode
ENV NODE_ENV=production
ENV CI=true

# Copy package files
COPY package*.json ./

# Install dependencies with optimizations
RUN npm config set fund false && \
    npm config set update-notifier false && \
    npm install --omit=dev --no-audit --no-optional --network-timeout=100000 --silent

# Copy source and build
COPY . .
RUN npm run build --silent

# Production stage
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]