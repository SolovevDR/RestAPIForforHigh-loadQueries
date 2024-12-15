FROM python:3.11-bullseye as base

WORKDIR /app

COPY ./src/requirements.txt ./
RUN apt update && pip install --upgrade pip && pip3 install -r requirements.txt

COPY ./src ./

ENTRYPOINT ["uvicorn", "app:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
