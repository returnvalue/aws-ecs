import boto3

def main():
    ecs = boto3.client('ecs', endpoint_url="http://localhost:4566", region_name="us-east-1")
    ec2 = boto3.client('ec2', endpoint_url="http://localhost:4566", region_name="us-east-1")

    # Get subnet and security group to be robust
    subnets = ec2.describe_subnets()['Subnets']
    subnet_1 = subnets[0]['SubnetId'] if subnets else 'subnet-000'
    sgs = ec2.describe_security_groups(GroupNames=['ECSTaskSG'])['SecurityGroups']
    task_sg = sgs[0]['GroupId'] if sgs else 'sg-000'

    # Run a standalone task directly into our VPC
    response = ecs.run_task(
        cluster='FargateCluster',
        launchType='FARGATE',
        taskDefinition='web-app',
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': [subnet_1],
                'securityGroups': [task_sg],
                'assignPublicIp': 'ENABLED'
            }
        }
    )
    print(f"Ran Task: {response['tasks'][0]['taskArn'] if response['tasks'] else 'Failed'}")

if __name__ == '__main__':
    main()
