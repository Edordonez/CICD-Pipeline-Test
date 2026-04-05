output "ecr_repository_url" {
  description = "ECR repository URL"
  value       = aws_ecr_repository.healthcare_etl.repository_url
}

output "ecs_cluster_name" {
  description = "ECS cluster name"
  value       = aws_ecs_cluster.main.name
}

output "raw_bucket_name" {
  description = "Raw S3 bucket name"
  value       = aws_s3_bucket.raw.bucket
}

output "processed_bucket_name" {
  description = "Processed S3 bucket name"
  value       = aws_s3_bucket.processed.bucket
}