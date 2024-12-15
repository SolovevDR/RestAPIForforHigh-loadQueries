FROM python:3.11-bullseye as base

WORKDIR /app

COPY ./worker/requirements.txt ./
RUN apt update && pip install --upgrade pip && pip3 install -r requirements.txt

COPY ./worker ./
COPY src/models/models.py ./

CMD ["python3", "worker.py"]
