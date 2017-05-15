import json
import boto3
import time

config = json.load(open('config.json','r'))

session = boto3.session.Session(
  aws_access_key_id=config['session']['aws_access_key_id'],
  aws_secret_access_key=config['session']['aws_secret_access_key'],
  region_name=config['session']['region_name']
)

ec2 = session.resource("ec2")

deployed_instances = []
for instance in config['instances']:
  deployed_instances += ec2.create_instances(
    ImageId=instance['ImageId'],
    MinCount=instance['MinCount'],
    MaxCount=instance['MaxCount'],
    KeyName=instance['KeyName'],
    SecurityGroups=instance['SecurityGroups'],
    InstanceType=instance['InstanceType']
  )

for instance in deployed_instances:
  print instance
