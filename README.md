# huawei_lte_api_web
Controller for huawei router

## USAGE
docker run -d \
        --name huaweiweb \
        -e API_USER=admin \
        -e API_PASSW=[PASSWORD] \
        -e API_IP=192.168.1.1 \
        -p [YOUR_PORT]:2233 \
        --restart=always \
        ghcr.io/cumal/huawei_lte_api_web:0.0.1

## Refs
https://github.com/Salamek/huawei-lte-api

