FROM debian:latest

LABEL maintainer="Aymeric Blondel <aymeric.blondel@univ-nantes.fr>"

RUN echo "deb https://snapshot.debian.org/archive/debian/20250101T023759Z/ bookworm main" > /etc/apt/sources.list \
    && apt-get update


RUN apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    libatlas-base-dev \
    && rm -rf /var/lib/apt/lists/*


RUN python3 -m venv /env
ENV PATH="/env/bin:$PATH"
RUN /env/bin/pip install --upgrade pip

COPY requirements.txt /app/requirements.txt
RUN /env/bin/pip install -r /app/requirements.txt

RUN mkdir /DATA
WORKDIR /app
#COPY src/ /app/src/
EXPOSE 8886
