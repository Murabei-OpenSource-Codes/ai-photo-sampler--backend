source version
git add --all
git commit -m "Building a new version for Auth App ${VERSION}"
git tag -a app_${VERSION} -m "Building a new version for Auth App ${VERSION}"
git push
git push origin app_${VERSION}

docker push southamerica-east1-docker.pkg.dev/serene-boulder-340918/private-images/ai-photo-sampler-app:${VERSION}
