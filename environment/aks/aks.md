##### Create a service role binding for spark: 

kubectl create serviceaccount spark
kubectl create clusterrolebinding spark-role --clusterrole=edit --serviceaccount=default:spark --namespace=default

##### Create spark image in ACR - Run commands from WSL

    # build spark docker image: 
    az acr login --resource-group az-rg-kangxh-aks --name kangxhacrsea
    cd $SPARK_HOME
    docker-image-tool.sh -r kangxhacrsea.azurecr.io -t v3.0.1 -p kubernetes/dockerfiles/spark/bindings/python/Dockerfile build
    docker-image-tool.sh -r kangxhacrsea.azurecr.io -t v3.0.1 -p kubernetes/dockerfiles/spark/bindings/python/Dockerfile push

##### create Azure File PV for AKS

    cd /home/allenk/github/PySpark-AKS/environment/aks

    export STORAGE_KEY=abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd
    export STORAGE_ACCOUNT_NAME=kangxhadlsgen2sea

    kubectl create secret generic azure-adls-secret --from-literal=azurestorageaccountname=$STORAGE_ACCOUNT_NAME --from-literal=azurestorageaccountkey=$STORAGE_KEY

    kubectl apply -f spark-azurefile-pv.yaml
    kubectl apply -f spark-azurefile-pvc.yaml

##### trigger Spark job on AKS from WSL

    # sample to use pvc where we can save the job code 
    spark-submit \
        --master k8s://kangxhakss-az-rg-kangxh-aks-9c6835-eb765b68.hcp.southeastasia.azmk8s.io:443 \
        --deploy-mode cluster \
        --name spark-pi \
        --conf spark.executor.instances=3 \
        --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
        --conf spark.kubernetes.container.image=kangxhacrsea.azurecr.io/spark-py:v3.0.1 \
        --conf spark.kubernetes.driver.volumes.persistentVolumeClaim.adlsfile.options.claimName=adls-file-pyspark-pvc \
        --conf spark.kubernetes.driver.volumes.persistentVolumeClaim.adlsfile.mount.path=/mnt/pysparkapp \
        local:///mnt/pysparkapp/spark-pi.py

    spark-submit \
        --master k8s://kangxhakss-az-rg-kangxh-aks-9c6835-eb765b68.hcp.southeastasia.azmk8s.io:443 \
        --deploy-mode cluster \
        --name spark-adls \
        --conf spark.executor.instances=3 \
        --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
        --conf spark.kubernetes.container.image=kangxhacrsea.azurecr.io/spark-py:v3.0.1 \
        --conf spark.kubernetes.driver.volumes.persistentVolumeClaim.adlsfile.options.claimName=adls-file-pyspark-pvc \
        --conf spark.kubernetes.driver.volumes.persistentVolumeClaim.adlsfile.mount.path=/mnt/pysparkapp \
        local:///mnt/pysparkapp/spark-read-adls-csv.py
