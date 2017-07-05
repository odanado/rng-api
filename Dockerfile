FROM python:3

RUN pip install bottle
RUN pip install https://github.com/pklaus/bottlelog/archive/master.zip
RUN pip install paste 

RUN mkdir /root/work
WORKDIR /root/work
