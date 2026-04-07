FROM node:18-alpine

WORKDIR /app

COPY app/juice-shop/ .

RUN npm install --omit=dev

EXPOSE 3000

CMD ["npm", "start"]