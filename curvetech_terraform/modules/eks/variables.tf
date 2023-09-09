variable "cluster_name" {
  description = "The name of the EKS cluster"
  type        = string
}

variable "subnet_ids" {
  description = "The subnet IDs for the EKS cluster and worker nodes"
  type        = list(string)
}

variable "microservices_desired_capacity" {
  description = "The desired capacity for the microservices node group"
  type        = number
  default     = 1
}

variable "microservices_max_size" {
  description = "The maximum size for the microservices node group"
  type        = number
  default     = 2
}

variable "microservices_min_size" {
  description = "The minimum size for the microservices node group"
  type        = number
  default     = 1
}

variable "internal_services_desired_capacity" {
  description = "The desired capacity for the internal services node group"
  type        = number
  default     = 1
}

variable "internal_services_max_size" {
  description = "The maximum size for the internal services node group"
  type        = number
  default     = 2
}

variable "internal_services_min_size" {
  description = "The minimum size for the internal services node group"
  type        = number
  default     = 1
}
