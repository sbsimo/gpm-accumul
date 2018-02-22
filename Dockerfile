FROM ubuntu:xenial

RUN apt update
RUN apt install -y software-properties-common python-software-properties

RUN add-apt-repository -y ppa:ubuntugis/ppa
RUN apt update
RUN apt install -y gdal-bin python3-gdal libgdal-dev

RUN apt install -y python3-pip
RUN pip3 install h5py
RUN pip3 install Django==2

VOLUME /usr/src/gpm-accumul

WORKDIR /usr/src

EXPOSE 8000

CMD bash