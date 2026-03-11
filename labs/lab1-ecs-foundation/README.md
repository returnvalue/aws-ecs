# Lab 1: Networking Foundation & ECR Registry

**Goal:** Create a multi-AZ VPC for high availability and provision an Elastic Container Registry (ECR) to securely store our Docker images.

```bash
# 1. Create VPC and two Subnets
VPC_ID=$(awslocal ec2 create-vpc --cidr-block 10.0.0.0/16 --query 'Vpc.VpcId' --output text)
SUBNET_1=$(awslocal ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.0.1.0/24 --availability-zone us-east-1a --query 'Subnet.SubnetId' --output text)
SUBNET_2=$(awslocal ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.0.2.0/24 --availability-zone us-east-1b --query 'Subnet.SubnetId' --output text)

# 2. Create an Internet Gateway and Route Table
IGW_ID=$(awslocal ec2 create-internet-gateway --query 'InternetGateway.InternetGatewayId' --output text)
awslocal ec2 attach-internet-gateway --vpc-id $VPC_ID --internet-gateway-id $IGW_ID
RT_ID=$(awslocal ec2 create-route-table --vpc-id $VPC_ID --query 'RouteTable.RouteTableId' --output text)
awslocal ec2 create-route --route-table-id $RT_ID --destination-cidr-block 0.0.0.0/0 --gateway-id $IGW_ID
awslocal ec2 associate-route-table --subnet-id $SUBNET_1 --route-table-id $RT_ID
awslocal ec2 associate-route-table --subnet-id $SUBNET_2 --route-table-id $RT_ID

# 3. Create a Security Group for the containers (Task-level security)
TASK_SG=$(awslocal ec2 create-security-group --group-name ECSTaskSG --description "Allow HTTP" --vpc-id $VPC_ID --query 'GroupId' --output text)
awslocal ec2 authorize-security-group-ingress --group-id $TASK_SG --protocol tcp --port 80 --cidr 0.0.0.0/0

# 4. Create an ECR Repository
awslocal ecr create-repository --repository-name my-web-app
```

## 🧠 Key Concepts & Importance

- **Amazon ECR (Elastic Container Registry):** A fully managed Docker container registry that makes it easy for developers to store, manage, and deploy Docker container images.
- **Multi-AZ Networking:** Creating subnets in multiple Availability Zones is crucial for high availability, ensuring that your containerized tasks can be distributed across different physical data centers.
- **Task-Level Security Groups:** Security groups are applied at the task level in ECS, allowing for granular control over the traffic entering and leaving your containers.
- **Internet Gateway (IGW):** Enables communication between your VPC and the internet, allowing you to pull public images or expose your services to the web.

## 🛠️ Command Reference

- `ec2 create-vpc`: Creates a VPC with the specified IPv4 CIDR block.
- `ec2 create-subnet`: Creates a subnet in a specific Availability Zone.
- `ec2 create-internet-gateway`: Creates an internet gateway for use with a VPC.
- `ec2 attach-internet-gateway`: Attaches an internet gateway to a VPC.
- `ec2 create-route-table`: Creates a route table for a VPC.
- `ec2 create-route`: Creates a route in a route table within a VPC.
- `ec2 associate-route-table`: Associates a subnet with a route table.
- `ec2 create-security-group`: Creates a security group for a VPC.
- `ec2 authorize-security-group-ingress`: Adds an inbound rule to a security group.
- `ecr create-repository`: Creates a new ECR image repository.
    - `--repository-name`: The name to give the repository.
