##### test jobs from WSL2

##### Data Inject

    Data inject is by vload PoD running in AKS to insert data to: 

    1. ADLS Gen2 - kangxhadlsgen2sea
    2. EventHub  - kangxheventhubsea  (not ready)

##### Data Cleansing

    spark jobs to remove verbose column, create addition column and save to as parquet with partition
    spark-submit local:///home/allenk/github/PySpark-AKS/jobs/taxi/spark-cleansing.py