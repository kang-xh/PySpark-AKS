cd /home/allenk/github/PySpark-AKS/vload

# create newest build
docker image build -t vload:test -f Dockerfile .

# start the container in WSL2 docker to verify function. it should directly create load using LOCAL configuration
docker run -it --rm  vload:test bash

# push the tested version to ACR 
docker tag vload:test docker.io/kangxh/vload:latest && docker push docker.io/kangxh/vload:latest

az acr login --resource-group MSDNRGKangxhSEAAKS --name kangxhacrsea
az acr import --source docker.io/kangxh/vload:latest --resource-group MSDNRGKangxhSEAAKS --name kangxhacrsea --image vload:latest --force


