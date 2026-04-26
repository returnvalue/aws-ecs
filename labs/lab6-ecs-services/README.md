# Lab 6: ECS Long-Running Services

**Goal:** Deploy the application as an ECS Service. Services automatically maintain a desired number of tasks, restarting them if they fail, and registering them with the ALB.
```bash
# Create the ECS Service tied to the ALB
awslocal ecs create-service \
  --cluster FargateCluster \
  --service-name WebAppService \
  --task-definition web-app \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[$SUBNET_1,$SUBNET_2],securityGroups=[$TASK_SG],assignPublicIp=ENABLED}" \
  --load-balancers "targetGroupArn=$TG_ARN,containerName=nginx-container,containerPort=80"
aws ecs create-service \
  --cluster FargateCluster \
  --service-name WebAppService \
  --task-definition web-app \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[$SUBNET_1,$SUBNET_2],securityGroups=[$TASK_SG],assignPublicIp=ENABLED}" \
  --load-balancers "targetGroupArn=$TG_ARN,containerName=nginx-container,containerPort=80"
```

## 🧠 Key Concepts & Importance

- **ECS Service:** Allows you to run and maintain a specified number of instances of a task definition simultaneously in an Amazon ECS cluster. If any of your tasks fail or stop, the Amazon ECS service scheduler launches another instance of your task definition to replace it.
- **Service Scheduler:** Responsible for maintaining the desired count of tasks and ensuring they are spread across Availability Zones.
- **ALB Integration:** When a service is configured with a load balancer, the service scheduler automatically registers and deregisters containers with the target group.
- **High Availability (Desired Count):** By setting a `desired-count` greater than 1, you ensure that your application can handle task failures without downtime.
- **Self-Healing:** The primary advantage of a Service over a standalone task is its ability to automatically recover from failures.

## 🛠️ Command Reference

- `ecs create-service`: Runs and maintains a desired number of tasks from a specified task definition.
    - `--cluster`: The short name or full Amazon Resource Name (ARN) of the cluster on which to run your service.
    - `--service-name`: The name of your service.
    - `--task-definition`: The `family` and `revision` (family:revision) or full ARN of the task definition to run in your service.
    - `--desired-count`: The number of instantiations of the specified task definition to place and keep running on your cluster.
    - `--launch-type`: The launch type on which to run your service (set to `FARGATE`).
    - `--load-balancers`: A load balancer object that represents the load balancer to use with your service.

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
