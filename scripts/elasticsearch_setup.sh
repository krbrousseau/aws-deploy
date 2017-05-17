#!/bin/bash
sudo apt-get update
sudo apt-get -y install elasticsearch
sudo systemctl enable elasticsearch.service
sudo sed -i 's/#START_DAEMON/START_DAEMON/' /etc/default/elasticsearch
sudo systemctl restart elasticsearch
systemctl status elasticsearch

sudo apt-get -y install nginx
systemctl status nginx

sudo apt-get -y install apache2-utils
sudo mv /etc/nginx/sites-available/default /etc/nginx/sites-available/_default
sudo cp nginx-elasticsearch-proxy.conf /etc/nginx/sites-available/default
sudo systemctl restart nginx
