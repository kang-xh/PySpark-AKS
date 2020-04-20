## input:  csv files in landing zone
# proces: remove the verbose column
# output: save the process data to taxi container

# reference the code in https://github.com/Microsoft/Azure-Databricks-NYC-Taxi-Workshop
import string
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import StructType, StructField, StringType, IntegerType,LongType,FloatType,DoubleType, TimestampType

# srcDataFile = "68f400a7-5c1e-4039-9b24-1018382d3584.csv"
srcDataFile = "02288b32-c246-46ae-8b62-d51e2bdf38a6.csv"
# srcDataDirRoot = "/home/allenk/github/PySpark-AKS/spark/sample/cab/" 
#destDataDirRoot = "/home/allenk/tmp/" 
srcDataDirRoot = "abfs://landingzone@kangxhadlsgen2sea.dfs.core.windows.net/"
destDataDirRoot = "abfs://cleansing@kangxhadlsgen2sea.dfs.core.windows.net/" 

TripSchemaColList = ["year", "month", "day", "city", "vendor","pickup_time","pickup_zone","dropoff_time","dropoff_zone","trip_time_by_sec","fare","tips","total", "tips_rate"]

TripSchema = StructType([
    StructField("vendor", StringType(), True),
    StructField("pickup_zone", IntegerType(), True),
    StructField("dropoff_zone", IntegerType(), True),
    StructField("trip_time_by_sec", IntegerType(), True),
    StructField("pickup_time", TimestampType(), True),
    StructField("dropoff_time", TimestampType(), True),
    StructField("fare", DoubleType(), True),
    StructField("tips", DoubleType(), True),
    StructField("total", DoubleType(), True),
    StructField("verbose", StringType(), True)])

# clearnsing the data by remove the verbose column and create 3 new column: Year, Month, TipRate
def cleansingTripDataframe(sourceDF):
    sourceDF = (sourceDF 
        .withColumn("city", lit("shanghai")) 
        .withColumn("tips_rate", round(col("tips")/col("total"),2)) 
        .withColumn("year", substring(col("pickup_time"),0, 4)) 
        .withColumn("month", substring(col("pickup_time"),6, 2)) 
        .withColumn("day", substring(col("pickup_time"),9, 2)) 
        .drop("verbose"))

    return sourceDF

spark = SparkSession.builder.master("local[*]").appName("taxi-clearnsing") \
    .config("fs.azure.account.auth.type.kangxhadlsgen2sea.dfs.core.windows.net", "SharedKey") \
    .config("fs.azure.account.key.kangxhadlsgen2sea.dfs.core.windows.net", "HQQYSGMjr1+JuMz7sUEY1hBfetU6kIm8i/TI8MvygCbbpuYP9PHkupQM4ypmslbancEcxrqbAPNIcgk3zZrcyQ==") \
    .getOrCreate()

rawTripDF = spark.read.format('csv').option('header',True).option('sep', ',').load(srcDataDirRoot+srcDataFile)
cleanTripDF = cleansingTripDataframe(rawTripDF).select(*TripSchemaColList)

# save output to parquet with partition
# cleanTripDF.show()
cleanTripDF.write.format("parquet").mode("append").partitionBy("city","year","month","day", "vendor").save(destDataDirRoot)  
