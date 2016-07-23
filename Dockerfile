FROM python:2.7

RUN apt-get update
RUN apt-get install -y --fix-missing zip

RUN pip install boto3
RUN pip install requests


WORKDIR /lambda2git
