set -ex

#SET THE FOLLOWING VARIABLES
# DOCKERHUB username
USERNAME=manoskoutoulakis

#IMAGE name
IMAGE=obc_client

docker build -t $USERNAME/$IMAGE:latest .
