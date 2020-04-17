# vendor,pickup_zone,dropoff_zone,trip_time_by_sec,pickup_time,dropoff_time,fare,tips,total,verbose

import random, string, csv, uuid, os
from threading import Thread
from datetime import datetime, timedelta
from time import time, sleep
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

if ("AZURE_STORAGE_CONNECTION_STRING" in os.environ and os.environ['AZURE_STORAGE_CONNECTION_STRING']):
    AZURE_STORAGE_CONNECTION_STRING = os.environ['VOTE1VALUE']
else:
    AZURE_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=kangxhadlsgen2sea;AccountKey=HQQYSGMjr1+JuMz7sUEY1hBfetU6kIm8i/TI8MvygCbbpuYP9PHkupQM4ypmslbancEcxrqbAPNIcgk3zZrcyQ==;EndpointSuffix=core.windows.net"

if ("CONTAINER_NAME" in os.environ and os.environ['CONTAINER_NAME']):
    CONTAINER_NAME = os.environ['CONTAINER_NAME']
else:
    CONTAINER_NAME = "landingzone"

if ("THREAD_COUNT" in os.environ and os.environ['THREAD_COUNT']):
    THREAD_COUNT = int(os.environ['THREAD_COUNT'])
else:
    THREAD_COUNT = 5

if ("GENERATE_BLOB_LOAD" in os.environ and os.environ['GENERATE_BLOB_LOAD']):
    GENERATE_BLOB_LOAD = os.environ['GENERATE_BLOB_LOAD']
else:
    GENERATE_BLOB_LOAD = True

if ("LOAD_SLEEP_TIME_IN_SEC" in os.environ and os.environ['LOAD_SLEEP_TIME_IN_SEC']): 
    LOAD_SLEEP_TIME_IN_SEC = int(os.environ['LOAD_SLEEP_TIME_IN_SEC'])
else:
    LOAD_SLEEP_TIME_IN_SEC = 60

def create_TaxiRecord():
    VENDER_LIST = ["yellow", "blue", "green"]

    vendor = VENDER_LIST[random.randint(0,2)]
    pickup_zone = random.randint(1,20)
    dropoff_zone = random.randint(1,20)
    trip_time_by_sec = 300 + random.randint(0,7200)
    pickup_time = datetime.now()
    dropoff_time = pickup_time + timedelta(seconds = trip_time_by_sec)
    fare  = trip_time_by_sec * random.randint(3,5) / 100.0
    tips = fare * random.randint(3,10) / 100.0
    total = fare + tips
    verbose = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(768)])
    return [vendor, str(pickup_zone), str(dropoff_zone), str(trip_time_by_sec), str(pickup_time), str(dropoff_time), "{:.2f}".format(fare), "{:.2f}".format(tips), "{:.2f}".format(total), verbose]

# thread function to create a 
def Create_RecordFile_AzureBlob(threadName, connect_str, container_name, delay):
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container = container_name

    filename = str(uuid.uuid4())+".csv"

    with open(filename, 'w') as csvfile:
        recordwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        recordwriter.writerow(["vendor","pickup_zone","dropoff_zone","trip_time_by_sec","pickup_time","dropoff_time","fare","tips","total","verbose"])

        for n in range(2390):  # create a record file about 2MB
            recordwriter.writerow(create_TaxiRecord()) 

        with open(filename, 'rb') as data:    
            blob_client = blob_service_client.get_blob_client(container=container, blob=filename)
            blob_client.upload_blob(data)
            print ("create blob from tread: " + threadName)

    print ("delete local cache file: " + threadName)
    os.remove(filename)

while (GENERATE_BLOB_LOAD):
    for threadID in range(THREAD_COUNT):
        Thread(target= Create_RecordFile_AzureBlob, kwargs={"threadName": "Thread-"+str(threadID), "connect_str": AZURE_STORAGE_CONNECTION_STRING, "container_name": CONTAINER_NAME, "delay":5},).start()
    sleep(LOAD_SLEEP_TIME_IN_SEC)
