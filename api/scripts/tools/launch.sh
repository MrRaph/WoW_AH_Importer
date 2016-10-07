#!/bin/bash

export APP_DIR="/usr/src/app"
export MANAGE=$(which manage)
# export APP_DIR="/home/raphael/ownCloud/Documents/Perso/Developpement/Python/WoW/Wow_AH_Importer/app"

if [[ ! -z ${RABBIT_HOST} ]]
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
  # echo "AMQP_URI: '${AMQP_URI}'" >> ${APP_DIR}/config.yml
  sed -i "s/#AMQP#/${AMQP_URI}/" ${APP_DIR}/api.py

else
  echo "Missing Service or RabbitMQ env ..."
  exit 1
fi

tail -f /var/log/supervisor/* &
TAIL_PID=$!

cd ${APP_DIR}
${MANAGE} run

kill $TAIL_PID
wait $TAIL_PID
