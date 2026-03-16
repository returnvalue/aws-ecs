import boto3

def main():
    ecs = boto3.client('ecs', endpoint_url="http://localhost:4566", region_name="us-east-1")
    ec2 = boto3.client('ec2', endpoint_url="http://localhost:4566", region_name="us-east-1")
    elbv2 = boto3.client('elbv2', endpoint_url="http://localhost:4566", region_name="us-east-1")

    # Get Subnets and Security Group
    subnets = ec2.describe_subnets()['Subnets']
    subnet_ids = [subnet['SubnetId'] for subnet in subnets][:2]
    
    sgs = ec2.describe_security_groups(GroupNames=['ECSTaskSG'])['SecurityGroups']
    task_sg = sgs[0]['GroupId'] if sgs else 'sg-000'

    # Get Target Group ARN
    tgs = elbv2.describe_target_groups(Names=['ECS-Web-TG'])['TargetGroups']
    tg_arn = tgs[0]['TargetGroupArn'] if tgs else 'arn:aws:elasticloadbalancing:us-east-1:000000000000:targetgroup/ECS-Web-TG/000'

    # Create the ECS Service tied to the ALB
    service_response = ecs.create_service(
        cluster='FargateCluster',
        serviceName='WebAppService',
        taskDefinition='web-app',
        desiredCount=2,
        launchType='FARGATE',
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': subnet_ids,
                'securityGroups': [task_sg],
                'assignPublicIp': 'ENABLED'
            }
        },
        loadBalancers=[
            {
                'targetGroupArn': tg_arn,
                'containerName': 'nginx-container',
                'containerPort': 80
            }
        ]
    )
    print(f"Created ECS Service: {service_response['service']['serviceArn']}")

if __name__ == '__main__':
    main()
