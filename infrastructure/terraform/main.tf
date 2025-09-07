terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Create buckets for all environments
resource "google_storage_bucket" "buckets" {
  for_each = toset(var.environments)

  name     = "cicd-demo-${each.key}-eu-west2-001"
  location = "EUROPE-WEST2"

  versioning {
    enabled = true
  }

  uniform_bucket_level_access = true

  # PROD bucket retention
  retention_policy {
    count           = each.key == "prod" ? 1 : 0
    retention_period = var.prod_retention_days * 86400  # convert days to seconds
  }

  # Optional: lifecycle for DEV temp folder
  lifecycle_rule {
    count = each.key == "dev" ? 1 : 0
    action {
      type = "Delete"
    }
    condition {
      age            = 30
      matches_prefix = ["temp/"]
    }
  }
}

# Create folder placeholders in each bucket
resource "google_storage_bucket_object" "folders" {
  for_each = {for env in var.environments : env => var.folders}

  dynamic "folder" {
    for_each = each.value
    content {
      name   = "${folder.value}/.keep"
      bucket = google_storage_bucket.buckets[each.key].name
      source = "empty.txt"
    }
  }
}
