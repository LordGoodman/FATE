ARG PREFIX=prefix
ARG TAG=tag

FROM ${PREFIX}/base-image:${TAG}

COPY .  /data/projects/FATE/

ENV dir=/data/projects/FATE/eggroll/storage/storage-service-cxx

ENV CPLUS_INCLUDE_PATH=/data/projects/common/miniconda3/include/python3.6m/

# initial python virtual envrionment
RUN touch /var/lib/rpm/*  && yum install -y which git && \
    source /data/projects/fate/venv/bin/activate

# update third party
RUN cd /data/projects/FATE && \
    git submodule update --init --recursive

# install boostrap
RUN cd $dir/third_party/boost && \
    sed -ie "14s#PREFIX=.*#PREFIX=$dir/third_party#g" ./bootstrap.sh && \
    ./bootstrap.sh && \
    ./b2 install

# install google log
RUN cd $dir/third_party/glog && \
    ./autogen.sh && \
    ./configure  --prefix=$dir/third_party && \
    make && make install

# install grpc and proto
RUN cd $dir/third_party/grpc && \
    make && \
    mkdir -p /tmp/third_party && \
    make install prefix=/tmp/third_party && \
    cd third_party/protobuf && \
    ./autogen.sh && \
    ./configure --prefix=/tmp/third_party && \
    make && \
    make check && \
    make install && \
    rsync -a /tmp/third_party/* $dir/third_party/

# install dynamic libraries lmdb
RUN cd $dir/third_party/lmdb/libraries/liblmdb && \
    make && \
    cp lmdb.h $dir/third_party/include && \
    cp liblmdb.so $dir/third_party/lib

# copy cpp dependencies to /data/projects/fate/third_party
RUN mkdir -p /data/projects/fate/third_party && \
    mv $dir/third_party/bin  $dir/third_party/lib $dir/third_party/include $dir/third_party/share /data/projects/fate/third_party

