#!/bin/bash
sudo apt-get update
echo INSTALLING ELASTICSEARCH
sudo apt-get -y install elasticsearch
sudo systemctl enable elasticsearch.service
sudo sed -i 's/#START_DAEMON/START_DAEMON/' /etc/default/elasticsearch
sudo systemctl restart elasticsearch
[ $(systemctl status elasticsearch | grep -c "active (running)") -le 0 ] && exit 1
echo ELASTICSEARCH RUNNING

echo INSTALLING NGINX
sudo apt-get -y install nginx
[ $(systemctl status nginx | grep -c "active (running)") -le 0 ] && exit 1
echo NGINX RUNNING

echo CONFIGURING NGINX
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt -config openssl-prompt.conf
sudo openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048
sudo cp self-signed.conf /etc/nginx/snippets/self-signed.conf
sudo cp ssl-params.conf /etc/nginx/snippets/ssl-params.conf
sudo mv /etc/nginx/sites-available/default /etc/nginx/sites-available/_default
sudo cp nginx-elasticsearch-proxy.conf /etc/nginx/sites-available/default
sudo systemctl restart nginx
[ $(systemctl status nginx | grep -c "active (running)") -le 0 ] && exit 1
echo NGINX CONFIGURED

echo INSTALLING APACHE2 UTILS
sudo apt-get -y install apache2-utils
echo READY TO SETUP USER AUTHORIZATION
