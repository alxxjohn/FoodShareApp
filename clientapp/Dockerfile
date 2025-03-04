# Base image for common dependencies (Node.js and npm install)
FROM node:18-alpine AS base
WORKDIR /app

RUN corepack enable && npm install -g npm

COPY ./package.json /app/package.json
COPY ./package-lock.json /app/package-lock.json

RUN npm install @vue/cli-service --save-dev

RUN npm install

COPY . .

# Development image (run Vue dev server)
FROM base AS dev
EXPOSE 8080

# Build image (build the app for production)
FROM base AS build
RUN npm run build

# Use nginx to serve the built frontend
FROM nginx:alpine AS prod
# Copy the custom Nginx configuration


COPY ./nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
# Start Nginx to serve the application
CMD ["nginx", "-g", "daemon off;"]