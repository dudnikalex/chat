FROM node:15.12.0-alpine3.10 as builder

WORKDIR /app

RUN apk add g++ make python

COPY frontend/package.json /app/package.json
RUN yarn install --only=prod

COPY frontend /app

RUN yarn run build

FROM nginx:1.16.0-alpine
COPY --from=builder /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]