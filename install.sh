#!/bin/bash
#
#
#
# This script will:
# 1. Generate unique Id for OpenBioC server
# 2. Install all client dependencies
#	- docker
#	- docker-compose


export OBC_CLIENT_PATH="/home/"$USER"/obc_client"

echo "Set installation path on your environment: " $OBC_CLIENT_PATH 
# Generate the installation file
mkdir $OBC_CLIENT_PATH
echo $?
echo "Make dir exit code"
export OBC_USER_ID=$(dbus-uuidgen)

if [ $? -eq 1 ] ; then
	echo "uuidgen is not installed"
	echo "uuidgen installation start...."
 	sudo apt-get install uuid-runtime
	export $OBC_USER_ID=$(dbus-uuidgen)
fi
echo -e "Client ID : \033[38;2;0;255;0m$OBC_USER_ID\033[0m"

cd $OBC_CLIENT_PATH

echo -e "Client ID for OpenBioC Server : \033[38;2;0;255;0m$OBC_USER_ID\033[0m"
echo OBC_USER_ID=$OBC_USER_ID | tee .env


# Set files
#mkdir dags
#mkdir logs
mkdir config
# File contains images
wget https://raw.githubusercontent.com/manoskout/OpenBioC_Execution/master/docker-compose.yml
# Config File
cd config ; wget https://raw.githubusercontent.com/manoskout/docker-airflow/master/config/airflow.cfg
cd ..

# Client Configuration Should not be existed TODO upload to DockerHub
#mkdir OBC_Client; cd OBC_Client
#mkdir generated_dags
# Dockerfile - Client Service
#wget https://raw.githubusercontent.com/manoskout/docker-airflow/master/client/client.py
#wget https://raw.githubusercontent.com/manoskout/docker-airflow/master/client/requirements.txt
#wget https://raw.githubusercontent.com/manoskout/docker-airflow/master/client/Dockerfile


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

# Set OBC_Client_run.sh (Optional)
# wget https://raw.githubusercontent.com/manoskout/docker-airflow/master/OBC_client_run.sh
#cd $OBC_CLIENT_PATH
echo "Running Directory : " $(pwd)
docker-compose up -d
if [ $? -eq 0 ] ; then 
	export PUBLIC_IP=$(curl http://ip4.me 2>/dev/null | sed -e 's#<[^>]*>##g' | grep '^[0-9]')

	export OBC_CLIENT_URL="http://$PUBLIC_IP:5000/$OBC_USER_ID"
	echo -e "\033[38;2;0;255;0m\n\n\n Successful installation \n\n\n\033[0m"
	echo -e "\033[38;2;0;255;0m Close tests \033[0m"
	docker-compose down
	echo -e "\n\n\n\n\n"
	echo $OBC_CLIENT_URL | xsel -ib
	echo -e "\033[38;2;0;255;0m**IMPORTANT**\033[0m"
	echo -e "\033[38;2;0;255;100m
	Copy this link below in OpenBioC Settings to confirm the connection: 
	(Link have automatically copied)
	\033[0m
	"
	echo -e "\033[48;2;0;255;0m
	\033[38;2;0;0;0m$OBC_CLIENT_URL\033[0m
	\033[0m"
else
#	echo "Subnet already in use..."
#        echo "Remove networks"
#	docker network prune
#        docker-compose up -d
#        echo "service run test  code -> " $?
	docker-compose down
fi

