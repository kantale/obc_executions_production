set -ex


#SET THE FOLLOWING VAR
USERNAME=manoskoutoulakis
IMAGE=obc_client

#ensure we are up to date
git pull

version=`cat VERSION`
echo "version: $version"

#run build
./build.sh

#TAG IT
git add -A
git commit -m "version $version"
git tag -a "$version" -m "version $version"
git push
git push --tags

docker tag $USERNAME/$IMAGE:latest $USERNAME/$IMAGE:$version

#push it 
docker push $USERNAME/$IMAGE:latest
docker push $USERNAME/$IMAGE:$version
