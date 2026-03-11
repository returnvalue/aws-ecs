# Lab 2: IAM Role Separation (Execution vs. Task Roles)

**Goal:** Security best practices require strict IAM separation. The Execution Role allows ECS to pull images and push logs. The Task Role allows your application code to access AWS services (like S3).

```bash
# 1. Create the Trust Policy for ECS Tasks
cat <<EOF > ecs-trust.json
{
  "Version": "2012-10-17",
  "Statement": [{"Effect": "Allow", "Principal": {"Service": "ecs-tasks.amazonaws.com"}, "Action": "sts:AssumeRole"}]
}
EOF

# 2. Create the Task Execution Role (For the ECS Agent)
EXEC_ROLE_ARN=$(awslocal iam create-role --role-name ecsTaskExecutionRole --assume-role-policy-document file://ecs-trust.json --query 'Role.Arn' --output text)
awslocal iam attach-role-policy --role-name ecsTaskExecutionRole --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy

# 3. Create the Task Role (For the Application itself)
TASK_ROLE_ARN=$(awslocal iam create-role --role-name ecsAppTaskRole --assume-role-policy-document file://ecs-trust.json --query 'Role.Arn' --output text)
# (In a real scenario, you would attach S3 or DynamoDB policies here)
```

## 🧠 Key Concepts & Importance

- **Task Execution Role:** This role is used by the Amazon ECS container agent and the Fargate agent. It allows the agent to pull container images from ECR and send container logs to CloudWatch Logs.
- **Task Role:** This is the IAM role that the containers in your task assume. If your application code needs to access AWS services like S3, DynamoDB, or SQS, you define those permissions here.
- **Principle of Least Privilege:** By separating these roles, you ensure that the application code only has access to the specific resources it needs, and not the underlying infrastructure permissions required by the ECS agent.
- **Trust Policy:** Both roles must have a trust policy that allows the `ecs-tasks.amazonaws.com` service principal to assume the role.

## 🛠️ Command Reference

- `iam create-role`: Creates a new IAM role for your AWS account.
    - `--role-name`: The name of the role to create.
    - `--assume-role-policy-document`: The trust relationship policy document.
- `iam attach-role-policy`: Attaches a managed policy to an IAM role.
    - `--policy-arn`: The ARN of the policy to attach (e.g., `AmazonECSTaskExecutionRolePolicy`).
