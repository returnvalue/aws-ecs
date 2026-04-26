# Lab 3: ECS Cluster & Task Definitions (awsvpc mode)

**Goal:** Create a serverless Fargate cluster and define the blueprint (Task Definition) for our application using the `awsvpc` network mode.
```bash
# 1. Create the ECS Cluster
awslocal ecs create-cluster --cluster-name FargateCluster
aws ecs create-cluster --cluster-name FargateCluster

# 2. Create the Task Definition JSON
cat <<EOF > task-def.json
{
  "family": "web-app",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "$EXEC_ROLE_ARN",
  "taskRoleArn": "$TASK_ROLE_ARN",
  "containerDefinitions": [
    {
      "name": "nginx-container",
      "image": "nginx:latest",
      "essential": true,
      "portMappings": [{"containerPort": 80, "hostPort": 80, "protocol": "tcp"}],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/web-app",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
EOF

# 3. Register the Task Definition
TASK_DEF_ARN=$(awslocal ecs register-task-definition --cli-input-json file://task-def.json --query 'taskDefinition.taskDefinitionArn' --output text)
TASK_DEF_ARN=$(aws ecs register-task-definition --cli-input-json file://task-def.json --query 'taskDefinition.taskDefinitionArn' --output text)
```

## 🧠 Key Concepts & Importance

- **ECS Cluster:** A logical grouping of tasks or services. For Fargate, the cluster is serverless and doesn't require managing EC2 instances.
- **Task Definition:** A blueprint for your application. It defines which container image to use, how much CPU and memory to allocate, and which IAM roles to use.
- **awsvpc Network Mode:** The recommended network mode for ECS. It gives each task its own elastic network interface (ENI) and a private IP address from the VPC, providing full networking features and security group control.
- **Fargate Launch Type:** A serverless way to run containers. You pay for the resources (vCPU and memory) consumed by your containers, without managing the underlying servers.
- **Log Configuration:** Defines where your container logs are sent. In this lab, we use the `awslogs` driver to send logs to CloudWatch.

## 🛠️ Command Reference

- `ecs create-cluster`: Creates a new Amazon ECS cluster.
    - `--cluster-name`: The name of the cluster.
- `ecs register-task-definition`: Registers a new task definition revision.
    - `--cli-input-json`: Path to the JSON file containing the task definition.

---

💡 **Pro Tip: Using `aws` instead of `awslocal`**

If you prefer using the standard `aws` CLI without the `awslocal` wrapper or repeating the `--endpoint-url` flag, you can configure a dedicated profile in your AWS config files.

### 1. Configure your Profile
Add the following to your `~/.aws/config` file:
```ini
[profile localstack]
region = us-east-1
output = json
# This line redirects all commands for this profile to LocalStack
endpoint_url = http://localhost:4566
```

Add matching dummy credentials to your `~/.aws/credentials` file:
```ini
[localstack]
aws_access_key_id = test
aws_secret_access_key = test
```

### 2. Use it in your Terminal
You can now run commands in two ways:

**Option A: Pass the profile flag**
```bash
aws iam create-user --user-name DevUser --profile localstack
```

**Option B: Set an environment variable (Recommended)**
Set your profile once in your session, and all subsequent `aws` commands will automatically target LocalStack:
```bash
export AWS_PROFILE=localstack
aws iam create-user --user-name DevUser
```

### Why this works
- **Precedence**: The AWS CLI (v2) supports a global `endpoint_url` setting within a profile. When this is set, the CLI automatically redirects all API calls for that profile to your local container instead of the real AWS cloud.
- **Convenience**: This allows you to use the standard documentation commands exactly as written, which is helpful if you are copy-pasting examples from AWS labs or tutorials.
