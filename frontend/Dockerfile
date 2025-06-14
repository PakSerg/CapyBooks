FROM node:20 AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Просто выход, т.к. этот контейнер только для сборки
CMD ["echo", "Frontend build completed"]
