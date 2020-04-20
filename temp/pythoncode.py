import random, string, csv, uuid, os
from threading import Thread
from datetime import datetime, timedelta
from time import time, sleep
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient    
    
import pyodbc

"jdbc:sqlserver://kangxhsqlserversea.database.windows.net:1433;database=kangxhsqldbsea;user=allenk@kangxhsqlserversea;password=L04N8Bmv12zWdMd;encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.database.windows.net;loginTimeout=30;"
server = 'kangxhsqlserversea.database.windows.net'
database = 'kangxhsqldbsea'
username = 'allenk'
password = 'L04N8Bmv12zWdMd'
driver= '{ODBC Driver 17 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
cursor.execute("SELECT TOP 20 pc.Name as CategoryName, p.name as ProductName FROM [SalesLT].[ProductCategory] pc JOIN [SalesLT].[Product] p ON pc.productcategoryid = p.productcategoryid")
row = cursor.fetchone()
while row:
    print (str(row[0]) + " " + str(row[1]))
    row = cursor.fetchone()