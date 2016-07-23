FROM python:2.7

RUN pip install boto3
RUN pip install requests

WORKDIR /lambda2git
