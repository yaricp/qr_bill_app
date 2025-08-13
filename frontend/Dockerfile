# building stage
FROM node:18.18.0 as build-stage
WORKDIR /app
COPY package*.json ./
COPY . .
RUN yarn install

ARG VUE_APP_ENV=${VUE_APP_ENV}
ARG VUE_APP_PREFIX=${VUE_APP_PREFIX}
ARG VUE_APP_API_PROD=${VUE_APP_API_PROD}
ARG VUE_APP_API_STAG=${VUE_APP_API_STAG}
ARG VUE_APP_API_DEV=${VUE_APP_API_DEV}
ARG VUE_APP_THIS_HOST_API=${VUE_APP_THIS_HOST_API}

RUN echo "$VUE_APP_THIS_HOST_API"

RUN yarn build

# production stage
FROM nginx:stable-alpine as production-stage
RUN apk add certbot
COPY --from=build-stage /app/dist /usr/share/nginx/html
# COPY nginx/conf.d/* /etc/nginx/conf.d/
COPY nginx/conf.d/qracun.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
