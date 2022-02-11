source version
git add --all
git commit -m "Building a new version for Test Database ${VERSION}"
git tag -a db_${VERSION} -m "Building a new version for Test Database ${VERSION}"
git push
git push origin db_${VERSION}

docker push andrebaceti/test-db-ai-photo-sampler:${VERSION}
