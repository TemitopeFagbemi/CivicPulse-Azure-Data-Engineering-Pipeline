# Create a resource group
resource "azurerm_resource_group" "helpline_projectrg" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_storage_account" "helplinestorageaccount" {
  name                     = var.storage_account_name
  resource_group_name      = azurerm_resource_group.helpline_projectrg.name
  location                 = azurerm_resource_group.helpline_projectrg.location
  account_tier             = "Standard"
  account_replication_type = "GRS"

  tags = {
    environment = "staging"
  }
}

resource "azurerm_storage_container" "raw_data" {
  name                  = "bronze"
  storage_account_name  = azurerm_storage_account.helplinestorageaccount.name
  container_access_type = "private"
}

resource "azurerm_storage_container" "transformed_data" {
  name                  = "silver"
  storage_account_name  = azurerm_storage_account.helplinestorageaccount.name
  container_access_type = "private"

  depends_on = [azurerm_storage_account.helplinestorageaccount]
}

# create a PostgreSQL flexible server
resource "azurerm_postgresql_flexible_server" "pgsflex" {
  name                          = var.postgresql_server_name
  resource_group_name           = var.resource_group_name
  location                      = var.location
  version                       = "16"
  public_network_access_enabled = true
  administrator_login           = var.db_admin_login
  administrator_password        = var.db_admin_password
  zone                          = "1"

  storage_mb   = 32768
  storage_tier = "P30"

  sku_name    = "GP_Standard_D4s_v3"
  create_mode = "Default"

  authentication {
    password_auth_enabled = true
  }

  depends_on = [azurerm_resource_group.helpline_projectrg]
}

resource "azurerm_postgresql_flexible_server_database" "pgserver_db" {
  name      = "pgserver_db"
  server_id = azurerm_postgresql_flexible_server.pgsflex.id
  collation = "en_US.utf8"
  charset   = "UTF8"

  # prevent the possibility of accidental data loss
  lifecycle {
    prevent_destroy = false
  }
}

resource "azurerm_data_factory" "helpline_data_factory" {
  name                = "helpline-data-factory"
  location            = azurerm_resource_group.helpline_projectrg.location
  resource_group_name = azurerm_resource_group.helpline_projectrg.name
}

resource "azurerm_data_factory_linked_service_azure_blob_storage" "helpline_blob_linked_service" {
  name              = "helpline-blob-linked-service"
  data_factory_id   = azurerm_data_factory.helpline_data_factory.id
  connection_string = azurerm_storage_account.helplinestorageaccount.primary_connection_string
}

module "data_factory_blob_storage" {
  source              = "./data_factory_blob_storage"
  data_factory_id     = azurerm_data_factory.helpline_data_factory.id
  linked_service_name = azurerm_data_factory_linked_service_azure_blob_storage.helpline_blob_linked_service.name
}