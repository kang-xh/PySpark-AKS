# create workload in Blob, SQL and Event Hub.
# the generated data is with same schema for TaxiRecord
# vendor,pickup_zone,dropoff_zone,trip_time_by_sec,pickup_time,dropoff_time,fare,tips,total,verbose

import random, string, csv, uuid, os
from threading import Thread
from datetime import datetime, timedelta
from time import time, sleep
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import pyodbc

if ("RUNTIME_ENV" in os.environ and os.environ['RUNTIME_ENV']):
    RUNTIME_ENV = str(os.environ['RUNTIME_ENV'])
else:
    RUNTIME_ENV = "LOCAL"
    BLOB_GENERATE_LOAD = True
    BLOB_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=sclce2corestorage;AccountKey=krspwUWBwffi3L9VoFjg74okMjAD1sCtc5Ttxqz/ljdB4CePJX1fQY94CaecrijZCIkPNMNACDtdI601T5o3rA==;EndpointSuffix=core.chinacloudapi.cn"
    BLOB_CONTAINER_NAME = "landingzone"
    BLOB_THREAD_COUNT = 2
    BLOB_SLEEP_TIME_IN_SEC= 60

    SQL_GENERATE_LOAD = False
    SQL_CONNECTION_STRING = "jdbc:sqlserver://kangxhsqlserversea.database.windows.net:1433;database=kangxhsqldbsea;user=allenk@kangxhsqlserversea;password=L04N8Bmv12zWdMd;encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.database.windows.net;loginTimeout=30;"
    SQL_TABLE_NAME = "[dbo].[taxi.order]"
    SQL_THREAD_COUNT = 2
    SQL_SLEEP_TIME_IN_SEC= 60

if (RUNTIME_ENV == "AKS") :
    if ("SQL_GENERATE_LOAD" in os.environ and os.environ['SQL_GENERATE_LOAD']):
        SQL_GENERATE_LOAD = bool(os.environ['SQL_GENERATE_LOAD']=="True")
    else:
        SQL_GENERATE_LOAD = False

    if SQL_GENERATE_LOAD:
        SQL_CONNECTION_STRING = str(os.environ['SQL_CONNECTION_STRING'])
        SQL_TABLE_NAME = str(os.environ['SQL_TABLE_NAME'])
        SQL_THREAD_COUNT = int(os.environ['SQL_THREAD_COUNT'])
        SQL_SLEEP_TIME_IN_SEC= int(os.environ['SQL_SLEEP_TIME_IN_SEC'])

    if ("BLOB_GENERATE_LOAD" in os.environ and os.environ['BLOB_GENERATE_LOAD']):
        BLOB_GENERATE_LOAD = bool(os.environ['BLOB_GENERATE_LOAD']=="True")
    else:
        BLOB_GENERATE_LOAD = False

    if BLOB_GENERATE_LOAD:
        BLOB_CONNECTION_STRING = str(os.environ['BLOB_CONNECTION_STRING'])
        BLOB_CONTAINER_NAME = str(os.environ['BLOB_CONTAINER_NAME'])
        BLOB_THREAD_COUNT = int(os.environ['BLOB_THREAD_COUNT'])
        BLOB_SLEEP_TIME_IN_SEC= int(os.environ['BLOB_SLEEP_TIME_IN_SEC'])

# generate Texi Order for blob, sql and stream
def create_TaxiRecord(load_type):

    # "yellow", "blue", "green" for blob. "black", "orange" for SQLDB, "gray","white" for Eventhub Streaming

    VENDER_LIST = ["yellow", "blue", "green", "red", "black", "orange", "gray","white"]
    load_switch = {
        "blob": lambda type: VENDER_LIST[random.randint(0,2)],
        "sql": lambda type: VENDER_LIST[random.randint(3,4)],
        "stream": lambda type: VENDER_LIST[random.randint(5,7)]
    }
    vendor = load_switch[load_type](load_type)

    pickup_zone = random.randint(1,20)
    dropoff_zone = random.randint(1,20)
    
    trip_time_by_sec = 300 + random.randint(0,7200)
    current_time = datetime.now()
    pickup_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dropoff_time = (current_time + timedelta(seconds = trip_time_by_sec)).strftime("%Y-%m-%d %H:%M:%S")

    fare  = trip_time_by_sec * random.randint(3,5) / 100.0
    tips = fare * random.randint(3,10) / 100.0
    total = fare + tips

    verbose = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(768)])

    return [vendor, pickup_zone, dropoff_zone, trip_time_by_sec, pickup_time, dropoff_time, float("{:.2f}".format(fare)), float("{:.2f}".format(tips)), float("{:.2f}".format(total)), verbose]

# thread function to generate load, depends on level of load, create multiple thread to generate load.
def Create_RecordFile_AzureBlob(threadName, connect_str, container_name, delay):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        while(blob_service_client):
            print(str(datetime.now()) + " - " + threadName + " enter workload loop")

            filename = str(uuid.uuid4())+".csv"
            with open(filename, 'w') as csvfile:
                recordwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                recordwriter.writerow(["vendor","pickup_zone","dropoff_zone","trip_time_by_sec","pickup_time","dropoff_time","fare","tips","total","verbose"])
                for n in range(2390):  # create a record file about 2MB
                    recordwriter.writerow(create_TaxiRecord("blob")) 

            print (str(datetime.now())+ " - create blob from tread " + threadName + ": " + filename)
            with open(filename, 'rb') as data:    
                blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
                blob_client.upload_blob(data)
                blob_client.close

            os.remove(filename)
            print (str(datetime.now())+ " - delete local cache file from " + threadName + ": " + filename)
            sleep(delay)
    except:
        print(datetime.now() + " - " + threadName + " end")

def Create_RecordSQL_AzureSQL(threadName, connect_str, table_name, delay):
    server = connect_str[connect_str.find("sqlserver://") + len("sqlserver://") : connect_str.find(":1433")]
    database = connect_str[connect_str.find("database=") + len("database=") : connect_str.find(";user=")]
    username = connect_str[connect_str.find("user=") + len("user=") : connect_str.find("@", connect_str.find("user=") + len("user="))]
    password = connect_str[connect_str.find("password=") + len("password=") : connect_str.find(";encrypt=true")]
    driver= "{ODBC Driver 17 for SQL Server}"

    sqlconnect = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password, autocommit=True)
    cursor = sqlconnect.cursor()

    while(True):
        new_order = create_TaxiRecord("sql")
        new_order_str = "'"+"','".join([str(item) for item in new_order])+"'"
        query_str = "insert into [dbo].[taxi.order] values (%s)" % new_order_str

        cursor.execute(query_str)
        print(str(datetime.now())+ " - insert one entry to Azure SQL DB from " + threadName)
        sleep(delay)

    sqlconnect.close()

def Create_RecordMsg_EventHub(threadName, connect_str, delay):
    print ("create Message Record from tread: " + threadName)

# start to create thread to generate workload
print(str(BLOB_GENERATE_LOAD))
if BLOB_GENERATE_LOAD==True:
    print(str(datetime.now())+ " - Creating threads to genereate BLOB workload")
    for threadID in range(BLOB_THREAD_COUNT):
        Thread(target= Create_RecordFile_AzureBlob, kwargs={"threadName": "BLOB-Thread-"+str(threadID), "connect_str": BLOB_CONNECTION_STRING, "container_name": BLOB_CONTAINER_NAME, "delay":BLOB_SLEEP_TIME_IN_SEC},).start()
        print(str(datetime.now())+ " - BLOB-Thread-" +str(threadID) + " created")

print(str(SQL_GENERATE_LOAD))
if SQL_GENERATE_LOAD==True:
    print(str(datetime.now())+ " - Creating threads to genereate SQL workload")
    for threadID in range(SQL_THREAD_COUNT):
        Thread(target= Create_RecordSQL_AzureSQL, kwargs={"threadName": "SQL-Thread-"+str(threadID), "connect_str": SQL_CONNECTION_STRING, "table_name": SQL_TABLE_NAME, "delay":SQL_SLEEP_TIME_IN_SEC},).start()
        print(str(datetime.now())+ " - SQL-Thread-" +str(threadID) + " created")

