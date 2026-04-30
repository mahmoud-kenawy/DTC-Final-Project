variable "project_id" {
  description = "The ID of the GCP project"
  type        = string
  default     = "project-af60fa76-7499-4c3a-aa2"
}

variable "region" {
  description = "The region for GCP resources"
  type        = string
  default     = "us-central1"
}

variable "bq_dataset_name" {
  description = "The name of the BigQuery Dataset"
  type        = string
  default     = "usgs_data"
}

variable "gcs_bucket_name" {
  description = "The name of the GCS Bucket"
  type        = string
  default     = "usgs-data-lake-bucket-dtc" # Recommend changing the suffix
}
