# Elevation Mapping cupy
Installation steps are as follows 
-dockerfile is updated, but scripting is not done as of now, please ignore bash scripts in the docker folder. 
```
IMAGE_NAME=elev_map_dev:latest

# Build it
docker build \
  -f Dockerfile \
  -t $IMAGE_NAME \
```
