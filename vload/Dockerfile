FROM python:3.6.4

RUN mkdir /code \
&&apt-get update \
&&apt-get -y install freetds-dev

COPY /source /code 
COPY /requirement.txt /code

RUN pip install --upgrade pip
RUN pip install -r /code/requirement.txt -i https://pypi.douban.com/simple

WORKDIR /code
ENTRYPOINT ["python3","/code/vload.py"]