FROM nginx:alpine
LABEL security-test="unsigned-image"
RUN apk update && apk upgrade --no-cache && rm -rf /var/cache/apk/*
