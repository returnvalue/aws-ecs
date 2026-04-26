# Lab 7: Service Auto Scaling (Target Tracking)

**Goal:** Handle unpredictable web traffic automatically. We will register the ECS service with Application Auto Scaling and apply a policy to scale tasks out/in based on average CPU utilization.
```bash
# 1. Register the ECS Service as a Scalable Target (Min 2, Max 10 tasks)
awslocal application-autoscaling register-scalable-target \
  --service-namespace ecs \
  --resource-id service/FargateCluster/WebAppService \
  --scalable-dimension ecs:service:DesiredCount \
  --min-capacity 2 \
  --max-capacity 10
aws application-autoscaling register-scalable-target \
  --service-namespace ecs \
  --resource-id service/FargateCluster/WebAppService \
  --scalable-dimension ecs:service:DesiredCount \
  --min-capacity 2 \
  --max-capacity 10

# 2. Create a Target Tracking Scaling Policy (Maintain 70% CPU)
cat <<EOF > ecs-scaling-policy.json
{
  "TargetValue": 70.0,
  "PredefinedMetricSpecification": {
    "PredefinedMetricType": "ECSServiceAverageCPUUtilization"
  },
  "ScaleOutCooldown": 60,
  "ScaleInCooldown": 60
}
EOF

# 3. Apply the Scaling Policy
awslocal application-autoscaling put-scaling-policy \
  --service-namespace ecs \
  --resource-id service/FargateCluster/WebAppService \
  --scalable-dimension ecs:service:DesiredCount \
  --policy-name ECSTargetTrackingCPU \
  --policy-type TargetTrackingScaling \
  --target-tracking-scaling-policy-configuration file://ecs-scaling-policy.json
aws application-autoscaling put-scaling-policy \
  --service-namespace ecs \
  --resource-id service/FargateCluster/WebAppService \
  --scalable-dimension ecs:service:DesiredCount \
  --policy-name ECSTargetTrackingCPU \
  --policy-type TargetTrackingScaling \
  --target-tracking-scaling-policy-configuration file://ecs-scaling-policy.json
```

## 🧠 Key Concepts & Importance

- **Application Auto Scaling:** A web service that you can use to automatically scale your AWS resources. For ECS, it allows you to automatically adjust the number of running tasks in a service.
- **Scalable Target:** The resource that you want to scale. In this lab, it's our ECS Service (`DesiredCount`).
- **Target Tracking Scaling:** A scaling policy that works like a thermostat. You specify a target value for a specific metric (e.g., 70% CPU), and the policy automatically adjusts the capacity of your scalable target to maintain that value.
- **Predefined Metrics:** AWS provides standard metrics for ECS services, such as `ECSServiceAverageCPUUtilization` and `ECSServiceAverageMemoryUtilization`.
- **Cooldown Periods:**
    - **ScaleOutCooldown:** The amount of time, in seconds, after a scale-out activity completes before another scale-out activity can start.
    - **ScaleInCooldown:** The amount of time, in seconds, after a scale-in activity completes before another scale-in activity can start.
- **Elasticity:** Ensures that your application has enough resources to handle load during peaks while minimizing costs by scaling down during troughs.

## 🛠️ Command Reference

- `application-autoscaling register-scalable-target`: Registers or updates a resource as a scalable target.
    - `--service-namespace`: The AWS service namespace (set to `ecs`).
    - `--resource-id`: The identifier of the resource (service/cluster/name).
    - `--scalable-dimension`: The dimension to scale (e.g., `ecs:service:DesiredCount`).
    - `--min-capacity`: The minimum value to scale to.
    - `--max-capacity`: The maximum value to scale to.
- `application-autoscaling put-scaling-policy`: Creates or updates a scaling policy for a scalable target.
    - `--policy-name`: A name for the policy.
    - `--policy-type`: The type of scaling policy (set to `TargetTrackingScaling`).
    - `--target-tracking-scaling-policy-configuration`: The JSON configuration for the tracking logic.

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
