import boto3
import json

def main():
    ecs = boto3.client('ecs', endpoint_url="http://localhost:4566", region_name="us-east-1")

    # For the sake of the script, we assume the ARNs are known or we can just fetch them or use placeholder if needed,
    # but let's query IAM to get the ARNs dynamically to be robust, or we can just use the name since aws localstack might allow it,
    # wait, IAM get_role is better.
    iam = boto3.client('iam', endpoint_url="http://localhost:4566", region_name="us-east-1")
    exec_role_arn = iam.get_role(RoleName='ecsTaskExecutionRole')['Role']['Arn']
    task_role_arn = iam.get_role(RoleName='ecsAppTaskRole')['Role']['Arn']

    # 1. Create the ECS Cluster
    cluster_response = ecs.create_cluster(clusterName='FargateCluster')
    print(f"Created ECS Cluster: {cluster_response['cluster']['clusterName']}")

    # 3. Register the Task Definition
    task_def_response = ecs.register_task_definition(
        family='web-app',
        networkMode='awsvpc',
        requiresCompatibilities=['FARGATE'],
        cpu='256',
        memory='512',
        executionRoleArn=exec_role_arn,
        taskRoleArn=task_role_arn,
        containerDefinitions=[
            {
                'name': 'nginx-container',
                'image': 'nginx:latest',
                'essential': True,
                'portMappings': [{'containerPort': 80, 'hostPort': 80, 'protocol': 'tcp'}],
                'logConfiguration': {
                    'logDriver': 'awslogs',
                    'options': {
                        'awslogs-group': '/ecs/web-app',
                        'awslogs-region': 'us-east-1',
                        'awslogs-stream-prefix': 'ecs'
                    }
                }
            }
        ]
    )
    print(f"Registered Task Definition: {task_def_response['taskDefinition']['taskDefinitionArn']}")

if __name__ == '__main__':
    main()
