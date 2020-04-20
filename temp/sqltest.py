# connect_str: "jdbc:sqlserver://kangxhsqlserversea.database.windows.net:1433;database=kangxhsqldbsea;user=allenk@kangxhsqlserversea;password=L04N8Bmv12zWdMd;encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.database.windows.net;loginTimeout=30;"
import pyodbc
import string

connect_str = "jdbc:sqlserver://kangxhsqlserversea.database.windows.net:1433;database=kangxhsqldbsea;user=allenk@kangxhsqlserversea;password=L04N8Bmv12zWdMd;encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.database.windows.net;loginTimeout=30;"

server = connect_str[connect_str.find("sqlserver://") + len("sqlserver://") : connect_str.find(":1433")]
database = connect_str[connect_str.find("database=") + len("database=") : connect_str.find(";user=")]
username = connect_str[connect_str.find("user=") + len("user=") : connect_str.find("@", connect_str.find("user=") + len("user="))]
password = connect_str[connect_str.find("password=") + len("password=") : connect_str.find(";encrypt=true")]
driver= "{ODBC Driver 17 for SQL Server}"

sqlconnect = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = sqlconnect.cursor()

cursor.execute("SELECT TOP 20 pc.Name as CategoryName, p.name as ProductName FROM [SalesLT].[ProductCategory] pc JOIN [SalesLT].[Product] p ON pc.productcategoryid = p.productcategoryid")
row = cursor.fetchone()
while row:
    print (str(row[0]) + " " + str(row[1]))
    row = cursor.fetchone()
