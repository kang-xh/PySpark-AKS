#### Running Spark on Kubernetes

    1. setup mini spark env on WSL. 
    2. test WSL with sc master=local[*]
    3. follow apache spark doc to prepare image for AKS. 
    4. put images to ACR

    https://spark.apache.org/docs/2.3.0/running-on-kubernetes.html
    
    use WSL as client to submit spark job. 

##### prepare spark env in WSL

    # install openjdk
    sudo apt-get install openjdk-8-jdk

    # install hadoop 3.2
    https://kontext.tech/column/hadoop/307/install-hadoop-320-on-windows-10-using-windows-subsystem-for-linux-wsl
    wget https://mirror.bit.edu.cn/apache/hadoop/common/hadoop-3.2.1/hadoop-3.2.1.tar.gz
    
    # install spark. 
    https://kontext.tech/column/spark/311/apache-spark-243-installation-on-windows-10-using-windows-subsystem-for-linux

    wget https://mirrors.tuna.tsinghua.edu.cn/apache/spark/spark-2.4.5/spark-2.4.5-bin-hadoop2.7.tgz
    tar -xvzf spark-2.4.5-bin-hadoop3.0.tgz -C ~/hadoop

    # after this step, WSL should be able to run spark-shell with sc master = local[*]

    # add ADLS G2 support to run local spark job.
    https://docs.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-abfs-driver
    https://hadoop.apache.org/docs/stable/hadoop-azure/abfs.html

    hdfs dfs -ls abfs://sample@kangxhadlsgen2sea.dfs.core.windows.net/
    spark-submit /sample/python/spark-read-adls-csv.py

    *Spark job could report error about Class Not found, etc. copy Jars from hadoop/share/hadoop/tools/lib to spark/jars.

##### samples: 

    use spark-pi 5 to calculate PI with 5 Executor, no dependence for storage.

##### connect spark to aks. 

    https://spark.apache.org/docs/2.3.0/running-on-kubernetes.html

    # build spark docker image: 
    az acr login --resource-group MSDNRGKangxhAKS --name kangxhacrsea
    $SPARK_HOME/bin/docker-image-tool.sh -r kangxhacrsea.azurecr.io -t aks build
    $SPARK_HOME/bin/docker-image-tool.sh -r kangxhacrsea.azurecr.io -t aks push






