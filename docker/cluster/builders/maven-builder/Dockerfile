FROM maven:3.6-jdk-8

# TODO: should remove this file and build jar in dockerfile of submodules

# build arch
COPY arch /data/projects/fate/arch
RUN cd /data/projects/fate/arch && mvn clean package -DskipTests

# build fate-serving
COPY fate-serving /data/projects/fate/fate-serving
RUN cd /data/projects/fate/fate-serving && mvn clean package -DskipTests
