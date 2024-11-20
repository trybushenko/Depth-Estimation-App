# src/frontend/Dockerfile

# 1. Build Stage
FROM node:18-alpine AS build

# 2. Set Working Directory
WORKDIR /app

# 3. Install Dependencies
COPY package.json package-lock.json ./
RUN npm install

# 4. Copy Application Code
COPY . .

# 5. Build the React App
RUN npm run build

# 6. Production Stage
FROM nginx:stable-alpine

# 7. Remove Default Nginx Website
RUN rm -rf /usr/share/nginx/html/*

# 8. Copy Built Files from Build Stage
COPY --from=build /app/build /usr/share/nginx/html

# 9. Copy Custom Nginx Configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 10. Expose Port
EXPOSE 80

# 11. Start Nginx
CMD ["nginx", "-g", "daemon off;"]
