FROM node:13.1.0-alpine3.10

EXPOSE $HTTP_PORT

ENV ENVIRONMENT ${ENVIRONMENT:-production}
ENV HTTP_PORT $HTTP_PORT
ENV APP_DIR /usr/src/app

RUN mkdir -p $APP_DIR
WORKDIR $APP_DIR

COPY .env webpack.config.js tsconfig.json environment.* postcss.config.js ./
COPY package.json yarn.lock ./

# installing dependencies for the container inside (linux deps)
RUN yarn install

RUN mkdir src

# this will run your local code via the system inside the container.
# You can make changes locally and they will be reflected after restart (only in src, otherwise rebuild is required).
CMD yarn cold-start
