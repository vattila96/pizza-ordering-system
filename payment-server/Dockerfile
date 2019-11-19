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

RUN ls -la

RUN yarn install
RUN yarn build

RUN ls -la
RUN ls -la ./dist

CMD ["node", "./dist/server.js"]
