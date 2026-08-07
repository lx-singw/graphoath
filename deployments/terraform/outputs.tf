output "db_endpoint" {
  value       = aws_db_instance.graphoath_db.endpoint
  description = "PostgreSQL RDS connection endpoint"
}

output "ecs_cluster_name" {
  value       = aws_ecs_cluster.graphoath_cluster.name
  description = "ECS cluster name"
}
