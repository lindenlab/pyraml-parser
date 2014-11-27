FROM lindenlab.com/debian:jessie

RUN apt-get update && apt-get install -y python-pip
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app
RUN python setup.py install
ENTRYPOINT ["/usr/src/app/parse-raml.py"]
CMD ["/proc/self/fd/0"]
