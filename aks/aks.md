##### Setup AKS cluster as normal 

    suggested node pool size above D3s. 
    using B4 vm in lab. 

##### Create a service role binding for spark: 

kubectl create serviceaccount spark
kubectl create clusterrolebinding spark-role --clusterrole=edit --serviceaccount=default:spark --namespace=default

##### Create spark image in ACR

    # build spark docker image: 
    az acr login --resource-group MSDNRGKangxhAKS --name kangxhacrsea
    docker-image-tool.sh -r kangxhacrsea.azurecr.io -t v3.3.0 -p kubernetes/dockerfiles/spark/bindings/python/Dockerfile build
    docker-image-tool.sh -r kangxhacrsea.azurecr.io -t v3.3.0 -p kubernetes/dockerfiles/spark/bindings/python/Dockerfile push

##### create Azure File PV for AKS

    export STORAGE_KEY=HQQYSGMjr1+JuMz7sUEY1hBfetU6kIm8i/TI8MvygCbbpuYP9PHkupQM4ypmslbancEcxrqbAPNIcgk3zZrcyQ==
    export STORAGE_ACCOUNT_NAME=kangxhadlsgen2sea

    kubectl create secret generic azure-adls-secret --from-literal=azurestorageaccountname=$STORAGE_ACCOUNT_NAME --from-literal=azurestorageaccountkey=$STORAGE_KEY

    kubectl apply -f spark-azurefile-pv.yaml
    kubectl apply -f spark-azurefile-pvc.yaml

##### trigger Spark job from WSL

sample without external storage dependence. 

    spark-submit \
        --master k8s://kangxhakss-msdnrgkangxhseaa-e7c1ea-e246302a.hcp.southeastasia.azmk8s.io:443 \
        --deploy-mode cluster \
        --name spark-pi \
        --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
        --conf spark.executor.instances=3 \
        --conf spark.kubernetes.container.image=kangxhacrsea.azurecr.io/spark-py:v3.3.0 \
        https://kangxhadlsgen2sea.blob.core.windows.net/pyspark/spark-pi.py

    driver pod will keep at completed status for job result. 

    NAME                                           TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)                      AGE
    service/kubernetes                             ClusterIP   192.168.0.1   <none>        443/TCP                      4d11h
    service/spark-pi-d9ad0371637353a6-driver-svc   ClusterIP   None          <none>        7078/TCP,7079/TCP,4040/TCP   70m

    # sample to use pvc where we can save the job code 
    spark-submit \
        --master k8s://kangxhakss-msdnrgkangxhseaa-e7c1ea-e246302a.hcp.southeastasia.azmk8s.io:443 \
        --deploy-mode cluster \
        --name spark-pi \
        --conf spark.executor.instances=3 \
        --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
        --conf spark.kubernetes.container.image=kangxhacrsea.azurecr.io/spark-py:v3.3.0 \
        --conf spark.kubernetes.driver.volumes.persistentVolumeClaim.adlsfile.options.claimName=adls-file-pyspark-pvc \
        --conf spark.kubernetes.driver.volumes.persistentVolumeClaim.adlsfile.mount.path=/mnt/pysparkapp \
        local:///mnt/pysparkapp/spark-pi.py

