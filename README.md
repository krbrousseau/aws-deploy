## aws-elasticsearch-deploy
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
Copy `configs/template_config.json` as `configs/config.json` and modify it to include the necessary AWS keys and settings for the instance being deployed, the path to your `.ssh` directory, the paths to this repo's `scripts` and `configs` directories, and user/password information for the server.

# Deploying the Instance
With the config file set up run : 
```
$ python deploy.py
```
The instance will be deployed to AWS based on the settings specified in `config.json`. 
A setup script and multiple config files will be uploaded to the instance.
The setup script is executed to install and configure elasticsearch.
On success, the final line output will have the IP address of the instance.

# Resources
 - lots of Googling
 - Boto 3 Docs
 - Elasticsearch docs and discussion posts
 - NGINX docs
 - stackoverflow
 - DigitalOcean Tutorials

# Feedback and Questions
Feedback can be found [here](feedback.md).
Questions can be found [here](questions.md).
