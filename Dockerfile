FROM python:3.10-alpine
RUN apk add python3 python3-dev g++ unixodbc-dev
RUN python3 -m ensurepip
RUN pip3 install --user pyodbc
RUN apk add --upgrade font-dejavu
WORKDIR /app
COPY ./noofa-app ./noofa-app
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
CMD ["uvicorn", "noofa-app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
