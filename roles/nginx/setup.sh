#!/bin/bash
echo INSTALLING NGINX
sudo apt-get -y install nginx
[ $(systemctl status nginx | grep -c "active (running)") -le 0 ] && exit 1
echo NGINX RUNNING
