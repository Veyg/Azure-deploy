FROM node:16-alpine AS build

WORKDIR /app

# Copy package files first
COPY package*.json ./

# Add npm optimization flags and increase network timeout
RUN npm install --production --no-audit --network-timeout=100000

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]