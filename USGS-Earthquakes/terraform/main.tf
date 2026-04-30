terraform {
  required_version = ">= 1.0"
  backend "local" {}  # Can change to "gcs" for production
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

# Data Lake Bucket
resource "google_storage_bucket" "data_lake_bucket" {
  name                        = var.gcs_bucket_name
  location                    = var.region
  force_destroy               = true
  uniform_bucket_level_access = true

  lifecycle_rule {
    condition {
      age = 30 # Delete after 30 days
    }
    action {
      type = "Delete"
    }
  }
}

# BigQuery Dataset
resource "google_bigquery_dataset" "usgs_dataset" {
  dataset_id                 = var.bq_dataset_name
  location                   = var.region
  delete_contents_on_destroy = true
}

# Auto-created via Spark but we can enforce table creation here or let Spark do it. 
# Spark structured streaming will create the table automatically with BigQuery connector.
