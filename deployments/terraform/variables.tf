variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "AWS region for deployment"
}

variable "environment" {
  type        = string
  default     = "staging"
  description = "Environment name (staging, prod)"
}

variable "db_name" {
  type        = string
  default     = "graphoath"
  description = "PostgreSQL database name"
}

variable "db_username" {
  type        = string
  default     = "graphoath_admin"
  description = "PostgreSQL admin username"
}

variable "db_password" {
  type        = string
  sensitive   = true
  description = "PostgreSQL admin password"
}

variable "db_instance_class" {
  type        = string
  default     = "db.t4g.micro"
  description = "RDS instance class"
}
