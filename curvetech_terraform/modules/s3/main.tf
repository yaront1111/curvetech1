# Create the S3 bucket
resource "aws_s3_bucket" "static_html" {
  bucket = var.bucket_name

  tags = var.tags
}

# Configure the website for the S3 bucket
resource "aws_s3_bucket_website_configuration" "static_html" {
  bucket = aws_s3_bucket.static_html.id

  index_document {
    suffix = var.index_document
  }

  error_document {
    key = var.error_document
  }
}
