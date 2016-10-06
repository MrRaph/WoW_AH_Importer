#!/bin/bash

export APP_DIR="/usr/src/app"
export APP_DIR="/home/raphael/ownCloud/Documents/Perso/Developpement/Python/WoW/Wow_AH_Importer/app"

if [[ ! -z ${ACTION} && ! -z ${SERVICE_NAME} && ! -z ${RABBIT_HOST} ]]
then
  echo "We'll ${ACTION} nameko service ${SERVICE_NAME}"
  cd ${APP_DIR}
  # AMQP_HOST=$(grep AMQP_URI config.yml  | awk -F'@' '{print $2}' | sed -e "s/'//")
  AMQP_IP=$(ping -c 1 ${RABBIT_HOST} | grep " bytes from " | awk -F':' '{print $1}' | awk '{print $4}')
else
  exit 1
fi

if [[ ! -z ${MONGO_HOST} ]]
then
  MONGO_IP=$(ping -c 1 ${MONGO_HOST} | grep " bytes from " | awk -F':' '{print $1}' | awk '{print $4}')
fi
