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
