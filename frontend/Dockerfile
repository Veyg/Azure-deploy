FROM node:16 AS build
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
RUN npm run build
RUN chmod -R 755 /app/build
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
# Add custom nginx configuration if necessary
# COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]