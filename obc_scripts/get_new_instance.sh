#!/bin/bash
#
# NEED UPDATE
#
# This script will:
# 1. Check which port are used
# 2. Generate unique Executor_Id and customize variables for OpenBioC server
# 3. Create new instance for obc_executor


echo "Welcome to the OpenBio Executor, ${USER}!"
echo "Installation of new will take a few minutes. Please be patient..."

echo "State 1/3 (generate files and check used ports)"

#TODO --> get the number of instance according the instance that already created
export PUBLIC_IP=$(curl http://ip4.me 2>/dev/null | sed -e 's#<[^>]*>##g' | grep '^[0-9]')
export EXECUTOR_INSTANCE=4
export OBC_EXECUTOR_PATH="/home/${USER}/obc_executor_instance_${EXECUTOR_INSTANCE}"

mkdir -p ${OBC_EXECUTOR_PATH}

# Generate unique id to communicate with OBC server
export OBC_USER_ID=$(dbus-uuidgen)

if [ $? -eq 1 ] ; then
  echo "uuidgen is not installed"
  echo "uuidgen installation start...."
  sudo apt-get install uuid-runtime
  export ${OBC_USER_ID}=$(dbus-uuidgen)
fi

echo -e "Client ID for OpenBioC Server : \033[38;2;0;255;0m${OBC_USER_ID}\033[0m"

export OBC_AIRFLOW_PORT=8080
export OBC_EXECUTOR_PORT=5000
export EXECUTOR_DB_PORT=5432
#TEST AIRFLOW PORT (DEFAULT 8080)
# echo "Check if Airflow port : " $OBC_AIRFLOW_PORT "is in use..."
sudo netstat -tulpn | grep ${OBC_AIRFLOW_PORT}
while [ $? -eq 0 ] ;
do
  echo "Port : ${OBC_AIRFLOW_PORT} already exist ...."
  # If the port Already exists check the previous_port + 1 (CHECK THAT)
  export OBC_AIRFLOW_PORT=$(expr ${OBC_AIRFLOW_PORT} + 1 )
  echo "New port check, in port : ${OBC_AIRFLOW_PORT}"
  sudo netstat -tulpn | grep ${OBC_AIRFLOW_PORT}
done
echo "Exit code of Airflow port Finder : ${?}"
echo "Port which Airflow running : ${OBC_AIRFLOW_PORT}"

#TEST EXECUTOR PORT (DEFAULT 5000)
sudo netstat -tulpn | grep ${OBC_EXECUTOR_PORT}
while [ $? -eq 0 ] ;
do
  echo "Port : ${OBC_EXECUTOR_PORT} already exist ...."
  export OBC_EXECUTOR_PORT=$(expr ${OBC_EXECUTOR_PORT} + 1 )
  echo "New port check, in port : ${OBC_EXECUTOR_PORT}"
  sudo netstat -tulpn | grep ${OBC_EXECUTOR_PORT}
done
echo "Exit code of Executor port Finder : ${?}"
echo "Port which Executor running : ${OBC_EXECUTOR_PORT}"

#TEST EXECUTOR DB (DEFAULt 5432)
while [ $? -eq 0 ] ;
do
  echo "Port : ${EXECUTOR_DB_PORT} already exist ...."
  export EXECUTOR_DB_PORT=$(expr ${EXECUTOR_DB_PORT} + 1 )
  echo "New port check, in port : ${EXECUTOR_DB_PORT}"
  sudo netstat -tulpn | grep ${EXECUTOR_DB_PORT}
done
echo "Exit code of Executor port Finder : ${?}"
echo "Port which Executor running : ${EXECUTOR_DB_PORT}"

sudo cat >> ${OBC_EXECUTOR_PATH}/.env << EOF
EXECUTOR_INSTANCE=${EXECUTOR_INSTANCE}
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
POSTGRES_DB=airflow
OBC_USER_ID=${OBC_USER_ID}
PUBLIC_IP=${PUBLIC_IP}
OBC_EXECUTOR_PORT=${OBC_EXECUTOR_PORT}
OBC_AIRFLOW_PORT=${OBC_AIRFLOW_PORT}
EXECUTOR_DB_PORT=${EXECUTOR_DB_PORT}

EOF


# To do specify tha on the main docker-compose.yml

wget -O ${OBC_EXECUTOR_PATH}/docker-compose.yml https://raw.githubusercontent.com/manoskout/obc_executions_production/master/docker-compose.yml
wget -O ${OBC_EXECUTOR_PATH}/airflow.cfg https://raw.githubusercontent.com/manoskout/obc_executions_production/master/airflow.cfg



echo "Files generated ..."
cd ${OBC_EXECUTOR_PATH}
sudo docker-compose up -d
if [ $? -eq 0 ] ; then 
  sudo apt-get install -y xsel 1> /dev/null 2>&1
  export OBC_EXECUTOR_URL="http://${PUBLIC_IP}:${OBC_EXECUTOR_PORT}/${OBC_USER_ID}"
  echo -e "\033[38;2;0;255;0m\n\n\n Successful installation \n\n\n\033[0m"
  echo -e "\033[38;2;0;255;0m Close tests \033[0m"
  #sudo docker-compose down
  echo -e "\n\n\n\n\n"
  echo ${OBC_EXECUTOR_URL} | xsel -ib
  echo -e "\033[38;2;0;255;0m**IMPORTANT**\033[0m"
  echo -e "\033[38;2;0;255;100m
  Copy this link below in OpenBioC Settings to confirm the connection: 
  (Link have automatically copied)
  \033[0m
  "
  echo -e "\033[48;2;0;255;0m
  \033[38;2;0;0;0m${OBC_EXECUTOR_URL}\033[0m
  \033[0m"
else
  sudo docker-compose down
fi


