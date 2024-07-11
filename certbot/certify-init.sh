#!/bin/sh

set -e

until nc -z nginx 80; do
  echo "Waiting for nginx proxy ..."
  sleep 5s & wait ${!}
done

echo "Getting certificate ..."

certbot certonly --webroot -w "/vol/www/" -d "rangvorang.ir" \
  --email "ismryazdan@gmail.com" --force-renewal \
  --rsa-key-size 4096 --agree-tos --noninteractive