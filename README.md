#### PySpark-AKS

    Running PySpark and Notebook on AKS for big data studay. 

#### AKS setup

    refer to Github Repo PoC-AKS for configuration, including: 
    - Basic AKS setup
    - vLoad PoD deployment 
    - Spark PV and PVC configuration is including in this repo under aks.

#### process guide: 

    http://spark.apache.org/docs/latest/running-on-kubernetes.html

    - follow the guide in spark folder to setup spark with hadoop in WSL2. 
    - verify spark job works in WSL to access HDFS and ADLS Gen2. 
    - follow the guide in aks folder to submit jobs to AKS cluster.  