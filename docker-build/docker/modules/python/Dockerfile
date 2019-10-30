# runtime envrionment
FROM centos-python

COPY  fate_flow /data/projects/fate/fate_flow
COPY  arch /data/projects/fate/arch
COPY  federatedml /data/projects/fate/federatedml
COPY  eggroll /data/projects/fate/eggroll

WORKDIR /data/projects/fate

ENV PYTHONPATH=/data/projects/fate
CMD while true; do sleep 1; done;

