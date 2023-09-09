variable "region" {
  description = "AWS region"
  default     = "eu-west-1"
}

variable "cluster_name" {
  description = "Name of the EKS cluster"
  default     = "curve-tech-cluster"
}

variable "website_name" {
  description = "Name of the S3 bucket for the static website"
  default     = "curve-tech-website"
}
