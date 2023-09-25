FROM node:14.9.0-buster-slim as build

WORKDIR /app

COPY "package*.json" ./
RUN npm install
COPY . ./
RUN npm run build

# Nginx wrapper to serve static files
FROM nginx:stable
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]