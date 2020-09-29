#! /bin/bash

# update repos:
apt-get update

# install utilities
apt-get install -y git \
                   build-essential gcc-4.4\
                   python3-pip \
                   wget \
                   vim

# link gcc version:
# ln /usr/bin/gcc-4.4 /usr/bin/gcc
# export CC=/usr/bin/gcc-4.4

# upgrade pip:
python3 -m pip install --upgrade pip

# since it's docker:
apt-get install file \
                lsof

# install dependencies:
apt-get install bzip2 libbz2-dev \
                libcairo2-dev \
                libjpeg-dev \
                libpng12-dev \
                libnetpbm10-dev libnetpbm10 netpbm \
                zlib1g-dev \
                wcslib-dev wcslib-tools \
                python3-dev python3-pil python3-numpy python3-scipy python3-matplotlib python3-tk python3-astropy \
                swig

# install cfitsio
apt-get install libcfitsio-dev libcfitsio-bin
