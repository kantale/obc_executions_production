#!/bin/bash
#
#
#
# This script will:
# 1. Install all client dependencies
#	- docker
#	- docker-compose
# 2. Generate unique Executor_Id and customize variables for OpenBioC server


# Check if docker exist in your environment

echo "Welcome to the OpenBio Executor, $USER!"
echo "Installation will take a few minutes. Please be patient..."

echo "State 1/3 (Install docker) "
docker -v
if [ $? -ne 0 ] ; then 
	echo "Docker is not installed."
	echo "Docker installation start...."
	curl -fsSL https://get.docker.com -o get-docker.sh
	sh get-docker.sh
	rm -r get-docker.sh
	# Post install docker https://docs.docker.com/install/linux/linux-postinstall/
	# Run docker without sudo
	sudo groupadd docker
	sudo usermod -aG docker $USER
	# Simplify somehow the next steps 
	# 1) Log out and log back in so that your group membership is re-evaluated
	# 2) If you initially ran Docker CLI commands using sudo before adding your 
	#    user to the docker group, you may see the following error, which 
	#    indicates that your ~/.docker/ directory was created with incorrect 
	#    permissions due to the sudo commands.

	#    To fix that error run:
        sudo chown "$USER":"$USER" /home/"$USER"/.docker -Run
	sudo chmod g+rwx "$HOME/.docker" -R


fi

echo "State 2/3 (Install docker-compose) "

docker-compose -v
if [ $? -ne 0 ] ; then
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

echo "State 3/3 (Setting up variables and installing the OpenBio Executor) "

export OBC_EXECUTOR_PATH="/home/"$USER"/obc_executor"

echo "Set installation path on your environment: " $OBC_EXECUTOR_PATH 
# Generate the installation file
mkdir $OBC_EXECUTOR_PATH
echo "Make dir exit code"
echo $?
export OBC_USER_ID=$(dbus-uuidgen)

if [ $? -eq 1 ] ; then
	echo "uuidgen is not installed"
	echo "uuidgen installation start...."
 	sudo apt-get install uuid-runtime
	export $OBC_USER_ID=$(dbus-uuidgen)
fi

# cd $OBC_EXECUTOR_PATH

echo -e "Client ID for OpenBioC Server : \033[38;2;0;255;0m$OBC_USER_ID\033[0m"
export PUBLIC_IP=$(curl http://ip4.me 2>/dev/null | sed -e 's#<[^>]*>##g' | grep '^[0-9]')

# File contains images
wget --directory-prefix=$OBC_EXECUTOR_PATH https://raw.githubusercontent.com/manoskout/OpenBioC_Execution/master/docker-compose.yml
# Config File
wget --directory-prefix=$OBC_EXECUTOR_PATH https://raw.githubusercontent.com/manoskout/docker-airflow/master/config/airflow.cfg



# Set obc_executor_run.sh (Optional)
# wget https://raw.githubusercontent.com/manoskout/docker-airflow/master/obc_executor_run.sh
#cd $OBC_EXECUTOR_PATH
echo "Running Directory : " $(pwd)

# Check if the pre-selected ports are in use 
export OBC_AIRFLOW_PORT=8080
export OBC_EXECUTOR_PORT=5000
#TEST AIRFLOW PORT (DEFAULT 8080)
# echo "Check if Airflow port : " $OBC_AIRFLOW_PORT "is in use..."
sudo netstat -tulpn | grep $OBC_AIRFLOW_PORT
while [$? -ne 0] ;
do
	echo "Port :" $(OBC_AIRFLOW_PORT) " already exist ...."
	# If the port Already exists check the previous_port + 1 (CHECK THAT)
	export OBC_AIRFLOW_PORT=$(expr $OBC_AIRFLOW_PORT + 1 )
	echo "New port check, in port : " $OBC_AIRFLOW_PORT
	sudo netstat -tulpn | grep $OBC_AIRFLOW_PORT
done
echo "Exit code of Airflow port Finder : " $?
echo "Port which Airflow running : " $OBC_AIRFLOW_PORT

#TEST EXECUTOR PORT (DEFAULT 5000)
sudo netstat -tulpn | grep $OBC_EXECUTOR_PORT
while [$? -ne 0] ;
do
	echo "Port :" $(OBC_EXECUTOR_PORT) " already exist ...."
	export OBC_EXECUTOR_PORT=$(expr $OBC_EXECUTOR_PORT + 1 )
	echo "New port check, in port : " $OBC_EXECUTOR_PORT
	sudo netstat -tulpn | grep $OBC_EXECUTOR_PORT
done
echo "Exit code of Executor port Finder : " $?
echo "Port which Executor running : " $OBC_EXECUTOR_PORT

echo -e OBC_USER_ID=$OBC_USER_ID"\n"PUBLIC_IP=$PUBLIC_IP"\n"OBC_EXECUTOR_PORT=$OBC_EXECUTOR_PORT"\n"OBC_AIRFLOW_PORT=$OBC_AIRFLOW_PORT >> .env 


docker-compose up -d
if [ $? -eq 0 ] ; then 

	export OBC_EXECUTOR_URL="http://$PUBLIC_IP:$OBC_EXECUTOR_PORT/$OBC_USER_ID"
	echo -e "\033[38;2;0;255;0m\n\n\n Successful installation \n\n\n\033[0m"
	echo -e "\033[38;2;0;255;0m Close tests \033[0m"
	docker-compose down
	echo -e "\n\n\n\n\n"
	echo $OBC_EXECUTOR_URL | xsel -ib
	echo -e "\033[38;2;0;255;0m**IMPORTANT**\033[0m"
	echo -e "\033[38;2;0;255;100m
	Copy this link below in OpenBioC Settings to confirm the connection: 
	(Link have automatically copied)
	\033[0m
	"
	echo -e "\033[48;2;0;255;0m
	\033[38;2;0;0;0m$OBC_EXECUTOR_URL\033[0m
	\033[0m"
else
#	echo "Subnet already in use..."
#        echo "Remove networks"
#	docker network prune
#        docker-compose up -d
#        echo "service run test  code -> " $?
	docker-compose down
fi

