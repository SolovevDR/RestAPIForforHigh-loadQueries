FROM postgres:15.10 as base

RUN useradd -ms /bin/bash appuser

WORKDIR /database
COPY database/requirements.txt ./

ENV PIP_BREAK_SYSTEM_PACKAGES=1
RUN apt-get update && apt-get install -y python3.11 python3-pip python3-venv
RUN pip3 install -r requirements.txt

COPY database ./
COPY src/models/models.py ./

RUN chmod +x start_bd.sh && chmod 777 /database

USER postgres

ENTRYPOINT ["/database/start_bd.sh"]
