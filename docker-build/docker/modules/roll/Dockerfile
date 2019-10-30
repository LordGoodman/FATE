FROM mcr.microsoft.com/java/jre:8u192-zulu-alpine

COPY cluster-deploy/packages/eggroll-roll-1.1.tar.gz /data/projects/fate/roll/eggroll-roll-1.1.tar.gz

RUN cd /data/projects/fate/roll/ && \
    tar -xzf eggroll-roll-1.1.tar.gz && \
    rm eggroll-roll-1.1.tar.gz && \
    ln -s eggroll-roll-1.1.jar fate-roll.jar

WORKDIR /data/projects/fate

CMD cd roll && \
    java -cp "conf/:lib/*:fate-roll.jar" com.webank.ai.fate.eggroll.Roll -c conf/roll.properties

