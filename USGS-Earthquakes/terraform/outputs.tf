output "gcs_bucket_name" {
  value = google_storage_bucket.data_lake_bucket.name
}

output "bigquery_dataset_id" {
  value = google_bigquery_dataset.usgs_dataset.dataset_id
}
