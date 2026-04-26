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
EXEC_ROLE_ARN=$(aws iam create-role --role-name ecsTaskExecutionRole --assume-role-policy-document file://ecs-trust.json --query 'Role.Arn' --output text)
awslocal iam attach-role-policy --role-name ecsTaskExecutionRole --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
aws iam attach-role-policy --role-name ecsTaskExecutionRole --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy

# 3. Create the Task Role (For the Application itself)
TASK_ROLE_ARN=$(awslocal iam create-role --role-name ecsAppTaskRole --assume-role-policy-document file://ecs-trust.json --query 'Role.Arn' --output text)
TASK_ROLE_ARN=$(aws iam create-role --role-name ecsAppTaskRole --assume-role-policy-document file://ecs-trust.json --query 'Role.Arn' --output text)
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
