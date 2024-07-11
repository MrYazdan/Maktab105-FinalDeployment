FROM nginx:stable-alpine

USER root

RUN apk add --update openssl bash

COPY ./default-ssl.conf.template ./default.conf.template /etc/nginx/
COPY ./entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]