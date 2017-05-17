# aws-elasticsearch-deploy
Deploys an AWS instance and configures Elasticsearch

# Goal
Deploy an AWS instance. 
Install, configure, and secure Elasticsearch.

# Requirements
Local environment with : 
```
python v2.7.x
 - boto3
 - cryptography
 - paramiko
```

A base AWS ami with :
```
oracle java8
```

# Setup
Copy the existing config template as `config.json` and modify it to include the necessary AWS keys and settings for the instance being deployed.

# Deploying the Instance
With the config file set up, just run : 
```
$ python deploy.py
```
The instance will be deployed to AWS based on the settings specified in `config.json`. 
A setup script and multiple config files are uploaded to the instance.
The setup script is executed to install and configure elasticsearch.

# Resources
 - lots of Googling
 - Boto 3 Docs
 - Elasticsearch docs and discussion posts
 - NGINX docs
 - stackoverflow
 - DigitalOcean Tutorials
