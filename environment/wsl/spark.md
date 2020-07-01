##### prepare spark env in WSL

    # install openjdk
    sudo apt-get install openjdk-8-jdk

    # install hadoop 3.2
    https://kontext.tech/column/hadoop/307/install-hadoop-320-on-windows-10-using-windows-subsystem-for-linux-wsl
    wget https://downloads.apache.org/spark/spark-3.0.0/spark-3.0.0-bin-hadoop3.2.tgz
    
    # install spark. 
    https://kontext.tech/column/spark/311/apache-spark-243-installation-on-windows-10-using-windows-subsystem-for-linux

    # after this step, WSL should be able to run spark-shell with sc master = local[*]

    # add ADLS G2 support to run local spark job.
    https://docs.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-abfs-driver
    https://hadoop.apache.org/docs/stable/hadoop-azure/abfs.html

    hdfs dfs -ls abfs://sample@kangxhadlsgen2sea.dfs.core.windows.net/

##### Run Test jobs on local spark

    # test job without storage access
    spark-submit /home/allenk/github/PySpark-AKS/jobs//spark-pi.py 5

    3 test job with ADLS data read.
    spark-submit /home/allenk/github/PySpark-AKS/jobs//spark-read-adls-csv.py

##### prepare spark to access azure resource

    cp ~/hadoop/share/hadoop/tools/lib/hadoop-az* $SPARK_HOME/jars/
    cp ~/hadoop/share/hadoop/tools/lib/az* $SPARK_HOME/jars/

    cp ~/hadoop/share/hadoop/tools/lib/wildfly-openssl-1.0.7.Final.jar $SPARK_HOME/jars/

##### connect spark to aks and submit some test job. 

    https://spark.apache.org/docs/2.3.0/running-on-kubernetes.html

    Locate the spark job in the a Azure File Share PVC which will be moutned in the Driver PoD. Test to ensure spark job can be submitted without ADLS access. 

    NAME                   CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                           STORAGECLASS   REASON   AGE
    adls-file-pyspark-pv   5Gi        RWX            Retain           Bound    default/adls-file-pyspark-pvc   azurefile               5d17h

    NAME                    STATUS   VOLUME                 CAPACITY   ACCESS MODES   STORAGECLASS   AGE
    adls-file-pyspark-pvc   Bound    adls-file-pyspark-pv   5Gi        RWX            azurefile      5d17h

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



