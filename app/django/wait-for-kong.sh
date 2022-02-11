#!/bin/bash
set -e

echo "############################"
echo "Waiting fot kong to kick in!"
echo "############################"

until curl -sSf http://load-balancer:8001/ > /dev/null; do
  >&2 echo "Kong is not ready"
  sleep 1
done
echo "Kong is ok!"
