FROM node:18.19-alpine3.18

WORKDIR /app

COPY package.json ./

COPY package-lock.json ./

RUN npm update && npm install -g @angular/cli && npm ci

COPY . .

CMD ["npm", "run", "start:prod"]
