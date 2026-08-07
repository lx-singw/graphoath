terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_db_instance" "graphoath_db" {
  allocated_storage    = 20
  max_allocated_storage = 100
  db_name              = var.db_name
  engine               = "postgres"
  engine_version       = "16"
  instance_class       = var.db_instance_class
  username             = var.db_username
  password             = var.db_password
  skip_final_snapshot  = true
}

resource "aws_ecs_cluster" "graphoath_cluster" {
  name = "${var.environment}-graphoath-cluster"
}
