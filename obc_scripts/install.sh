#!/bin/bash
#
# This bashscript work only on debian based distros
#
# This script will:
# 1. Install all client dependencies
#	- docker
#	- docker-compose
# 2. Generate unique Executor_Id and customize variables for OpenBioC server


# Check if docker exist in your environment

#SETTING COLORS FOR OUTPUTS OF ECHO

RED='\033[0;31m'
NC='\033[0m' # No Color
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
LGREEN='\033[1;32m'


echo "Welcome to the OpenBio Executor, ${USER}!"
echo "Installation will take a few minutes. Please be patient..."

echo "State 1/3 (Install docker) "

# Save the distroID to optimize the installation of docker
export DISTRO_ID=$(lsb_release -i -s)
echo "Check if docker already exists..."
# 1> /dev/null 2>&1 not show the output
docker -v 1> /dev/null 2>&1
if [ $? -ne 0 ] ; then 
	echo "--> Docker is not installed, installation starts..."
	sleep 2
	# Save the distroID to optimize the installation of docker
	export DISTRO_ID=$(lsb_release -i -s)
	
	sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 7EA0A9C3F273FCD8
	sudo apt-get update
	curl -fsSL https://get.docker.com -o get-docker.sh
	sudo sh get-docker.sh
fi
#sudo groupadd docker
#sudo usermod -aG docker $USER
#sudo chown "$USER":"$USER" /home/"$USER"/.docker -R
#sudo chmod g+rwx "$HOME/.docker" -R
echo "State 2/3 (Install docker-compose) "

echo "Check if docker already exists..."
docker-compose -v
if [ $? -ne 0 ] ; then
	echo "--> Docker-Compose is not installed, installation starts..."

	# Copy pasting from: https://docs.docker.com/compose/install/ 
	sudo curl -L "https://github.com/docker/compose/releases/download/1.25.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
	sudo chmod +x /usr/local/bin/docker-compose
fi

echo "State 3/3 (Setting up variables and installing the OpenBio Executor) "


# Set user input for executor name
read -e -p "Enter your executor name: " EXECUTOR_INSTANCE
if [ -z $EXECUTOR_INSTANCE ]; then 
	export EXECUTOR_INSTANCE="main"
	echo "Executor name is unset, take default value: main"; 
else 
	echo "Executor name is set : '$EXECUTOR_INSTANCE'"; 
fi

# Set OBC_EXECUTOR PATH
export OBC_EXECUTOR_PATH="/home/${USER}/obc_executor_${EXECUTOR_INSTANCE}"

echo "Set installation path on your environment: ${OBC_EXECUTOR_PATH}" 
# Generate the installation file
mkdir -p ${OBC_EXECUTOR_PATH}
echo "Make dir exit code"
echo $?
export OBC_USER_ID=$(dbus-uuidgen)
export NETDATA_ID=$(dbus-uuidgen)

if [ $? -eq 1 ] ; then
	echo "uuidgen is not installed"
	echo "uuidgen installation start...."
 	sudo apt-get install uuid-runtime
	export OBC_USER_ID=$(dbus-uuidgen)
	export NETDATA_ID=$(dbus-uuidgen)
fi

# cd $OBC_EXECUTOR_PATH

echo -e "Client ID for OpenBioC Server : \033[38;2;0;255;0m${OBC_USER_ID}\033[0m"
export PUBLIC_IP=$(curl http://ip4.me 2>/dev/null | sed -e 's#<[^>]*>##g' | grep '^[0-9]')

# File contains images
wget -O ${OBC_EXECUTOR_PATH}/docker-compose.yml https://raw.githubusercontent.com/manoskout/obc_executions_production/master/docker-compose.yml
# Config File
wget -O ${OBC_EXECUTOR_PATH}/airflow.cfg https://raw.githubusercontent.com/manoskout/obc_executions_production/master/airflow.cfg



# Set obc_executor_run.sh (Optional)
# wget https://raw.githubusercontent.com/manoskout/docker-airflow/master/obc_executor_run.sh
#cd $OBC_EXECUTOR_PATH
echo "Running Directory : $(pwd)"

# Check if the pre-selected ports are in use 
export OBC_AIRFLOW_PORT=8080
export OBC_EXECUTOR_PORT=5000
export EXECUTOR_DB_PORT=5432
export NETDATA_MONITORING_PORT=19998

# Check port function
function portfinder (){
	# local result
	sudo netstat -tulpn | grep $1 > /dev/null 2>&1
	while [ $? -eq 0 ] ;
	do
		# echo "Port : $1 already exist ...."
		# If the port Already exists check the previous_port + 1 (CHECK THAT)
		set -- $(expr $1 + 1) $1
		# echo "New port check, in port : $1"
		sudo netstat -tulpn | grep $1 > /dev/null 2>&1
	done
	# echo "Exit code of Airflow port Finder : ${?}"
	# echo "Port which Airflow running : $1"
	# return $1
	echo $1
}

cat >> ${OBC_EXECUTOR_PATH}/.env << EOF
EXECUTOR_INSTANCE=${EXECUTOR_INSTANCE}
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
POSTGRES_DB=airflow
OBC_USER_ID=${OBC_USER_ID}
PUBLIC_IP=${PUBLIC_IP}
OBC_EXECUTOR_PORT=$(portfinder $OBC_EXECUTOR_PORT)
OBC_AIRFLOW_PORT=$(portfinder $OBC_AIRFLOW_PORT)
NETDATA_MONITORING_PORT=$(portfinder $NETDATA_MONITORING_PORT)
EXECUTOR_DB_PORT=$(portfinder $EXECUTOR_DB_PORT)
NETDATA_ID=${NETDATA_ID}
EOF

#TODO -> change using docker-compose up -f asfsedfsdf.yml(FAILED)
cd ${OBC_EXECUTOR_PATH}
sudo docker-compose up -d
# eval $(cat $OBC_EXECUTOR_PATH/.env | xargs) sudo docker-compose -f $OBC_EXECUTOR_PATH/docker-compose.yml up -d

if [ $? -eq 0 ] ; then 

	export OBC_EXECUTOR_URL="http://${PUBLIC_IP}:${OBC_EXECUTOR_PORT}/${OBC_USER_ID}"
	export NETDATA_URL="http://${PUBLIC_IP}:${NETDATA_MONITORING_PORT}/${NETDATA_ID}"
	echo -e "${GREEN}\n\n\n Successful installation \n\n\n\Close tests \n\n ${OBC_EXECUTOR_URL}${NC}"
	
	echo -e "${GREEN}\n\n\n Netdata url : ${NETDATA_URL}${NC}"
	echo -e "${YELLOW}**IMPORTANT**${NC}"
	echo -e "${GREEN}\n\tCopy this link below in OpenBioC Settings to confirm the connection: \n${NC}"
	echo -e "${LGREEN}${OBC_EXECUTOR_URL}${NC}"

	echo -e "${YELLOW}
	The executor already running on your system. If you like to kill the service simply run:
		$ docker-compose -f ${OBC_EXECUTOR_PATH} down
		or, if you like to make some changes on docker-compose.yml or on airflow.cfg file:
		$ cd ${OBC_EXECUTOR_PATH}  

	${NC}
	"
        sudo docker-compose down
else
	echo "Something goes wrong.. Close the service!"
	sudo docker-compose down
fi

