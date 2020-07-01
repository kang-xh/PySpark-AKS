# This image included necessary component to use Python for Azure environment. 

FROM python:3.6.4

ENV ACCEPT_EULA=Y

# Microsoft SQL Server Prerequisites
RUN apt-get update \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl curl https://packages.microsoft.com/config/debian/8/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get install -y --no-install-recommends locales apt-transport-https \
    && apt-get update \
    && apt-get -y --no-install-recommends install unixodbc-dev msodbcsql17 mssql-tools

ENV PATH=$PATH:/opt/mssql-tools/bin 

RUN pip install --upgrade pip

# detailed list from https://azure.github.io/azure-sdk/releases/latest/all/python.html
RUN pip install pyodbc \
    && pip install azure-storage-blob \
    && pip install azure-storage-file-share \
    && pip install azure-storage-file-datalake \
    && pip install azure-storage-queue \
    && pip install azure-monitor \
    && pip install azure-eventhub \
    && pip install azure-identity \
    && pip install azure-keyvault-secrets \
    && pip install azure-loganalytics 

ENTRYPOINT ["/bin/sh"]


