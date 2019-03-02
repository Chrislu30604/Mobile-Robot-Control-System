# This is an auto generated Dockerfile for ros:ros-core
# generated from docker_images/create_ros_core_image.Dockerfile.em
FROM ubuntu:bionic
MAINTAINER chrislu <chrislu30604@gmail.com>

# setup timezone
RUN echo 'Etc/UTC' > /etc/timezone && \
    ln -s /usr/share/zoneinfo/Etc/UTC /etc/localtime && \
    apt-get update && apt-get install -q -y tzdata && rm -rf /var/lib/apt/lists/*

# install packages
RUN apt-get update && apt-get install -q -y \
    dirmngr \
    gnupg2 \
    lsb-release \
    && rm -rf /var/lib/apt/lists/*

# setup keys
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 421C365BD9FF1F717815A3895523BAEEB01FA116

# setup sources.list
RUN echo "deb http://packages.ros.org/ros/ubuntu `lsb_release -sc` main" > /etc/apt/sources.list.d/ros-latest.list

# install bootstrap tools
RUN apt-get update && apt-get install --no-install-recommends -y \
    python-rosdep \
    python-rosinstall \
    python-vcstools \
    && rm -rf /var/lib/apt/lists/*

# setup environment
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# bootstrap rosdep
RUN rosdep init \
    && rosdep update

# install ros packages
ENV ROS_DISTRO melodic
RUN apt-get update && apt-get install -y \
    ros-melodic-ros-core=1.4.1-0* \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y  netcat	

RUN mkdir -p /robot/src
RUN /bin/bash -c '. /opt/ros/melodic/setup.bash; catkin_init_workspace /robot/src'
RUN /bin/bash -c '. /opt/ros/melodic/setup.bash; cd /robot/src; \
	catkin_create_pkg roboticlab std_msgs rospy roscpp geometry_msgs sensor_msgs'
RUN /bin/bash -c '. /opt/ros/melodic/setup.bash; cd /robot; catkin_make'
RUN echo "source /robot/devel/setup.bash" >> ~/.bashrc

WORKDIR /robot

VOLUME /home/chrislu/robotLabatory/Mobile-Robot-Control-System/controls/src/ /robot/src/roboticlab/launch
VOLUME /home/chrislu/robotLabatory/Mobile-Robot-Control-System/controls/launch/ /robot/src/roboticlab/src

#EXPOSE 10024 10025 10026
