#!/bin/bash
set -e

PREFIX=fatetest
BASE_TAG=0.3-beta
BUILDER_TAG=0.3-beta
TAG=0.3-alpha

current_dir=`pwd`

## User maven to build all jar target
echo "### START BUILDING MODULES JAR FILES ###"
docker build -f ./docker/cluster/builders/maven-builder/Dockerfile -t ${PREFIX}/maven-builder:${BUILDER_TAG} .
# Copy target files from the `fate-builder`

# overwrite the arch and fate-serving dirs
container_id=`docker run -d fate-builder:latest bash -c 'while true; do sleep 1; done'`
docker cp ${container_id}:/data/projects/fate/arch/ ${current_dir}/
docker cp ${container_id}:/data/projects/fate/fate-serving/ ${current_dir}/
docker rm -f ${container_id}
echo "### FINISH BUILDING MODULES JAR FILES ###"

# packaging modules
cd ${current_dir}/cluster-deploy/scripts
bash auto-packaging.sh


# create builder image for storage-service-cxx
# build the storage-service-cxx builder if "buildStorageServiceBuilder" was given
for val in "$@"
do
    if [ "$val" = "buildStorageServiceBuilder" ]; then
	echo "START BUILDING STORAGE-SERVICE BUILDER"
        cd ${current_dir}
        docker build --build-arg PREFIX=${PREFIX} --build-arg BASE_TAG=${BASE_TAG} -f docker/cluster/builders/storage-service-builder/Dockerfile -t ${PREFIX}/storage-service-builder:${BUILDER_TAG} .
	echo "FINISH BUILDING STORAGE-SERVICE BUILDER"
    fi;

    # TODO ADD building of base here
    if [ "$val" = "buildBase" ]; then
	echo "START BUILDING BASE IMAGE"
        cd ${current_dir}
        docker build -f docker/cluster/base/Dockerfile -t ${PREFIX}/base-image:${BASE_TAG} .
	echo "FINISH BUILDING BASE IMAGE"
    fi;
done;

# build modules according to the dir-tree
cd ${current_dir}

for module in "federation" "proxy" "roll" "python" "meta-service" "serving-service"
do

    echo "### START BUILDING ${module^^} ###"
    cp -r ./cluster-deploy/example-dir-tree/${module}/* ./docker/cluster/modules/${module}/
    docker build --build-arg PREFIX=${PREFIX} --build-arg BASE_TAG=${BASE_TAG} -t ${PREFIX}/${module}:${TAG} -f ./docker/cluster/modules/${module}/Dockerfile ./docker/cluster/modules/${module}
    echo "### FINISH BUILDING ${module^^} ###"
    echo ""

done;

## build egg/storage-service (also copy python module to egg)
echo "### START BUILDING EGG ###"
## init submodule lmdb-safe
git submodule update --init ./eggroll/storage/storage-service-cxx/third_party/lmdb-safe
mkdir -p ./docker/cluster/modules/egg/egg-service
cp -r ./cluster-deploy/example-dir-tree/egg/* ./docker/cluster/modules/egg/egg-service/

mkdir -p ./docker/cluster/modules/egg/egg-processor
cp -r ./cluster-deploy/example-dir-tree/python/* ./docker/cluster/modules/egg/egg-processor/

mkdir -p ./docker/cluster/modules/egg/storage-service
cp -r ./cluster-deploy/example-dir-tree/storage-service-cxx/* ./docker/cluster/modules/egg/storage-service/

## copy lmdb-safe submodule
cp -r ./eggroll/storage/storage-service-cxx/third_party/lmdb-safe/* ./docker/cluster/modules/egg/storage-service/third_party/lmdb-safe/

docker build --build-arg PREFIX=${PREFIX} --build-arg BASE_TAG=${BASE_TAG} --build-arg BUILDER_TAG=${BUILDER_TAG} -t ${PREFIX}/egg:${TAG} -f ./docker/cluster/modules/egg/Dockerfile ./docker/cluster/modules/egg
echo "### FINISH BUILDING EGG ###"
echo ""
