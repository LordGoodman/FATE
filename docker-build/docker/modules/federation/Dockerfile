
FROM nvidia/cuda:10.1-devel-centos7

COPY fate-federation-1.1.tar.gz /data/projects/fate/federation/fate-federation-1.1.tar.gz

RUN rpm --rebuilddb && \
    yum install -y which java-1.8.0-openjdk java-1.8.0-openjdk-devel && \
    cd /data/projects/fate/federation/ && \
    tar -xzf fate-federation-1.1.tar.gz && \
    rm fate-federation-1.1.tar.gz && \
    ln -s fate-federation-1.1.jar fate-federation.jar
EXPOSE 9394

CMD cd /data/projects/fate/federation && \
    java -cp "conf/:lib/*:fate-federation.jar" com.webank.ai.fate.driver.Federation -c conf/federation.properties

