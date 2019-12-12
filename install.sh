#!/bin/bash
#
#
#
# This script will:
# 1. Generate unique Id for OpenBioC server
# 2. Install all client dependencies
#	- docker
#	- docker-compose


export OBC_CLIENT_PATH= "/home/"$USER"/obc_client"

echo "Set installation path on your environment: "$OBC_CLIENT_PATH 
# Generate the installation file
mkdir $OBC_CLIENT_PATH

export OBC_USER_ID=$(dbus-uuidgen)

if [ $? -eq 1 ] ; then
	echo "uuidgen is not installed"
	echo "uuidgen installation start...."
	sudo apt-get install uuid-runtime
	export $OBC_USER_ID=$(dbus-uuidgen)
fi
cd $OBC_CLIENT_PATH

echo "Unique id for OpenBioC server generated :"
echo $OBC_USER_ID | tee obc_id.txt

# Set the id file read-only
chmod 0444 obc_id.txt

# Set files
mkdir dags
mkdir logs
mkdir config
# File contains images
wget https://raw.githubusercontent.com/manoskout/docker-airflow/master/docker-compose.yml
# Config File
cd config ; wget https://raw.githubusercontent.com/manoskout/docker-airflow/master/config/airflow.cfg ; cd ..

# Client Configuration Should not be existed TODO upload to DockerHub
mkdir OBC_Client; cd OBC_Client
mkdir generated_dags
# Dockerfile - Client Service
wget https://raw.githubusercontent.com/manoskout/docker-airflow/master/client/client.py
wget https://raw.githubusercontent.com/manoskout/docker-airflow/master/client/requirements.txt
wget https://raw.githubusercontent.com/manoskout/docker-airflow/master/client/Dockerfile


# Check if docker exist in your environment
docker -v
if [ $? -eq 1 ] ; then 
	echo "Docker is not installed."
	echo "Docker installation start...."
	curl -fsSL https://get.docker.com -o get-docker.sh
	sh get-docker.sh
	rm -r get-docker.sh
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
    	&& printf '\nDocker Compose installed successfully\n\n' \
	rm -r run.sh

fi

# Set OBC_Client_run.sh

wget https://raw.githubusercontent.com/manoskout/docker-airflow/master/OBC_client_run.sh
