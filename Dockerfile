FROM python:3.10
RUN apt-get update
RUN apt-get install g++ unixodbc-dev -y
RUN python3 -m ensurepip
RUN pip3 install --user pyodbc
WORKDIR /app
COPY ./noofa-app ./noofa-app
COPY ./requirements.txt ./
RUN pip install -U pip
RUN pip install -r requirements.txt