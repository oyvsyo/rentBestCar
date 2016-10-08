#!/bin/sh
if [ -z "$RUN_ENV" ]; then
    echo 'Please set up RUN_ENV variable'
    exit 1
fi

if [ "$RUN_ENV" = "PROD" ]; then
    git pull
    docker-compose -f docker-compose.prod.yml stop
    docker-compose -f docker-compose.prod.yml rm -f
    docker-compose -f docker-compose.prod.yml up -d
fi

if [ "$RUN_ENV" = "DEV" ]; then
    docker-compose -f docker-compose.dev.yml stop
    docker-compose -f docker-compose.dev.yml rm -f
    docker-compose -f docker-compose.dev.yml up -d
fi

if [ "$RUN_ENV" = "STAGE" ]; then
    git pull

    if [ "$1" = "stage" ]; then
        docker-compose -f docker-compose.stage.yml stop
        docker-compose -f docker-compose.stage.yml rm -f
        docker-compose -f docker-compose.stage.yml up -d
    elif [ "$1" = "test" ]; then
        docker-compose -f docker-compose.test.yml stop
        docker-compose -f docker-compose.test.yml rm -f
        docker-compose -f docker-compose.test.yml up -d
    else
        echo "Enter parameter for redeploy: [stage, test], please."
    fi
fi