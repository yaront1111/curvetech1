output "vpc_id" {
  value = module.vpc.vpc_id
}

output "public_subnets" {
  value = module.vpc.public_subnets
}

output "private_subnets" {
  value = module.vpc.private_subnets
}

output "eks_cluster_endpoint" {
  value = module.eks.eks_cluster_endpoint
}

output "s3_website_endpoint" {
  value = module.s3.website_url
}
