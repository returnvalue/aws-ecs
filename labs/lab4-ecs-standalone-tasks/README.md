# Lab 4: Running Standalone Tasks (Fargate)

**Goal:** Execute a one-off, serverless task. This pattern is ideal for batch jobs, database migrations, or scheduled cron jobs.
```bash
# Run a standalone task directly into our VPC
awslocal ecs run-task \
  --cluster FargateCluster \
  --launch-type FARGATE \
  --task-definition web-app \
  --network-configuration "awsvpcConfiguration={subnets=[$SUBNET_1],securityGroups=[$TASK_SG],assignPublicIp=ENABLED}"
aws ecs run-task \
  --cluster FargateCluster \
  --launch-type FARGATE \
  --task-definition web-app \
  --network-configuration "awsvpcConfiguration={subnets=[$SUBNET_1],securityGroups=[$TASK_SG],assignPublicIp=ENABLED}"
```

## 🧠 Key Concepts & Importance

- **Standalone Tasks:** Used for processes that run to completion and then exit, rather than long-running services that need to stay active.
- **Fargate Launch Type:** Eliminates the need to provision or manage EC2 instances. You only specify the task and its resource requirements.
- **Network Configuration:** When using `awsvpc` mode, you must explicitly define the subnets and security groups for the task's Elastic Network Interface (ENI).
- **Use Cases:** 
    - Database migrations (running a script once).
    - Image processing or batch analytics.
    - Periodic cleanup tasks (triggered by CloudWatch Events/EventBridge).

## 🛠️ Command Reference

- `ecs run-task`: Starts a new task using the specified task definition.
    - `--cluster`: The short name or full Amazon Resource Name (ARN) of the cluster on which to run your task.
    - `--launch-type`: The launch type on which to run your task (set to `FARGATE`).
    - `--task-definition`: The `family` and `revision` (family:revision) or full ARN of the task definition to run.
    - `--network-configuration`: The network configuration for the task, including subnets and security groups.

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
