FROM kangxh-python-azure:2020.4

RUN mkdir /code 
COPY /source /code 

WORKDIR /code
ENTRYPOINT ["python3","/code/vload.py"]