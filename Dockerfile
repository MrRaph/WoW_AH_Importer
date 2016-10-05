FROM python:3.5-slim

MAINTAINER MrRaph_
COPY scripts/etc/ /etc/
COPY scripts/my_init /
COPY scripts/my_service /

RUN apt-get update && apt-get -y upgrade && \
    apt-get install -y --no-install-recommends ca-certificates \
     rsyslog supervisor build-essential libffi-dev libssl-dev \
     python-dev python3-pip wget python3-openssl openssl && \
    chmod +x /my_*; return 0 && \
    mkdir /etc/my_runonce /etc/my_runalways /etc/container_environment /etc/workaround-docker-2267 /var/log/supervisor && \
    touch /var/log/startup.log && chmod 666 /var/log/startup.log && \
    rm -rf rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt

RUN pip install --upgrade pip \
  && pip install nameko supervisor-stdout \
  && pip install -r /tmp/requirements.txt \
  && apt-get purge -y build-essential

COPY scripts/services/  /etc/supervisor.d/
COPY app/ /usr/src/app/
COPY scripts/my_runonce/ /etc/my_runonce/
RUN chmod -R +x /etc/my_runonce && mkdir -p /etc/workaround-docker-2267

# Set environment variables.
ENV HOME /root

# Define default command.
#CMD ["/my_init"]
CMD ["/usr/bin/supervisord"]
