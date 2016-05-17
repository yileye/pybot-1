FROM python:2.7
RUN apt-get update && apt-get -y install netcat
RUN pip install flask pika pymongo requests
COPY entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh


