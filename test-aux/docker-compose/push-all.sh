source docker-versions.sh

docker push southamerica-east1-docker.pkg.dev/serene-boulder-340918/private-images/test-db-ai-photo-sampler:$TEST_DB_PUMPWOOD_AUTH
docker push southamerica-east1-docker.pkg.dev/serene-boulder-340918/private-images/ai-photo-sampler-app:$PUMPWOOD_AUTH_APP
docker push southamerica-east1-docker.pkg.dev/serene-boulder-340918/private-images/ai-photo-sampler-static:$PUMPWOOD_AUTH_APP
