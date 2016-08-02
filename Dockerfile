FROM ipython/scipyserver 

RUN apt-get update
RUN apt-get install -y --fix-missing zip

RUN pip2.7 install boto3
RUN pip2.7 install requests


WORKDIR /lambda2git
