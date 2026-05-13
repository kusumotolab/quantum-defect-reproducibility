FROM python:3.10.20

RUN apt-get update \
    && apt-get install -y vim build-essential tree procps parallel \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -g 1000 user \
    && useradd -m -u 1000 -g 1000 -s /bin/bash user

WORKDIR /src

COPY requirements.txt /src/requirements.txt
COPY bash_setting /home/user/.bashrc

RUN pip install --upgrade pip
RUN pip install -r /src/requirements.txt

ENV HOME=/home/user
ENV TZ=Asia/Tokyo

RUN chown -R 1000:1000 /home/user /src

USER user