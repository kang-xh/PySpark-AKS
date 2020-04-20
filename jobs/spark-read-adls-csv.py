from pyspark.sql import SparkSession

appName = "Python Example - PySpark Read ADLS CSV"
master = 'local'

# Create Spark session
spark = SparkSession.builder \
    .master(master) \
    .appName(appName) \
    .config("fs.azure.account.auth.type.kangxhadlsgen2sea.dfs.core.windows.net", "SharedKey") \
    .config("fs.azure.account.key.kangxhadlsgen2sea.dfs.core.windows.net", "HQQYSGMjr1+JuMz7sUEY1hBfetU6kIm8i/TI8MvygCbbpuYP9PHkupQM4ypmslbancEcxrqbAPNIcgk3zZrcyQ==") \
    .getOrCreate()

# Convert list to data frame
df = spark.read.format('csv') \
    .option('header',True) \
    .option('sep', ',') \
    .load('abfs://sample@kangxhadlsgen2sea.dfs.core.windows.net/csv/sales.csv')

df.show()