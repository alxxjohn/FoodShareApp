# Use node for build stage
FROM node:18 AS build
WORKDIR /app

# Copy package files and install dependencies
COPY ./package.json /app/package.json
COPY ./package-lock.json /app/package-lock.json
RUN npm install

# Copy project files and build Vue app
COPY . .
RUN npm run build

# Use nginx to serve the built frontend
FROM nginx:alpine

# Copy the custom Nginx configuration
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]