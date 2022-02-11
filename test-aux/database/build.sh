source version
PGPASSWORD=pumpwood pg_dump -h localhost -p 7000 -U pumpwood pumpwood > db_dump/database.sql
docker build -t southamerica-east1-docker.pkg.dev/serene-boulder-340918/private-images/test-db-ai-photo-sampler:${VERSION} .
rm db_dump/database.sql
