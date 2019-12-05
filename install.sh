#!/bin/bash
#
#
#
#
#
# This script will:
#
# 1. Install all client dependencies
#	- docker
#	- docker-compose

 

# Check if docker exist in your environment
docker -v
if [ $? -eq 1 ] ; then 
	echo "Docker is not installed."
	echo "Docker installation start...."
	curl -fsSL https://get.docker.com -o get-docker.sh
	sh get-docker.sh
fi

docker-compose -v
if [ $? -eq 1 ] ; then
	echo "Docker-Compose is not installed."
	echo "Docker-Compose installation start...."
	sudo wget \
        	--output-document=/usr/local/bin/docker-compose \
        	https://github.com/docker/compose/releases/download/1.24.0/run.sh \
    	&& sudo chmod +x /usr/local/bin/docker-compose \
    	&& sudo wget \
        	--output-document=/etc/bash_completion.d/docker-compose \
        	"https://raw.githubusercontent.com/docker/compose/$(docker-compose version --short)/contrib/completion/bash/docker-compose" \
    	&& printf '\nDocker Compose installed successfully\n\n'
fi


