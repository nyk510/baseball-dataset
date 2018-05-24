FROM ubuntu:16.04
LABEL maintainer="nykergoto@gmail.com"

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN apt-get update --fix-missing && \
    apt-get install -y wget bzip2 ca-certificates curl git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir /npb



# userの追加
RUN groupadd -g 1000 developer

# user:penguin, password:highway
RUN useradd -g developer -G sudo -m -s /bin/bash penguin
RUN echo "penguin:highway" | chpasswd

# 以下は penguin での操作
USER penguin
WORKDIR /home/penguin/

# pyenv
RUN git clone git://github.com/yyuu/pyenv.git .pyenv
ENV HOME /home/penguin
ENV PYENV_ROOT ${HOME}/.pyenv
ENV PATH ${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${PATH}
ENV CONDA_VERSION miniconda3-4.3.30

RUN pyenv install ${CONDA_VERSION}
RUN pyenv rehash
RUN pyenv global ${CONDA_VERSION}

WORKDIR /npb

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

# EXPOSE 8888
# CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888"]
