# CivicPulse: Azure Data Engineering Pipeline

CivicPulse is an end-to-end **Azure-based data engineering pipeline** built to ingest, transform, orchestrate, and prepare civic complaint data for analytics and reporting.

This project simulates a real-world modern data platform using **Azure Blob Storage**, **Azure Data Factory**, **PostgreSQL**, **Terraform**, and **Apache Airflow**, following a layered **Bronze → Silver → Gold** architecture.

---

## Project Overview

The goal of this project is to design and implement a cloud-native data pipeline that:

- Extracts raw civic complaint data
- Stores raw data in a **Bronze** layer
- Cleans and standardizes records into a **Silver** layer
- Aggregates curated business-ready datasets into a **Gold** layer
- Loads structured outputs into **Azure PostgreSQL**
- Supports orchestration using **Apache Airflow**
- Demonstrates infrastructure provisioning with **Terraform**

This project was built as part of my **data engineering portfolio** to showcase practical skills in cloud data pipelines, ETL/ELT workflows, orchestration, and infrastructure as code.

---

## Architecture

### Data Flow

```text
Raw Data Source
      ↓
Python Ingestion Script
      ↓
Azure Blob Storage (Bronze)
      ↓
Python Transformation Script
      ↓
Azure Blob Storage (Silver)
      ↓
Gold Aggregation Script
      ↓
Azure PostgreSQL (Gold Layer)
      ↓
Power BI / Analytics (Planned)

Architecture Diagram

Tech Stack
Cloud & Infrastructure
    Microsoft Azure
        Azure Blob Storage
        Azure Data Factory
        Azure PostgreSQL Flexible Server

Data Engineering
    Python
    Pandas
    PyArrow
    SQLAlchemy
    psycopg2
    Apache Airflow
    Terraform

Dev Tools
    Docker Desktop
    Astronomer CLI
    Git & GitHub
    VS Code

Project Structure

Civicpulse/
│
├── dags/
│   └── civicpulse_pipeline.py
│
├── data/
│   ├── extract_data.py
│   ├── transform_bronze_to_silver.py
│   ├── load_raw_data_to_bronze_layer.py
│   ├── load_transformed_bronze_to_silver_layer.py
│   └── load_transformed_silver_to_gold_layer.py
│
├── include/
│   ├── load_raw_data_to_bronze_layer.py
│   ├── transform_bronze_to_silver.py
│   ├── load_transformed_bronze_to_silver_layer.py
│   └── load_transformed_silver_to_gold_layer.py
│
├── docs/
│   ├── civicpulse.drawio
│   └── civicpulse_architecture.png
│
├── Terraform/
│   ├── main.tf
│   ├── provider.tf
│   ├── variable.tf
│   ├── terraform.tfvars.example
│   └── data_factory_blob_storage/
│
├── tests/
│
├── Dockerfile
├── airflow_settings.yaml
├── packages.txt
├── requirements.txt
└── README.md

Data Layers
Bronze Layer

The Bronze layer stores raw ingested data exactly as extracted from the source.

Purpose
    Preserve original source data
    Support traceability and reproducibility
    Serve as the initial landing zone

Storage
    Azure Blob Storage
    Container: bronze

Silver Layer

The Silver layer contains cleaned, standardized, and enriched complaint records.

Transformations Applied
    Column renaming and standardization
    Null handling
    Datetime formatting
    Complaint categorization cleanup
    Borough/location standardization
    Submission method cleanup

Storage
    Azure Blob Storage
    Container: silver
    Formats used:
        CSV
        Parquet

Gold Layer
The Gold layer contains aggregated and analytics-ready data.

Gold Outputs Include
    Complaint counts by category
    Complaint trends by borough
    Complaint summaries by date
    Curated tables prepared for reporting and BI tools
Storage
    Azure PostgreSQL
    Schema: gold

Pipeline Components
1. Data Extraction

The raw complaint data is extracted and prepared for ingestion into the Bronze layer.

Script
python data/extract_data.py

2. Load Raw Data to Bronze
Uploads raw extracted data to Azure Blob Storage Bronze container.

Script
python data/load_raw_data_to_bronze_layer.py

3. Transform Bronze to Silver
Cleans and transforms raw complaint data into structured Silver-ready output.

Script
python data/transform_bronze_to_silver.py

4. Load Silver Data to Azure Blob
Uploads transformed Silver data into Azure Blob Storage.

Script
python data/load_transformed_bronze_to_silver_layer.py

5. Load Silver / Gold Outputs to PostgreSQL
Loads transformed or aggregated outputs into Azure PostgreSQL for downstream reporting.

Script
python data/load_transformed_silver_to_gold_layer.py

Airflow Orchestration

This project includes an Apache Airflow DAG to orchestrate the ETL pipeline.

DAG
dags/civicpulse_pipeline.py

Orchestrated Tasks
Extract raw data
Load to Bronze
Transform to Silver
Upload to Silver
Transform to Gold
Load to PostgreSQL
Run Airflow Locally

If using Astronomer / Docker:
astro dev start --docker

Then open Airflow UI:
http://localhost:8080

Note: On Windows with Astronomer, your port may be mapped differently depending on Docker/Astro configuration.

Terraform Infrastructure

Infrastructure provisioning is managed using Terraform.

Resources Provisioned
Azure Resource Group
Azure Storage Account
Bronze/Silver Blob Containers
Azure Data Factory
Azure PostgreSQL Flexible Server
PostgreSQL Database
ADF datasets and linked services
Terraform Commands

Initialize Terraform:
terraform init

Validate configuration:
terraform validate

Preview infrastructure changes:
terraform plan

Apply infrastructure:
terraform apply

Environment Variables

Create a .env file in your local environment with the required secrets.

Example
AZURE_STORAGE_CONNECTION_STRING=your_storage_connection_string
DB_HOST=your_postgres_host
DB_PORT=5432
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_ADMIN_LOGIN=your_admin_login
DB_ADMIN_PASSWORD=your_admin_password

Never commit your real .env file to GitHub.

Key Learnings From This Project
Through this project, I gained practical experience in:

    Designing layered data lake architectures
    Building ETL/ELT workflows with Python
    Working with Azure Blob Storage and Azure Data Factory
    Loading analytics-ready datasets into PostgreSQL
    Using Terraform for infrastructure provisioning
    Orchestrating pipelines with Apache Airflow
    Managing schema and data mapping issues across cloud services
    Troubleshooting authentication, data format, and pipeline mapping errors

Challenges Faced
Some of the real-world challenges encountered while building this project included:
    Azure Blob Storage authentication issues
    File format mismatches between CSV and Parquet
    Data Factory schema mapping inconsistencies
    PostgreSQL schema/table alignment issues
    Git history cleanup for large Terraform provider files
    Windows-specific Docker / Astro / Airflow setup quirks

These challenges were valuable in understanding the operational realities of building production-style data pipelines.

Future Improvements
Planned enhancements include:
    Add Power BI dashboards for reporting
    Improve data quality checks
    Add logging and monitoring
    Implement incremental loads
    Add unit tests for transformation scripts
    Improve CI/CD deployment
    Deploy Airflow in Azure for production-style orchestration

Repository Description
Azure-based end-to-end data engineering pipeline using Python, Azure Blob Storage, Azure Data Factory, PostgreSQL, Terraform, and Apache Airflow with Bronze-Silver-Gold architecture.

Author

Temitope Fagbemi
Data Engineer Consultant
GitHub: https://github.com/TemitopeFagbemi

Disclaimer
This project is for educational, portfolio, and demonstration purposes.