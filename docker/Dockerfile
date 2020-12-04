FROM conda/miniconda3-centos7

ENV RUN_DIR /runners
ENV TERM=xterm
ENV DOCKER_CONTAINER Yes

# Create directory structure.
RUN mkdir -p ${RUN_DIR}
RUN mkdir -p ${RUN_DIR}

RUN yum install git -y

# Copy run files.
ADD environment_droplet.yml ${RUN_DIR}
ADD token.enc /root
ADD startup.sh ${RUN_DIR}
RUN chmod +x ${RUN_DIR}/startup.sh

WORKDIR ${RUN_DIR}

RUN git clone https://github.com/paulscherrerinstitute/gitutils.git 

ENTRYPOINT ["/bin/bash"]
