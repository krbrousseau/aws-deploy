# Reasoning

# Feedback

I started this project on 5/15, and it took me roughly three full days to have a deployment solution that successfully deploys and secures a single ElasticSearch node.

# Questions

How did you choose to automate the provisioning and bootstrapping of the instance? Why?
 - used python boto3 to launch the AWS instance, and then utilized a bash script to setup and configure the services on the instance
How did you choose to secure ElasticSearch? Why?
 - i utilized nginx because it was the easiest to configure and can be used for other applications
How would you monitor this instance? What metrics would you monitor?
 - utilize AWS cloudwatch to monitor that the elasticsearch and nginx processes are running
Could you extend your solution to launch a secure cluster of ElasticSearch nodes? What would need to change to support this use case?
 - create designated setup configs for master and slave nodes, and set up each instance
Could you extend your solution to replace a running ElasticSearch instance with little or no downtime? How?
 - add functionality to place elasticsearch instances behind a loadbalancer in an autoscale group, which would take care of replacing nodes and scaling a cluster
Was it a priority to make your code well structured, extensible, and reusable?
 - code written to be extendsible to deploy multiple kinds of services
What sacrifices did you make due to time?
 - little commenting, no tests
