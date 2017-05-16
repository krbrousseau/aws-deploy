import json
import boto3
import time
import paramiko

config = json.load(open('config.json','r'))

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
	time.sleep(30)
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
    print "connecting to "+hostname
    ssh_client.connect(hostname, username="ubuntu", key_filename=key_path)
    ftp_client = ssh_client.open_sftp()
    # push script file
    setup_script = config['ftp']['setup_script']
    localpath = config['ftp']['script_path']+setup_script
    remotepath = "/home/ubuntu/"+setup_script
    print "uploading "+setup_script
    ftp_client.put(localpath, remotepath)
    ftp_client.close()
    print "executing "+setup_script
    stdin, stdout, stderr = ssh_client.exec_command('chmod +x '+setup_script+'; ./'+setup_script)
    time.sleep(5)
    sout = stdout.readlines()
    print sout
    serr = stderr.readlines()
    print serr
    while len(sout)>0:
      print "waiting for script"
      time.sleep(5)
      sout = stdout.readlines()
      print sout
      serr = stderr.readlines()
      print serr
    stdin, stdout, stderr = ssh_client.exec_command("ps ax -o command | grep -c '^/usr/bin/java.*Elasticsearch'")
    if int(stdout.readlines()[0])==1:
      print "Elasticsearch running"
    else:
      print "setup failed; exiting"
    ssh_client.close()
