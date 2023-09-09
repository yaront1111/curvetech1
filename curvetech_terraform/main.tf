provider "aws" {
  region = var.region
}


module "vpc" {
  source = "./modules/vpc"
}

module "s3" {
  source         = "./modules/s3"
  bucket_name    = "curvetechapp"
  index_document = "index.html"
  error_document = "error.html"
  tags = {
    Name = "curvetechapp"
  }
}

module "eks" {
  source        = "./modules/eks"
  cluster_name  = var.cluster_name
  subnet_ids    = concat(module.vpc.public_subnets, module.vpc.private_subnets)
}
