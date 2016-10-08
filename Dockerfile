FROM ubuntu:14.04
MAINTAINER Taras Slyvka

# Base setting 
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
RUN apt-get update && apt-get install -y python-pip python-dev libpq-dev && apt-get clean

# Install apt-get*
RUN sudo apt-get install -y python-croniter

# Install pip requirements
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy project in container
WORKDIR /project
ADD . /project

