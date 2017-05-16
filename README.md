# aws-elasticsearch-deploy
Deploys an AWS instance and configures Elasticsearch

# Goal
Deploy an AWS instance. 
Install, configure, and secure Elasticsearch.

# Requirements
```
python v2.7.x
 - boto3
 - cryptography
 - paramiko
```

# Setup
Copy the existing config template as `config.json` and modify it to include the necessary AWS keys and settings for the instance being deployed.

# Deploying the Instance
With the config file set up, just run : 
```
$ python deploy_elasticsearch.py
```
The instance will be deployed to AWS based on the settings specified in `config.json`. A setup script is uploaded and executed to install and setup elasticsearch.
