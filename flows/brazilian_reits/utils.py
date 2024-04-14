

def create_bigquery_table(table_id, overwrite=True) -> None:
    """
    Creates a BigQuery table with external Parquet data source.

    Args:
    table_id (str): The identifier of the table to be created in BigQuery.
    overwrite (bool, optional): If True, the existing table with the same `table_id` will be overwritten.
                                If False and the table already exists, the function does nothing. Default is True.
    """    
    from google.cloud import bigquery
    source_uris = [
        f"gs://brazilian-reits-bucket/br_cvm_fii/{table_id}/*"
    ]
    bq_table_id = f"arthur-data-engineering-course.brazilian_reits_staging.{table_id}_staging"
    client = bigquery.Client()
    if overwrite:
        client.delete_table(bq_table_id, not_found_ok=True)  # Make an API request.
        print("Deleted table '{}'.".format(bq_table_id))
    external_source_format = "PARQUET"

    external_config = bigquery.ExternalConfig(external_source_format)
    hive_partitioning = bigquery.HivePartitioningOptions()
    hive_partitioning.mode = "AUTO"
    hive_partitioning.source_uri_prefix = f"gs://brazilian-reits-bucket/br_cvm_fii/{table_id}/"
    external_config.source_uris = source_uris
    external_config.hive_partitioning = hive_partitioning
    table = bigquery.Table(bq_table_id)
    table.external_data_configuration = external_config
    table = client.create_table(table)  
    print(
        f"Created table with external source format {table.external_data_configuration.source_format}"
    )
