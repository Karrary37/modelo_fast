#!/bin/bash

if [[ $CNAME == 'roteador-contrato' ]]
then
    echo 'Start NGINX'
    service nginx start
    echo '------------------'
    echo 'Start Application'
    newrelic-admin run-program \
        uvicorn main:app \
        --host ${GUNICORNADDRESS} \
        --port ${GUNICORNPORT}
fi
