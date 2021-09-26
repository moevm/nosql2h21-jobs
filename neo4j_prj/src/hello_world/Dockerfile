FROM python:3.6-buster
ENV PYTHONUNBUFFERED 1

WORKDIR /docker/
COPY ./requirements.txt requirements.txt
RUN pip install -r /docker/requirements.txt

WORKDIR neo4j_prj/
COPY ./src src

WORKDIR src/hello_world/

CMD ["sh", "-c", "python main.py"]

