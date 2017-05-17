import json
import boto3
import time
import paramiko

config = json.load(open('configs/config.json','r'))

session = boto3.session.Session(
  aws_access_key_id=config['session']['aws_access_key_id'],
  aws_secret_access_key=config['session']['aws_secret_access_key'],
  region_name=config['session']['region_name']
)

ec2 = session.resource("ec2")

deployed_instances = []
print "deploying instances"
for instance in config['instances']:
  instances = ec2.create_instances(
    ImageId=instance['ImageId'],
    MinCount=instance['MinCount'],
    MaxCount=instance['MaxCount'],
    KeyName=instance['KeyName'],
    SecurityGroups=instance['SecurityGroups'],
    InstanceType=instance['InstanceType']
  )
  print instances
  deployed_instances.append(instances)

time.sleep(90)
print "continuing setup"
for instances in deployed_instances:
  for instance in instances:
    instance = ec2.Instance(instance.instance_id)
    hostname = instance.public_ip_address
    key_name = instance.key_name
    if hostname == None or key_name == None:
      print "waiting for instance"
      i = 0
      while (hostname == None or key_name == None) and i<=3:
	time.sleep(60)
	i += 1
	instance = ec2.Instance(instance.instance_id)
	hostname = instance.public_ip_address
	key_name = instance.key_name
      if hostname == None or key_name == None:
	exit()
    key_path = config['ssh']['key_path']+key_name+'.pem'
    #print "ubuntu@"+str(hostname)+" "+str(key_path)
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print "connecting to "+instance.instance_id+" at "+hostname
    ssh_client.connect(hostname, username="ubuntu", key_filename=key_path)
    ftp_client = ssh_client.open_sftp()
    # push script file
    setup_script = config['ftp']['setup_script']
    setup_script_path = config['ftp']['script_path']+setup_script
    config_path = config['ftp']['config_path']
    print "uploading "+setup_script
    ftp_client.put(setup_script_path, "/home/ubuntu/"+setup_script)
    time.sleep(5)
    for config_upload in config['ftp']['configs']:
      print "uploading "+config_upload
      ftp_client.put(config_path+config_upload, "/home/ubuntu/"+config_upload)
      time.sleep(5)
    ftp_client.close()
    print "waiting for instance"
    time.sleep(60)
    print "executing "+setup_script
    stdin, stdout, stderr = ssh_client.exec_command('chmod +x '+setup_script+'; ./'+setup_script)
    script_output = ""
    script_errors = ""
    print "waiting for script"
    stdout_buffer = stdout.readlines()
    stderr_buffer = stderr.readlines()
    while len(stdout_buffer)>0 and len(stderr_buffer)>0:
      print "waiting for script"
      script_output+="".join(stdout_buffer)
      script_errors+="".join(stderr_buffer)
      stdout_buffer = stdout.readlines()
      stderr_buffer = stderr.readlines()
    print script_output
    print script_errors
    for user in config['user_auth']:
      username = user['username']
      password = user['password']
      stdin, stdout, stderr = ssh_client.exec_command("sudo htpasswd -c -b /etc/nginx/.htpasswd "+username+" "+password)
    stdin, stdout, stderr = ssh_client.exec_command("ps ax -o command | grep -c '^/usr/bin/java.*Elasticsearch'")
    if int(stdout.readlines()[0])==1:
      print "elasticsearch running"
    else:
      print "elasticsearch setup failed; exiting"
      ssh_client.close()
      exit()
    stdin, stdout, stderr = ssh_client.exec_command("ps ax -o command | grep -c '^nginx'")
    if int(stdout.readlines()[0])>=1:
      print "nginx running"
    else:
      print "nginx setup failed; exiting"
      ssh_client.close()
      exit()
    ssh_client.close()
