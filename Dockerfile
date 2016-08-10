FROM ipython/scipyserver 

RUN apt-get update
RUN apt-get install -y --fix-missing zip

RUN pip2.7 install boto3
RUN pip2.7 install --upgrade requests
RUN pip2.7 install --upgrade nose
RUN pip2.7 install --upgrade cover


WORKDIR /lambda2git
