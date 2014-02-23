FROM akerl/arch
MAINTAINER akerl <me@lesaker.org>
RUN pacman -Syu --needed --noconfirm base-devel bc python-pip
RUN pip install roller
RUN git clone git://github.com/akerl/kernels /opt/kernels
CMD ['/bin/bash']
