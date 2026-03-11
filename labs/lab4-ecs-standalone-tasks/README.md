# Lab 4: Running Standalone Tasks (Fargate)

**Goal:** Execute a one-off, serverless task. This pattern is ideal for batch jobs, database migrations, or scheduled cron jobs.

```bash
# Run a standalone task directly into our VPC
awslocal ecs run-task \
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
