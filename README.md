# Script for Passwordless ssh login to multiple machines

# Requirements 
* python needs to be installed 

# Input
Yaml file containing the host names, UserName (same for all the nodes) and passwords for the hosts 

```
user:
    User_name for all the hosts
host:
    worker1:
        host_name: host_ip
        password: password
```

#Usage:

* The script should be run as follows
```
python ssh_passwordless.ssh config.yaml
```










