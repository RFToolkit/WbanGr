FROM ubuntu:22.04

ENV WORKSPACE /opt/gr-wban
ENV TZ="Europe/Paris"
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
COPY ./scripts/install_lib.sh /usr/bin/install_lib.sh
RUN mkdir -p /root/.grc_gnuradio
COPY .grc_gnuradio /root/.grc_gnuradio
RUN chmod +x /usr/bin/install_lib.sh

RUN apt-get update && \
    apt-get install -y software-properties-common git cmake g++ libboost-all-dev libgmp-dev swig python3-numpy \
    python3-mako python3-sphinx python3-lxml doxygen libfftw3-dev \
    libsdl1.2-dev libgsl-dev libqwt-qt5-dev libqt5opengl5-dev python3-pyqt5 \
    liblog4cpp5-dev libzmq3-dev python3-yaml python3-click python3-click-plugins \
    python3-zmq python3-scipy python3-gi python3-gi-cairo gir1.2-gtk-3.0 qt5-gtk-platformtheme \
    libcodec2-dev libgsm1-dev pybind11-dev python3-matplotlib libsndfile1-dev \
    libairspy-dev librtlsdr-dev libhackrf-dev libairspyhf-dev libbladerf-dev libcanberra-gtk-* libgtk-3-* libgtk2.0*  \
    python3-pip libsoapysdr-dev soapysdr-tools xterm libuhd-dev libfreesrp-dev liborc-0.4-dev && \
    add-apt-repository ppa:gnuradio/gnuradio-releases-3.9 &&\
    rm -rf /var/lib/apt/lists/*

RUN apt update &&\
    apt install -y gnuradio python3-packaging &&\
        install_lib.sh

RUN DEBIAN_FRONTEND=noninteractive apt install netcat vim xxd tshark -y

COPY ./scripts/requirements.txt /opt/gr-wban/requirements.txt
RUN pip install -r /opt/gr-wban/requirements.txt

COPY ./scripts/entrypoint.sh /usr/bin/entrypoint.sh
RUN chmod +x /usr/bin/entrypoint.sh

RUN echo "alias grep='grep --color=auto'" >> ~/.bashrc && \
    echo 'set -g default-terminal "screen-256color"' >> ~/.tmux.conf

RUN pip3 install Flask[async] codext

#ENV CODE_VERSION 1.74.2.22355
#ENV CODE_LINK https://github.com/VSCodium/vscodium/releases/download/${CODE_VERSION}/codium_${CODE_VERSION}_amd64.deb
#RUN cd tmp &&\
#    curl -L ${CODE_LINK} -o /tmp/code.deb &&\
#    apt install /tmp/code.deb &&\
#    rm -rvf /tmp/code.deb &&\
#    echo "codium --no-sandbox --user-data-dir=/tmp/code $@" > /usr/bin/code2

COPY ./grc/precompiled /opt/gr-wban/precompiled
RUN mkdir -p ${WORKSPACE}
WORKDIR ${WORKSPACE}