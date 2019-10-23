if [ "$1" == "" ]
then
  echo "Need to provide Harbor' address"
  echo "Usage: ./.tag_for_harbor.sh $harbor_address"
  exit 0
fi

images=`docker images | grep ^federatedai | awk '{print $1":"$2}'`
for image in $images; do
  docker tag $image $1/$image
  docker push $1/$image
done

images=`docker images | grep -e mysql -e redis | awk '{print $1":"$2}'`
for image in $images; do
  docker tag $image $1/$image
  docker push $1/$image
done
