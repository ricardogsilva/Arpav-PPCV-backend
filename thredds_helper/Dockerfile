FROM node:16
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm install
COPY index.js .
EXPOSE 8089
CMD [ "node", "index.js" ]
