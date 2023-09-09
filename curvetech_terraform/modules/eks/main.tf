resource "aws_eks_cluster" "this" {
  name     = var.cluster_name
  role_arn = aws_iam_role.eks_cluster.arn

  vpc_config {
    subnet_ids = var.subnet_ids
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_cluster,
  ]
}

resource "aws_iam_role" "eks_cluster" {
  name = "eks-cluster-${var.cluster_name}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "eks.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "eks_cluster" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.eks_cluster.name
}

resource "aws_eks_node_group" "microservices" {
  cluster_name    = aws_eks_cluster.this.name
  node_group_name = "microservices-node-group"
  node_role_arn   = aws_iam_role.eks_worker.arn
  subnet_ids      = var.subnet_ids
  instance_types = ["t3.small"]

  scaling_config {
    desired_size = var.microservices_desired_capacity
    max_size     = var.microservices_max_size
    min_size     = var.microservices_min_size
  }

  depends_on = [aws_iam_role_policy_attachment.eks_worker_node_policy, aws_iam_role_policy_attachment.eks_ecr_policy]
}

resource "aws_eks_node_group" "internal_services" {
  cluster_name    = aws_eks_cluster.this.name
  node_group_name = "internal-services-node-group"
  node_role_arn   = aws_iam_role.eks_worker.arn
  subnet_ids      = var.subnet_ids
  instance_types = ["t3.small"]

  scaling_config {
    desired_size = var.internal_services_desired_capacity
    max_size     = var.internal_services_max_size
    min_size     = var.internal_services_min_size
  }

  depends_on = [aws_iam_role_policy_attachment.eks_worker_node_policy, aws_iam_role_policy_attachment.eks_ecr_policy]
}

resource "aws_iam_role" "eks_worker" {
  name = "eks-worker-nodes-${var.cluster_name}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "eks_worker_node_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.eks_worker.name
}

resource "aws_iam_role_policy_attachment" "eks_ecr_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.eks_worker.name
}
