## Reasoning

My solution is a straightforward and simple approach to the exercise.
The main Python script facilitates all AWS interactions for deploying the instance, uploads the list of necessary config files and the main bash setup script, and then executes the bash script on the instance which completes the rest of the setup.
The bash script is customized for the service being deployed (in this case ElasticSearch), installs all the necessary services, and configures the services based on the config files that were uploaded.
Instance deployment information, as well as the list of config files to upload and the setup script to use are stored in a primary config file, which can be modified to suit whatever service needs to be deployed.

By modifying the python script to take an argument for which deploy config to use, and by using different deploy configs, you could deploy multiple services with a generic python deploy script.
Additionally, you could modify the deploy configs to have information on deploying multiple types of instances and services, which could potentially enable deploying a full stack of services.

However, this gets very close to functionality provided by deployment solutions like Chef.
I chose not to use Chef for this because I have no experience setting up and configuring a Chef server, nor experience writing a Chef recipe and cookbook from scratch.
I was able to use Python and bash scripts to mimic the functionality you could achieve by using a scripting language like Python to orchestrate the deployment of AWS instances with Chef pre-installed on the ami, and then kick off Chef executions on the instances to complete the service configuration (or you could just use Chef for the whole process).

Also, using Python and bash allowed me to test as I developed my solution, as I could deploy an instance, determine what shell commands I needed to execute to install a step, update the setup script, retest and redeploy, and repeat until I no longer had any steps to automate.

I chose to use NGINX as my tool to secure ElasticSearch because NGINX can be utilized for all kinds of services, and by splitting up the setup script into two (one for NGINX and one for installing and securing ElasticSearch), you could utilize the same NGINX initial setup on other service deployments.
NGINX also provided a very straightforward and simple solution for securing a service with user auth and ssl.

## Feedback

I enjoyed working on the project, and it was fun to shake off the rust after not doing this kind of development for a while.
I think the exercise touches on a lot of good points for devops.
It gets you thinking not only on the current task, but where to go from it.
It has you setting up a service you may or may not have ever worked with before, and for me I had never set up or configured ElasticSearch, so that was a new experience.
I also had never dealt too much with securing a service beyond configuring AWS security groups, so it was new configuring NGINX as well.
The only familiar territory for me was working in Python (though I haven't used Boto3 much at all before), bash scripting, AWS, and the general deployment process.

I started this project on 5/15, and it took me roughly three full days to have a deployment solution that successfully deploys and secures a single ElasticSearch node, and about another half day cleaning up some code and documentation.
It took a day to have my Python script deploying an instance and able to connect for ssh and ftp, another day to get ElasticSearch up and running, and one more day to get everything properly secured using NGINX, ssl, and user auth.

## Questions

### How did you choose to automate the provisioning and bootstrapping of the instance? Why?
I chose Python as my tool for automating provisioning and initiating bootstrapping because the Boto3 and paramiko packages provided all the tools I needed to interact with AWS to deploy an instance and connect to an instance to put config files and execute scripts. I chose to use a bash script as my bootstrapping method because I was able to break down the setup process into a series of well constructed shell commands that would install and configure services and configs.

### How did you choose to secure ElasticSearch? Why?
I chose NGINX because there were many resources online for how to secure a service using ssl and user authentification. I have never secured a service in this manner before, so I chose a tool that is easy to configure and can be utilized with a multitude of services.

### How would you monitor this instance? What metrics would you monitor?
I would create custom AWS cloudwatch metrics (which would also require a service that uploads said metrics). I would monitor the java ElasticSearch process and the nginx process, along with cpu utilization and load, in addition to the standard AWS cloudwatch metrics.

### Could you extend your solution to launch a secure cluster of ElasticSearch nodes? What would need to change to support this use case?
Improve the python deploy script and deploy config file structure to allow for a single deploy config that contains information on two types of instances to deploy (master and slave), each with its own set of setup scripts and configs. Configure the nodes to talk to eachother using AWS private IPs, secured using a single security group, along with the standard securing via NGINX. To further control traffic, you could put the instances behind a loadbalancer, with the slaves in an autoscaling group.

### Could you extend your solution to replace a running ElasticSearch instance with little or no downtime? How?
Improve the python deploy script to also allow for setting up loadbalancers and autoscale groups. Place the cluster within an autoscale group, which would allow mostly seamless replacing of nodes. Master node is a little more tricky, but if it too was behind a loadbalancer in an autoscale group, and if there were multiple nodes as master, it also would be a seamless replacement.

### Was it a priority to make your code well structured, extensible, and reusable?
I wanted to have the potential to use the Python deploy script for different services, so I utilized a config file to control how the deployment proceded. Some alterations to the config structure and python script could make it easier to deploy multiple kinds of instances with a single deploy, but currently it can deploy multiple instances of the same type (in this case ElasticSearch).

### What sacrifices did you make due to time?
My initial goal was achieving full functionality to deploy and secure ElasticSearch, so my code was written straightforward and simple. I sacrificed well commented code and did not split up my python script into functions as I should have. I also could have tested more variants in my deploy config. With my code functioning properly, I intend on further code cleanup and modifications to improve efficiency and make the code more extensible.
