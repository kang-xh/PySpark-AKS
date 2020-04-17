# create newest build
docker image build -t vload:test -f ~/github/PySpark-AKS/vload/Dockerfile ~/github/PySpark-AKS/vload/

# start the web site in WSL2 docker
docker run -it --rm  vload:test bash

# push the tested version to ACR 
docker tag vload:test docker.io/kangxh/vload:latest
docker push docker.io/kangxh/vload:latest

az acr login --resource-group MSDNRGKangxhSEAAKS --name kangxhacrsea
az acr import --source docker.io/kangxh/vload:latest --resource-group MSDNRGKangxhSEAAKS --name kangxhacrsea --image vload:latest --force



