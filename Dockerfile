FROM mrraph/docker-nameko

COPY services/  /etc/supervisor.d/
COPY app/ /usr/src/app/
RUN chmod -R +x /etc/my_runalways /etc/my_runonce
