variable "credentials" {
  description = "My credentials"
  default     = "/Users/apple/Documents/data-engineering-course/week_1_basics_n_setup/terraform/keys/my-creds.json"
}

variable "project" {
  description = "Project"
  default     = "arthur-data-engineering-course"
}

variable "location" {
  description = "Project location"
  default     = "US"
}

variable "bq_dataset_name" {
  description = "My bq dataset name"
  default     = "course_dataset"
}

variable "gcs_storage_class" {
  description = "Bucket storage class"
  default     = "STANDARD"
}

variable "gcs_bucket_name" {
  description = "My storage bucket name"
  default     = "arthur-data-engineering-course-terra-bucket"
}