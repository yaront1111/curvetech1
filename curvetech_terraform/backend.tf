terraform {
  backend "s3" {
    bucket = "curvetech-yaron"
    key = "terraform/curve/dev.tfstate"
    region = "eu-west-1"
    # dynamodb_table = "mytable"
  }
}