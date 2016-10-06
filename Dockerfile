FROM python:3.6-slim

MAINTAINER MrRaph_
COPY scripts/etc/ /etc/
COPY scripts/tools/launch.sh /launch.sh

RUN apt-get update && apt-get -y upgrade && \
    apt-get install -y --no-install-recommends ca-certificates \
     rsyslog supervisor build-essential libffi-dev libssl-dev \
     python-dev python3-pip wget python3-openssl openssl && \
     mkdir /etc/my_runonce /etc/my_runalways /etc/container_environment && \
     touch /var/log/startup.log && chmod 666 /var/log/startup.log && \
     rm -rf rm -rf /var/lib/apt/lists/* && \
     chmod +x /launch.sh

COPY requirements.txt /tmp/requirements.txt

RUN pip install --upgrade pip \
  && pip install nameko supervisor-stdout dumb-init \
  && pip install -r /tmp/requirements.txt \
  && apt-get purge -y build-essential

COPY scripts/services/  /etc/supervisor.d/
COPY app/ /usr/src/app/
COPY scripts/my_runonce/ /etc/my_runonce/

# Set environment variables.
ENV HOME /root

# Define default command.
ENTRYPOINT ["/usr/local/bin/dumb-init", "--"]
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
