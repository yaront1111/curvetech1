output "website_url" {
  value = aws_s3_bucket.static_html.bucket_domain_name
}