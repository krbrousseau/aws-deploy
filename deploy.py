import sys
import os
import time
import json
import boto3
import paramiko


# load config
deploy_config = json.load(open('config.json','r'))

# set up AWS session credentials
aws_session = boto3.session.Session(
  aws_access_key_id=deploy_config['aws_session']['aws_access_key_id'],
  aws_secret_access_key=deploy_config['aws_session']['aws_secret_access_key'],
  region_name=deploy_config['aws_session']['region_name']
)

# load globals
ssh_key_path=deploy_config['ssh_key_path']
roles_location=deploy_config['roles_location']

# initialize AWS resources
ec2 = aws_session.resource("ec2")

def load_role_config(role):
  return json.load(open(roles_location+role+"/config.json",'r'))

def launch_instances(role):
  role_config = load_role_config(role)
  #print role_config
  
  print "launching "+role+" instances"
  launched_instances = ec2.create_instances(
    ImageId=role_config['instance']['ImageId'],
    MinCount=role_config['instance']['MinCount'],
    MaxCount=role_config['instance']['MaxCount'],
    KeyName=role_config['instance']['KeyName'],
    SecurityGroups=role_config['instance']['SecurityGroups'],
    InstanceType=role_config['instance']['InstanceType']
  )
  return launched_instances

def get_instance_ssh_info(instance):
  instance = ec2.Instance(instance.instance_id)
  hostname = instance.public_ip_address
  key_name = instance.key_name
  if hostname == None or key_name == None:
    print "waiting for instance"
    i = 0
    while (hostname == None or key_name == None) and i<=10:
      i += 1
      time.sleep(i)
      instance = ec2.Instance(instance.instance_id)
      hostname = instance.public_ip_address
      key_name = instance.key_name
    if hostname == None or key_name == None:
      exit()
  return hostname, key_name
  
def bootstrap_instance(instance, role, added_roles=[]):
  role_config = load_role_config(role)
  for requirement in role_config['requirements']:
    if requirement not in added_roles:
      added_roles += bootstrap_instance(instance, requirement, added_roles+role_config['requirements'])
      #added_roles += bootstrap_instance(instance, requirement, added_roles+[requirement])
  print "bootstrapping "+role

  # add inherited security groups
  security_groups = [sg['GroupName'] for sg in instance.security_groups]
  inherited_security_groups = role_config['instance']['SecurityGroups']
  for inherited_sg in inherited_security_groups:
    if inherited_sg not in security_groups:
      security_groups.append(inherited_sg)
  security_group_ids = [sg.id for sg in ec2.security_groups.filter(GroupNames=security_groups)]
  instance.modify_attribute(Groups=security_group_ids)

  # open ssh/ftp connections
  hostname = instance.public_ip_address
  key_name = instance.key_name
  if hostname == None or key_name == None:
    hostname, key_name = get_instance_ssh_info(instance)
  key_path = ssh_key_path+key_name+'.pem'
  ssh_client = paramiko.SSHClient()
  ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  print "connecting to "+instance.instance_id+" at "+hostname
  ssh_client.connect(hostname, username="ubuntu", key_filename=key_path)
  ftp_client = ssh_client.open_sftp()

  # push config files
  for config_upload in role_config['configs']:
    print "uploading "+config_upload
    ftp_client.put(roles_location+role+"/"+config_upload, "/home/ubuntu/"+config_upload)

  # push setup script
  setup_script_path = roles_location+role+"/setup.sh" 
  print "uploading setup.sh"
  ftp_client.put(setup_script_path, "/home/ubuntu/setup.sh")
  ftp_client.close()

  # execute setup script and collect output
  print "executing setup.sh"
  if not os.path.exists("logs"):
    os.makedirs("logs")
  stdout_file = open("logs/"+instance.instance_id+"_"+role+"_setup.out",'w')
  stderr_file = open("logs/"+instance.instance_id+"_"+role+"_setup.err",'w')
  stdin, stdout, stderr = ssh_client.exec_command('chmod +x setup.sh; ./setup.sh')
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
  #print script_output
  stdout_file.write(script_output.encode('utf-8'))
  #print script_errors
  stderr_file.write(script_errors.encode('utf-8'))

  # set up users
  for user in role_config['user_auth']:
    username = user['username']
    password = user['password']
    stdin, stdout, stderr = ssh_client.exec_command("sudo htpasswd -c -b /etc/nginx/.htpasswd "+username+" "+password)
    stdout_file.write("".join(stdout.readlines()).encode('utf-8'))
    stderr_file.write("".join(stderr.readlines()).encode('utf-8'))

  stdout_file.close()
  stderr_file.close()
  ssh_client.close()
  
  print "bootstrapping "+role+" completed"
  return role
  #return added_roles

# for testing bootstrap recursion ordering
def bootstrap(role, added_roles=[]):
  role_config = load_role_config(role)
  for requirement in role_config['requirements']:
    if requirement not in added_roles:
      added_roles += bootstrap(requirement, added_roles+role_config['requirements'])
      #added_roles += bootstrap(requirement, added_roles+[requirement])
  print "bootstrapping "+role
  return role
  #return added_roles

def deploy():
  roles = sys.argv[1:]
  for role in roles:
    #bootstrap(role)
    #exit()
    instances = launch_instances(role)
    for instance in instances:
      instance = ec2.Instance(instance.instance_id)
      bootstrap_instance(instance,role)
      print "\n"+role+" instance available at "+instance.public_ip_address+"\n"
  print "deploy complete"

deploy()

exit()
