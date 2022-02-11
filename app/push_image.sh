source version
git add --all
git commit -m "Building a new version for Auth App ${VERSION}"
git tag -a app_${VERSION} -m "Building a new version for Auth App ${VERSION}"
git push
git push origin app_${VERSION}

docker push andrebaceti/ai-photo-sampler-app:${VERSION}
