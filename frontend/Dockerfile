# ./frontend/Dockerfile
FROM node:20 AS build
WORKDIR /app
COPY . .
RUN npm install
RUN npm run build

FROM alpine AS dummy
WORKDIR /dist
COPY --from=build /app/dist .
