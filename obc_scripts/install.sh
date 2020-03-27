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

#SETTING COLORS FOR OUTPUTS
WHITE='\e[97m'
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
echo "[${YELLOW}-${NC}] Check if docker already exists..."
# 1> /dev/null 2>&1 not show the output
docker -v 1> /dev/null 2>&1
if [ $? -ne 0 ] ; then 
	echo "[${YELLOW}-${NC}] Docker is not installed, installation starts..."
	sleep 2
	# Save the distroID to optimize the installation of docker
	export DISTRO_ID=$(lsb_release -i -s)
	
	sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 7EA0A9C3F273FCD8
	sudo apt-get update
	curl -fsSL https://get.docker.com -o get-docker.sh
	sudo sh get-docker.sh
fi

echo "[${YELLOW}-${NC}] State 2/3 (Install docker-compose) "

echo "[${YELLOW}-${NC}] Check if docker already exists..."
docker-compose -v
if [ $? -ne 0 ] ; then
	echo "[${YELLOW}-${NC}] Docker-Compose is not installed, installation starts..."

	# Copy paste from: https://docs.docker.com/compose/install/ 
	sudo curl -L "https://github.com/docker/compose/releases/download/1.25.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
	sudo chmod +x /usr/local/bin/docker-compose
fi

echo "[${YELLOW}-${NC}] State 3/3 (Setting up variables and installing the OpenBio Executor) "


# Set user input for executor name, if the input is empty take default value ("main")
read -e -p "[${LGREEN}-->${NC}] Enter your executor name: " EXECUTOR_INSTANCE
if [ -z $EXECUTOR_INSTANCE ]; then 
	export EXECUTOR_INSTANCE="main"
	echo "[${YELLOW}-${NC}] Executor name is unset, take default value: main"; 
else 
	echo "[${YELLOW}-${NC}] Executor name is set : '$EXECUTOR_INSTANCE'"; 
fi

# Set OBC_EXECUTOR PATH
export OBC_EXECUTOR_PATH="/home/${USER}/obc_executor_${EXECUTOR_INSTANCE}"

echo "[${YELLOW}-${NC}] Set installation path on your environment: ${OBC_EXECUTOR_PATH}" 
mkdir -p ${OBC_EXECUTOR_PATH}
export OBC_USER_ID=$(dbus-uuidgen)
export NETDATA_ID=$(dbus-uuidgen)

#Install uuidgen if is not exist
if [ $? -eq 1 ] ; then
	echo "[${RED}-${NC}] uuidgen is not installed"
	echo "[${LGREEN}-${NC}] uuidgen installation start...."
 	sudo apt-get install uuid-runtime
	export OBC_USER_ID=$(dbus-uuidgen)
	export NETDATA_ID=$(dbus-uuidgen)
fi

echo -e "[${YELLOW}-${NC}] Client ID for OpenBioC Server : \033[38;2;0;255;0m${OBC_USER_ID}\033[0m"
export PUBLIC_IP=$(curl http://ip4.me 2>/dev/null | sed -e 's#<[^>]*>##g' | grep '^[0-9]')

# File contains images
wget -O ${OBC_EXECUTOR_PATH}/docker-compose.yml https://raw.githubusercontent.com/manoskout/obc_executions_production/master/docker-compose.yml
# Config File
wget -O ${OBC_EXECUTOR_PATH}/airflow.cfg https://raw.githubusercontent.com/manoskout/obc_executions_production/master/airflow.cfg



# Set obc_executor_run.sh (Optional)
# wget https://raw.githubusercontent.com/manoskout/docker-airflow/master/obc_executor_run.sh
echo "[${YELLOW}-${NC}] Running Directory : $(pwd)"

# Check if the pre-selected ports are in use 
export OBC_AIRFLOW_PORT=8080
export OBC_EXECUTOR_PORT=5000
export EXECUTOR_DB_PORT=5432
export NETDATA_MONITORING_PORT=19998

# Check port that service could starts running
function portfinder (){
	sudo netstat -tulpn | grep $1 > /dev/null 2>&1
	while [ $? -eq 0 ] ;
	do
		set -- $(expr $1 + 1) $1
		sudo netstat -tulpn | grep $1 > /dev/null 2>&1
	done
	echo $1
}
# Environment variables that used from Executor
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

if [ $? -eq 0 ] ; then 

	export OBC_EXECUTOR_URL="http://${PUBLIC_IP}:${OBC_EXECUTOR_PORT}/${OBC_USER_ID}"
	export NETDATA_URL="http://${PUBLIC_IP}:${NETDATA_MONITORING_PORT}/${NETDATA_ID}"
	echo -e "${GREEN}\n\n\n Successful installation \n\n\nClose tests ....\n\n${NC}"
    sudo docker-compose down
	echo -e "${YELLOW}**IMPORTANT**${NC}"
	echo -e "${GREEN}\n\tCopy this link below in OpenBioC Executor Settings to confirm the connection: \n${NC}"
	echo -e "${LGREEN}${OBC_EXECUTOR_URL}${NC}"
	echo -e "${GREEN}\n\tNetdata url : \n${NETDATA_URL}${NC}"

	echo -e "${WHITE}***Infos***${NC}\n${YELLOW}
	1)You can run OBC Executor using the following commands:${NC}
		$ cd ${OBC_EXECUTOR_PATH}
		$ docker-compose up
	2)Or, you can kill the Executor by typing the command below:
		$ cd ${OBC_EXECUTOR_PATH}
		$ docker-compose down
	${NC}
	"
else
	echo "Something goes wrong.. Close the service!"
	sudo docker-compose down
fi

