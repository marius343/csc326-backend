AccessKey = "REMOVED"
SecretKey = "REMOVED"
region = "us-east-1"

import boto
import boto.ec2

theServer = boto.connect_ec2(region=boto.ec2.get_region(region), aws_access_key_id=AccessKey, aws_secret_access_key=SecretKey)

key_pair = theServer.create_key_pair('engineKey')
key_pair.save('./')

#securityGroup = theServer.create_security_group("engineSecurity", "This is the search engine security group")

#Authorizing security group for various protocals
theServer.authorize_security_group(group_name ="engineSecurity", ip_protocol="icmp", from_port=-1, to_port=-1, cidr_ip ="0.0.0.0/0")
theServer.authorize_security_group(group_name ="engineSecurity", ip_protocol="tcp", from_port=22, to_port=22, cidr_ip ="0.0.0.0/0")
theServer.authorize_security_group(group_name ="engineSecurity", ip_protocol="tcp", from_port=80, to_port=80, cidr_ip ="0.0.0.0/0")

#starting micro instance of ubuntu
instances = theServer.run_instances(image_id="ami-cd0f5cb6", key_name='engineKey')

# Wait a minute or two while it boots
running = 0
while(running == 0):
    for r in theServer.get_all_instances():
        print r.id, r.instances[0].state
        if(r.instances[0].state == "running" ):
            validInstance = r
            running = 1
            break

print validInstance.instances[0].public_dns_name
print validInstance.instances[0].ip_address

