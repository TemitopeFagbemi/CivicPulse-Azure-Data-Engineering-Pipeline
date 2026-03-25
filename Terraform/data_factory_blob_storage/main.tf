resource "azurerm_data_factory_dataset_delimited_text" "helpline_csv_dataset" {
  name                = "helplinedataset"
  data_factory_id     = var.data_factory_id
  linked_service_name = var.linked_service_name

  column_delimiter    = ","
  row_delimiter       = "\n"
  encoding            = "UTF-8"
  quote_character     = "\""
  escape_character    = "\\"
  first_row_as_header = true
  null_value          = "null"

  azure_blob_storage_location {
    container = "silver"
    filename  = "silver_civicpulse_data.csv"
  }
}

resource "azurerm_data_factory_dataset_parquet" "helpline_parquet_dataset" {
  name                = "helpline_parquetdataset"
  data_factory_id     = var.data_factory_id
  linked_service_name = var.linked_service_name

  compression_codec = "snappy"

  azure_blob_storage_location {
    container = "silver"
    filename  = "silver_civicpulse_data.parquet"
  }
}