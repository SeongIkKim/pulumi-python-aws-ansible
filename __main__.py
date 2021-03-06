import pulumi
import pulumi_aws as aws
from pulumi_aws import ec2

# AMI image configuration
ec2_image_id = 'ami-07d1bb89ff2dd50fe'
ec2_image_owner = '099720109477'
ec2_instance_size = 't2.micro'
ec2_instance_name = 'aws-ec2-ubuntu'
ec2_keypair_name = 'pulumi_key'
ec2_ssh_port = 22

# Lets use Pulumi to get the AMI image
pulumi_ami = aws.get_ami(
                    filters = [{ "name": "image-id", "values": [ec2_image_id]}],
                    owners  = [ec2_image_owner])

# Create a EC2 security group
pulumi_security_group = ec2.SecurityGroup(
                            'pulumi-secgrp',
                            description = 'pulumi: enable SSH access & outgoing connections',
                            ingress = [
                                { 'protocol': 'tcp', 'from_port': ec2_ssh_port, 'to_port': ec2_ssh_port, 'cidr_blocks': ['0.0.0.0/0'] }
                            ],
                            egress = [
                                { 'protocol': '-1', 'from_port': 0, 'to_port': 0, 'cidr_blocks': ['0.0.0.0/0'] }
                            ]
)

# Create EC2 instance
ec2_instance = ec2.Instance(
                    ec2_instance_name,
                    key_name = ec2_keypair_name,
                    instance_type = ec2_instance_size,
                    security_groups = [pulumi_security_group.name],
                    ami = pulumi_ami.id
)

pulumi.export('publicIp', ec2_instance.public_ip)
pulumi.export('publicHostName', ec2_instance.public_dns)
