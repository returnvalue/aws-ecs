# Lab 5: Application Load Balancer Integration (IP Targets)

**Goal:** Prepare for a highly available web service. Because we use `awsvpc` network mode, the ALB Target Group must be configured with `TargetType=ip` (not instance IDs) to correctly route traffic to individual task ENIs.

```bash
# 1. Create the ALB
ALB_ARN=$(awslocal elbv2 create-load-balancer \
  --name ECS-Web-ALB \
  --subnets $SUBNET_1 $SUBNET_2 \
  --security-groups $TASK_SG \
  --query 'LoadBalancers[0].LoadBalancerArn' --output text)
ALB_ARN=$(aws elbv2 create-load-balancer \
  --name ECS-Web-ALB \
  --subnets $SUBNET_1 $SUBNET_2 \
  --security-groups $TASK_SG \
  --query 'LoadBalancers[0].LoadBalancerArn' --output text)

# 2. Create a Target Group (Crucial: --target-type ip)
TG_ARN=$(awslocal elbv2 create-target-group \
  --name ECS-Web-TG \
  --protocol HTTP --port 80 \
  --vpc-id $VPC_ID \
  --target-type ip \
  --query 'TargetGroups[0].TargetGroupArn' --output text)
TG_ARN=$(aws elbv2 create-target-group \
  --name ECS-Web-TG \
  --protocol HTTP --port 80 \
  --vpc-id $VPC_ID \
  --target-type ip \
  --query 'TargetGroups[0].TargetGroupArn' --output text)

# 3. Create the Listener
awslocal elbv2 create-listener \
  --load-balancer-arn $ALB_ARN \
  --protocol HTTP --port 80 \
  --default-actions Type=forward,TargetGroupArn=$TG_ARN
aws elbv2 create-listener \
  --load-balancer-arn $ALB_ARN \
  --protocol HTTP --port 80 \
  --default-actions Type=forward,TargetGroupArn=$TG_ARN
```

## 🧠 Key Concepts & Importance

- **Target Type 'ip':** In `awsvpc` network mode, each task is assigned its own private IP address from the subnet. The ALB must route traffic directly to these IPs rather than to an EC2 instance ID.
- **Load Balancing:** Distributes incoming traffic across multiple tasks to ensure application availability and fault tolerance.
- **Listeners & Rules:** A listener checks for connection requests. Rules determine how the load balancer routes requests to its registered targets.
- **Service Decoupling:** The ALB acts as a single entry point for your application, hiding the complexity of the underlying container fleet.

## 🛠️ Command Reference

- `elbv2 create-load-balancer`: Creates an Application Load Balancer.
    - `--subnets`: The subnets to attach to the load balancer (Multi-AZ).
- `elbv2 create-target-group`: Creates a target group used to route requests.
    - `--target-type`: Specifies how you register targets (set to `ip` for ECS Fargate).
- `elbv2 create-listener`: Creates a listener for the load balancer.
    - `--default-actions`: Defines the default routing behavior (e.g., forwarding to a target group).

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
