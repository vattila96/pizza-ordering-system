FROM node:13.1.0-alpine3.10

EXPOSE $HTTP_PORT

ENV ENVIRONMENT ${ENVIRONMENT:-production}
ENV HTTP_PORT $HTTP_PORT
ENV APP_DIR /usr/src/app

RUN mkdir -p $APP_DIR
WORKDIR $APP_DIR

COPY .env webpack.config.js tsconfig.json environment.* postcss.config.js ./
COPY src src/
COPY package.json yarn.lock ./

RUN yarn install
RUN yarn build

CMD ["node", "./dist/server.js"]
