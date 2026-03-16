import boto3
import json

def main():
    ec2 = boto3.client('ec2', endpoint_url="http://localhost:4566", region_name="us-east-1")
    ecr = boto3.client('ecr', endpoint_url="http://localhost:4566", region_name="us-east-1")

    # 1. Create VPC and two Subnets
    vpc_response = ec2.create_vpc(CidrBlock='10.0.0.0/16')
    vpc_id = vpc_response['Vpc']['VpcId']
    print(f"Created VPC: {vpc_id}")

    subnet1_response = ec2.create_subnet(VpcId=vpc_id, CidrBlock='10.0.1.0/24', AvailabilityZone='us-east-1a')
    subnet_1 = subnet1_response['Subnet']['SubnetId']
    print(f"Created Subnet 1: {subnet_1}")

    subnet2_response = ec2.create_subnet(VpcId=vpc_id, CidrBlock='10.0.2.0/24', AvailabilityZone='us-east-1b')
    subnet_2 = subnet2_response['Subnet']['SubnetId']
    print(f"Created Subnet 2: {subnet_2}")

    # 2. Create an Internet Gateway and Route Table
    igw_response = ec2.create_internet_gateway()
    igw_id = igw_response['InternetGateway']['InternetGatewayId']
    print(f"Created Internet Gateway: {igw_id}")

    ec2.attach_internet_gateway(VpcId=vpc_id, InternetGatewayId=igw_id)
    
    rt_response = ec2.create_route_table(VpcId=vpc_id)
    rt_id = rt_response['RouteTable']['RouteTableId']
    print(f"Created Route Table: {rt_id}")

    ec2.create_route(RouteTableId=rt_id, DestinationCidrBlock='0.0.0.0/0', GatewayId=igw_id)
    
    ec2.associate_route_table(SubnetId=subnet_1, RouteTableId=rt_id)
    ec2.associate_route_table(SubnetId=subnet_2, RouteTableId=rt_id)

    # 3. Create a Security Group for the containers (Task-level security)
    sg_response = ec2.create_security_group(GroupName='ECSTaskSG', Description='Allow HTTP', VpcId=vpc_id)
    task_sg = sg_response['GroupId']
    print(f"Created Security Group: {task_sg}")

    ec2.authorize_security_group_ingress(GroupId=task_sg, IpProtocol='tcp', FromPort=80, ToPort=80, CidrIp='0.0.0.0/0')

    # 4. Create an ECR Repository
    ecr_response = ecr.create_repository(repositoryName='my-web-app')
    print(f"Created ECR Repository: {ecr_response['repository']['repositoryName']}")

if __name__ == '__main__':
    main()
