# runtime envrionment
FROM centos-base

COPY  fate_flow /data/projects/fate/fate_flow
COPY  arch /data/projects/fate/arch
COPY  federatedml /data/projects/fate/federatedml
COPY  eggroll-api-1.1.tar.gz /data/projects/fate/

RUN cd /data/projects/fate/ && \
    mkdir -p eggroll/api && tar -C eggroll/api -xvf eggroll-api-1.1.tar.gz && \
    rm eggroll-api-1.1.tar.gz

WORKDIR /data/projects/fate

ENV PYTHONPATH=/data/projects/fate
CMD cd /data/projects/fate/fate_flow && python3 fate_flow_server.py
