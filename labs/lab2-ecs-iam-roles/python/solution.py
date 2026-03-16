import boto3
import json

def main():
    iam = boto3.client('iam', endpoint_url="http://localhost:4566", region_name="us-east-1")

    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "ecs-tasks.amazonaws.com"},
                "Action": "sts:AssumeRole"
            }
        ]
    }

    # 2. Create the Task Execution Role
    exec_role_response = iam.create_role(
        RoleName='ecsTaskExecutionRole',
        AssumeRolePolicyDocument=json.dumps(trust_policy)
    )
    exec_role_arn = exec_role_response['Role']['Arn']
    print(f"Created Execution Role: {exec_role_arn}")

    iam.attach_role_policy(
        RoleName='ecsTaskExecutionRole',
        PolicyArn='arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy'
    )

    # 3. Create the Task Role
    task_role_response = iam.create_role(
        RoleName='ecsAppTaskRole',
        AssumeRolePolicyDocument=json.dumps(trust_policy)
    )
    task_role_arn = task_role_response['Role']['Arn']
    print(f"Created Task Role: {task_role_arn}")

if __name__ == '__main__':
    main()
