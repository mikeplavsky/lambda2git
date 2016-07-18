FROM python:2.7
RUN pip install boto3

WORKDIR /lambda2git
