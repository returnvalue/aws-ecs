# AWS Elastic Container Service (ECS) Labs (LocalStack Pro)

![AWS](https://img.shields.io/badge/AWS-ECS_Containers-FF9900?style=for-the-badge&logo=amazonaws)
![LocalStack](https://img.shields.io/badge/LocalStack-Pro-000000?style=for-the-badge)

This repository contains hands-on labs demonstrating core Amazon ECS concepts, from foundational networking and image management to task definitions, services, and high availability. Using [LocalStack Pro](https://localstack.cloud/), we simulate a complete AWS container orchestration environment locally.

## 🎯 Architecture Goals & Use Cases Covered
Based on AWS best practices (SAA-C03), these labs cover:
* **Networking Foundation:** Designing multi-AZ VPCs for container reliability.
* **IAM Security:** Implementing strict separation between Execution and Task roles.
* **Image Management:** Using Amazon ECR to securely store and version Docker images.
* **Cluster Management:** (Upcoming) Provisioning ECS clusters.
* **Task Definitions:** (Upcoming) Defining blueprints for containerized applications.
* **Service Orchestration:** (Upcoming) Maintaining desired task counts and scaling.
* **Load Balancing:** (Upcoming) Distributing traffic to containers via ALB.

## ⚙️ Prerequisites

* [Docker](https://docs.docker.com/get-docker/) & Docker Compose
* [LocalStack Pro](https://app.localstack.cloud/) account and Auth Token
* [`awslocal` CLI](https://github.com/localstack/awscli-local) (a wrapper around the AWS CLI for LocalStack)

## 🚀 Environment Setup

1. Configure your LocalStack Auth Token in `.env`:
   ```bash
   echo "YOUR_TOKEN=your_auth_token_here" > .env
   ```

2. Start LocalStack Pro:
   ```bash
   docker-compose up -d
   ```

> [!IMPORTANT]
> **Cumulative Architecture:** These labs are designed as a cumulative scenario. You are building an evolving containerized infrastructure.
>
> **Session Persistence:** These labs rely on bash variables (like `$VPC_ID`, `$TASK_SG`, `$EXEC_ROLE_ARN`, etc.). Run all commands in the same terminal session to maintain context.

## 📚 Labs Index
1. [Lab 1: Networking Foundation & ECR Registry](./labs/lab1-ecs-foundation/README.md)
2. [Lab 2: IAM Role Separation (Execution vs. Task Roles)](./labs/lab2-ecs-iam-roles/README.md)
