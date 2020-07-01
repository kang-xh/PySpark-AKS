cd /home/allenk/github/PySpark-AKS/environment/aks/image/kangxh-python-azure

docker image build -t python-azure:2020.6 -f Dockerfile .

docker tag python-azure:2020.6 kangxh/python-azure:latest
docker push kangxh/python-azure:latest