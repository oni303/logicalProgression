FROM ubuntu:latest
MAINTAINER Georg von Zengen "oni303@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
COPY . /form
WORKDIR /form
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["app.py"]
