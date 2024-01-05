FROM node:17.5.0-stretch-slim as builder
WORKDIR /app
COPY ./package.json ./
COPY ./yarn.lock ./
RUN yarn install
COPY ./ ./
RUN yarn build

FROM nginx:1.23.4-alpine-slim
COPY ./conf.d/app.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist/ /