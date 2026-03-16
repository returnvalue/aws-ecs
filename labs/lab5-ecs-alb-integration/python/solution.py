import boto3

def main():
    elbv2 = boto3.client('elbv2', endpoint_url="http://localhost:4566", region_name="us-east-1")
    ec2 = boto3.client('ec2', endpoint_url="http://localhost:4566", region_name="us-east-1")

    # Get VPC, Subnets, and Security Group
    vpcs = ec2.describe_vpcs()['Vpcs']
    vpc_id = vpcs[0]['VpcId'] if vpcs else 'vpc-000'
    
    subnets = ec2.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])['Subnets']
    subnet_ids = [subnet['SubnetId'] for subnet in subnets][:2]
    
    sgs = ec2.describe_security_groups(GroupNames=['ECSTaskSG'])['SecurityGroups']
    task_sg = sgs[0]['GroupId'] if sgs else 'sg-000'

    # 1. Create the ALB
    alb_response = elbv2.create_load_balancer(
        Name='ECS-Web-ALB',
        Subnets=subnet_ids,
        SecurityGroups=[task_sg]
    )
    alb_arn = alb_response['LoadBalancers'][0]['LoadBalancerArn']
    print(f"Created ALB: {alb_arn}")

    # 2. Create a Target Group (Crucial: --target-type ip)
    tg_response = elbv2.create_target_group(
        Name='ECS-Web-TG',
        Protocol='HTTP',
        Port=80,
        VpcId=vpc_id,
        TargetType='ip'
    )
    tg_arn = tg_response['TargetGroups'][0]['TargetGroupArn']
    print(f"Created Target Group: {tg_arn}")

    # 3. Create the Listener
    listener_response = elbv2.create_listener(
        LoadBalancerArn=alb_arn,
        Protocol='HTTP',
        Port=80,
        DefaultActions=[
            {
                'Type': 'forward',
                'TargetGroupArn': tg_arn
            }
        ]
    )
    print(f"Created Listener: {listener_response['Listeners'][0]['ListenerArn']}")

if __name__ == '__main__':
    main()
