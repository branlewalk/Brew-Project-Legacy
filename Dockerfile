FROM ubuntu:16.04

MAINTAINER Your Name "youremail@domain.tld"

RUN apt-get update
RUN apt-get install -y python-pip
RUN apt-get install -y python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#COPY . /app

#ENTRYPOINT [ "python" ]

#CMD [ "server.py" ]
