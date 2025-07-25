# Dockerfile para servicio Node.js (vista de productos)
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3001
CMD [ "node", "index.js" ]

