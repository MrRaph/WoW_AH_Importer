#!/bin/bash

export APP_DIR="/usr/src/app"
export NAMEKO=$(which nameko)
# export APP_DIR="/home/raphael/ownCloud/Documents/Perso/Developpement/Python/WoW/Wow_AH_Importer/app"

if [[ ! -z ${ACTION} && ! -z ${SERVICE_NAME} && ! -z ${RABBIT_HOST} ]]
then
  # echo "We'll ${ACTION} nameko service ${SERVICE_NAME}"
  export AMQP_IP=$(ping -c 1 ${RABBIT_HOST} | grep " bytes from " | awk -F':' '{print $1}' | awk '{print $4}')

  if [[ -z ${RABBIT_USER} ]]
  then
    export RABBIT_USER=guest
  fi

  if [[ -z ${RABBIT_PASS} ]]
  then
    export RABBIT_PASS=guest
  fi

  export AMQP_URI="amqp://${RABBIT_USER}:${RABBIT_PASS}@${AMQP_IP}"

else
  echo "Missing Service or RabbitMQ env ..."
  exit 1
fi

if [[ ! -z ${MONGO_HOST} ]]
then
  export MONGO_IP=$(ping -c 1 ${MONGO_HOST} | grep " bytes from " | awk -F':' '{print $1}' | awk '{print $4}')

    if [[ ! -z ${MONGO_DB} && ! -z ${MONGO_USER} && ! -z ${MONGO_PASS} ]]
    then
      export MONGO_URI="mongodb://${MONGO_USER}:${MONGO_PASS}@${MONGO_IP}/${MONGO_DB}"
    else
      echo "Missing Mongo env ..."
      exit 1
    fi
fi

cd ${APP_DIR}
${NAMEKO} ${ACTION} --broker=${AMQP_URI} --config=${APP_DIR}/config.yml ${SERVICE_NAME}
