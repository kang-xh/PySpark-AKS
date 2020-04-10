from pyspark.sql import SparkSession

appName = "Python Example - PySpark Read local CSV"
master = 'local'

# Create Spark session
spark = SparkSession.builder \
    .master(master) \
    .appName(appName) \
    .getOrCreate()

# Convert list to data frame
df = spark.read.format('csv') \
                .option('header',True) \
                .option('sep', ',') \
                .load('hdfs:///sample/csv/sales.tsv')

# local         .load('/home/allenk/sample/csv/sales.csv')
# hdfs          .load('hdfs:///sample/csv/sales.tsv')
# adls gen2     .load('abfs://sample@kangxhadlsgen2sea.dfs.core.windows.net/csv/sales.csv')

df.show()