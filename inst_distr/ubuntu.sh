#!/bin/bash
#
#
#
# This script will:
# 1. Install docker on linux distro

# Update the apt package index.
sudo apt-get update

#Install the latest version of Docker Engine - Community and containerd:
sudo apt-get install docker-ce docker-ce-cli containerd.io

# Check if docker installed correctly
sudo docker run hello-world

if [ $? -eq 1 ] ; then
	echo "DOCKER installed correctly!"
fi