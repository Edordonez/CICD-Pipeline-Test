variable "aws_region" {
  description = "AWS region"
  default     = "us-east-1"
}

variable "raw_bucket_name" {
  description = "S3 bucket for raw data"
  default     = "healthcare-pipeline-raw-clouduser-cl"
}

variable "processed_bucket_name" {
  description = "S3 bucket for processed data"
  default     = "healthcare-pipeline-processed-clouduser-cl"
}

variable "db_username" {
  description = "RDS master username"
  default     = "postgres"
}

variable "db_password" {
  description = "RDS master password"
  sensitive   = true
}

variable "db_name" {
  description = "Database name"
  default     = "healthcare_db"
}

variable "ecr_image_uri" {
  description = "ECR image URI for ECS task"
  default     = "224776848212.dkr.ecr.us-east-1.amazonaws.com/healthcare-etl:latest"
}