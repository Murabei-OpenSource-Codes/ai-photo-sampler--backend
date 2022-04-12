source docker-versions.sh

docker push andrebaceti/test-db-ai-photo-sampler:$TEST_DB_PUMPWOOD_AUTH
docker push andrebaceti/ai-photo-sampler-app:$PUMPWOOD_AUTH_APP
docker push andrebaceti/ai-photo-sampler-static:$PUMPWOOD_AUTH_STATIC
