FROM python:3.9-slim-bullseye

WORKDIR /app/

RUN apt-get -y upgrade
RUN apt-get -y update

RUN python3 -m pip install -U pip

COPY src/requirements.txt src/requirements.txt

RUN pip3 install -Ur src/requirements.txt

COPY . .

WORKDIR /app/src

EXPOSE 8081/tcp 8082/tcp

CMD [ "python", "main.py" ]