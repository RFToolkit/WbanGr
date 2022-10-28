FROM ubuntu

ENV WORKSPACE /opt/gr-wban
ENV TZ="Europe/Paris"
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
COPY ./scripts/install_lib.sh /usr/bin/install_lib.sh
RUN chmod +x /usr/bin/install_lib.sh

RUN apt-get update && \
    apt-get install -y software-properties-common git cmake g++ libboost-all-dev libgmp-dev swig python3-numpy \
    python3-mako python3-sphinx python3-lxml doxygen libfftw3-dev \
    libsdl1.2-dev libgsl-dev libqwt-qt5-dev libqt5opengl5-dev python3-pyqt5 \
    liblog4cpp5-dev libzmq3-dev python3-yaml python3-click python3-click-plugins \
    python3-zmq python3-scipy python3-gi python3-gi-cairo gir1.2-gtk-3.0 \
    libcodec2-dev libgsm1-dev pybind11-dev python3-matplotlib libsndfile1-dev \
    python3-pip libsoapysdr-dev soapysdr-tools && \
    rm -rf /var/lib/apt/lists/*

RUN add-apt-repository ppa:gnuradio/gnuradio-releases-3.9 &&\
    apt update &&\
    apt install -y gnuradio python3-packaging &&\
        install_lib.sh

RUN mkdir -p ${WORKSPACE}
WORKDIR ${WORKSPACE}
