FROM python:3.10
WORKDIR /app
COPY ./noofa-app ./noofa-app
COPY ./requirements.txt ./
RUN apt-get update
RUN apt-get install g++ unixodbc-dev -y
RUN pip install -r requirements.txt
CMD ["uvicorn", "noofa-app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]