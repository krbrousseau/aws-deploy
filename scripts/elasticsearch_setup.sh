#!/bin/bash
sudo apt-get update
sudo apt-get -y install elasticsearch
sudo systemctl enable elasticsearch.service
sudo sed -i 's/#START_DAEMON/START_DAEMON/' /etc/default/elasticsearch
sudo systemctl restart elasticsearch
systemctl status elasticsearch
