resource "aws_ecs_service" "web_app" {
  name            = "WebAppService"
  cluster         = var.cluster_id
  task_definition = var.task_definition_arn
  desired_count   = 2
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = var.subnet_ids
    security_groups  = [var.sg_id]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = var.tg_arn
    container_name   = "nginx-container"
    container_port   = 80
  }
}
