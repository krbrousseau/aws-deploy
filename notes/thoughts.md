Previous version thoughts can be found [here](thoughts-v0.1.md)

## Reasoning [v0.1](thoughts-v0.1.md#reasoning)
I went back and refactored the config structure to make the code more extensible.
I pulled the role specific configs into their own separate configs, and left the primary config information in the main directory.
This would allow me to have multiple configs for different roles, and allow the deploy of different roles using a generic deploy script.
This also allowed me to incorporate role requirements, which allowed me to create role dependencies that can be used across different services (nginx for example).
What I have now is a little closer to the functionality that Chef provides with it's cookbooks and recipes.

## Feedback [v0.1](thoughts-v0.1.md#feedback)
Nothing new to add here, see previous version.

## Questions [v0.1](thoughts-v0.1.md#questions)
### How did you choose to automate the provisioning and bootstrapping of the instance? Why?
Provisioning and Bootstrapping method is mostly unchanged. The Boto3 package handles the launch of the instance, and bash scripts handle the bootstrapping. The recursive bootstrapping behavior for role dependencies is new, but provides the same function.
### How did you choose to secure ElasticSearch? Why?
Unchanged, see previous version.
### How would you monitor this instance? What metrics would you monitor?
I would create a role specifically for installing a metric collection service, and add that as a dependency. Rest of answer is unchanged, see previous version.
### Could you extend your solution to launch a secure cluster of ElasticSearch nodes? What would need to change to support this use case?
I would split up the ElasticSearch role into master and slave roles, and then launch them together to be configured together. The current python deploy script can launch multiple roles at once. See previous version for rest of answer.
### Could you extend your solution to replace a running ElasticSearch instance with little or no downtime? How?
See previous version.
### Was it a priority to make your code well structured, extensible, and reusable?
Going back through my code allowed me to break up the giant script into functions and reformat the config structure. This makes it much easier to add new roles in the future, and the main script is a little easier to follow.
### What sacrifices did you make due to time?
I'm still a little light on comments, but the code is better structured after my second iteration.
