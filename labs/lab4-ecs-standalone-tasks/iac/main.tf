# (IaC usually manages long-running services, but we can define the blueprint)
# The CLI 'run-task' is an operational command. IaC ensures the Cluster and TD exist.
resource "aws_ecs_cluster" "main" { name = "FargateCluster" }
resource "aws_ecs_task_definition" "web_app" { family = "web-app" #... }
