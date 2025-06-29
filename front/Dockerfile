FROM node:alpine

WORKDIR /usr/local/app

COPY package.json package-lock.json ./

RUN npm install -g @angular/cli

RUN npm install

COPY . .

CMD ["ng", "serve", "--host", "0.0.0.0"]

