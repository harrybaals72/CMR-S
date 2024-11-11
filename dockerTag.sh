#!/bin/bash

# Set the name of the image and the registry
username="harrybaals72"
image_name="cmr-s"

curr=$(cat docker_version)

# Get the current version number from the registry
# current_version=$(docker pull $registry/$image_name | grep -o "[0-9]\+$")
# current_version=$(docker pull $image_name | grep -o "[0-9]\+$")

# Increment the version number
new=$((curr+1))

echo "cur: $curr, new: $new"

# Build the new image with the new version number
docker build -t $image_name:$new .

# Tag the new image with the registry name
docker tag $image_name:$new ${username}/${image_name}:$new

# Push the new image to the registry
docker push ${username}/${image_name}:$new

# Also change latest tag to this version
docker tag $image_name:$new ${username}/${image_name}:latest
docker push ${username}/${image_name}:latest

echo "$new" > docker_version
