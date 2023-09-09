variable "bucket_name" {
  description = "The name of the bucket"
  type        = string
}

variable "index_document" {
  description = "Default index document for the static website"
  type        = string
  default     = "index.html"
}

variable "error_document" {
  description = "Default error document for the static website"
  type        = string
  default     = "error.html"
}

variable "tags" {
  description = "Tags to assign to the bucket"
  type        = map(string)
  default     = {}
}
