FROM ubuntu:latest
MAINTAINER Georg von Zengen "oni303@gmail.com"
LABEL com.centurylinklabs.watchtower.enable="false"
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
COPY ./form /form
WORKDIR /form
RUN pip3 install -r requirements.txt
CMD ["./run.sh"]
