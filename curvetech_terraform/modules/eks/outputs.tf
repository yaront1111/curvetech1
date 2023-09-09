output "eks_cluster_name" {
  value = aws_eks_cluster.this.name
  description = "The name of the EKS cluster."
}

output "eks_cluster_endpoint" {
  value = aws_eks_cluster.this.endpoint
  description = "The endpoint for the EKS cluster."
}

output "eks_cluster_arn" {
  value = aws_eks_cluster.this.arn
  description = "The ARN of the EKS cluster."
}

output "eks_cluster_version" {
  value = aws_eks_cluster.this.version
  description = "The Kubernetes version of the EKS cluster."
}

output "microservices_node_group_arn" {
  value = aws_eks_node_group.microservices.arn
  description = "The ARN of the microservices node group."
}

output "internal_services_node_group_arn" {
  value = aws_eks_node_group.internal_services.arn
  description = "The ARN of the internal services node group."
}

output "cluster_name" {
  value = aws_eks_cluster.this.name
  description = "The name of the cluster"
}