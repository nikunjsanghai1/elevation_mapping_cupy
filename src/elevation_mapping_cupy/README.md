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
Here, set the mount workspace as local directory and image name=docker image
```
docker run -it --rm \
  --gpus all \
  --device /dev/dri \
  --group-add $(getent group video | cut -d: -f3) \
  --name elev_map_dev \
  -e NVIDIA_VISIBLE_DEVICES=all \
  -e NVIDIA_DRIVER_CAPABILITIES=graphics,compute,utility \
  -e __GLX_VENDOR_LIBRARY_NAME=nvidia \
  -e DISPLAY=$DISPLAY \
  -e XAUTHORITY=/root/.Xauthority \
  -e QT_X11_NO_MITSHM=1 \
  -v $HOME/.Xauthority:/root/.Xauthority:ro \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v $WORKSPACE:/root/ros2_ws \
  $IMAGE bash

```
clone the ros2_py branch of the elevation_mapping_cupy, after making a workspace in ros2 
```
git clone --branch ros2_py https://github.com/leggedrobotics/elevation_mapping_cupy.git
```
download the rosdeps and dependencies, it will download a lot of bloat, that will be removed later, only build elevation_mapping_cupy and elevation_mapping_msgs
```
colcon build --symlink-install --packages-select elevation_mapping_cupy elevation_mapping_msgs
```
**The launch file that works in elevation_mapping.launch.py** 
-in case any changes need to be made the parameters of the algorithm are mentioned under
```
src/elevation_mapping_cupy/elevation_mapping_cupy/config/core/core_param.yaml, 
similarly robot config is mentioned in menzi/base.yaml under /config/setups 
```

### Troubleshooting
There can be errors associated with some dependency that is needed after docker image is built and repo is cloned because some bloat has not been severed. For now there is some bloat that is being installed, some repos will cause conflicts. **Code will not compile if ros-numpy is below 0.5**, to address that install ros-numpy, it will install numpy 1.24 , then force numpy 1.23.5 installation.


