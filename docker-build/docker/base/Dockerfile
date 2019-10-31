FROM centos:centos7.2.1511

COPY pip-packages-fate-1.1.tar.gz /data/pips/

RUN yum install -y \
		gcc gcc-c++ make openssl-devel \ 
		supervisor gmp-devel mpfr-devel libmpc-devel \
		libaio numactl autoconf automake libtool libffi-devel \
		snappy snappy-devel zlib zlib-devel bzip2 bzip2-devel lz4-devel libasan lsof \
       	java-1.8.0-openjdk \
       	java-1.8.0-openjdk-devel \
       	bzip2 && \
    yum install -y https://centos7.iuscommunity.org/ius-release.rpm && \
    yum update -y && \
	yum install -y python36u python36u-libs python36u-devel python36u-pip && \
    cd /data/pips && tar -xf pip-packages-fate-1.1.tar.gz && cd pip-packages-fate-1.1 && \
	rm tensorboard-1.14.0-py3-none-any.whl && rm setuptools-41.4.0-py2.py3-none-any.whl && \
    pip3 install ./* && \
    rm -f /bin/python && ln -s /bin/python3 /bin/python
