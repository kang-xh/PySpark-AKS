##### Generate TPC-DS data

    clone from https://github.com/maropu/spark-tpcds-datagen.git

##### Benchmark - run from WSL for functionality test

cd ~/github/spark-tpcds-datagen/
./bin/dsdgen --output-location ~/tpc/spark-tpcds-data --scale-factor 1 --format csv

# Github spark folder
export SPARK_HOME=/home/allenk/github/spark
# prebuild spark folder with ABFS access.
export SPARK_HOME=/home/allenk/spark/spark-3.0.0-bin-hadoop3.2

cd ~/github/spark
./bin/spark-submit \
    --class org.apache.spark.sql.execution.benchmark.TPCDSQueryBenchmark \
    sql/core/target/spark-sql_2.12-3.1.0-SNAPSHOT-tests.jar \
    --data-location ~/tpc/spark-tpcds-data

./bin/spark-submit \
    --class org.apache.spark.sql.execution.benchmark.TPCDSQueryBenchmark \
    ~/github/spark/sql/core/target/spark-sql_2.12-3.1.0-SNAPSHOT-tests.jar \
    --data-location ~/tpc/spark-tpcds-data
