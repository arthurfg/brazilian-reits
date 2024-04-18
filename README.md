# Brazilian Real Estate Investment Trusts (REIT's) Data Pipeline

### Challenge
Although the Comissão de Valores Mobiliarios (CVM), the regulatory body responsible for the capital markets in Brazil, provides data on Real Estate Investment Trusts (FII/REITS) in a relatively organized structure on its [open data portal](https://dados.cvm.gov.br/dataset/fii-doc-inf_mensal), accessibility and speed in acquiring new data are still significant obstacles. The availability of tables in .csv format, compressed into .zip files, does not meet today's needs for interactivity and practicality. Tracking the net assets of a specific real estate fund over the months requires the user to manually download all the .zip files and proceed to read and merge all the .csv's for analysis, a process that proves to be inefficient and unfriendly.


## Objective
This project aims to overcome these barriers and, at the same time, achieve the last milestone (the final project) of DataTalksClub's Data Engineering course. The project establishes a complete data pipeline, which starts with the collection of the original data, transforms it into a more modern and open source format, stores the converted and partitioned data on an object storage platform in the cloud (along with the raw data in .csv) and, from these files, creates the tables needed for the final product: an interactive dashboard that offers access to detailed information about one or more REITs, providing an agile and intuitive user experience.

## Overview

This project is based on the Monthly Structured REIT Reports, periodic electronic documents sent by real estate fund managers to the regulator, containing comprehensive data on REITs. The data set is organized in a directory, with each year represented by a .zip file that encapsulates three distinct tables: asset_passive, complement and general.

The layout of the directory is as follows:

```bash
Portal_Dados_Abertos_CVM
├── inf_mensal_fii_2016.zip (57K)
├── inf_mensal_fii_2017.zip (407K)
├── inf_mensal_fii_2018.zip (469K)
├── inf_mensal_fii_2019.zip (553K)
├── inf_mensal_fii_2020.zip (684K)
├── inf_mensal_fii_2021.zip (846K)
├── inf_mensal_fii_2022.zip (1008K)
├── inf_mensal_fii_2023.zip (1M)
└── inf_mensal_fii_2024.zip (294K)

```

Within each .zip, the data is structured into three tables:

```bash
├── inf_mensal_fii_2023.zip (1M)
│   ├── inf_mensal_fii_ativo_passivo_2023.csv (2,3 MB)
│   ├── inf_mensal_fii_complemento_2023.csv (1,6 MB)
│   └── inf_mensal_fii_geral_2023.csv (4,1 MB)
```

To make it easier to access and analyze this data, we have developed a pipeline that automates the download and extraction of .zip files, the reading and cleaning of .csv files, and the conversion of these files to the .parquet format, which is more efficient for storage and consultation. In addition, the pipeline manages the transfer of both raw and staged files to the project bucket (brazilian-reits-bucket).

The pipeline is also responsible for creating the staging tables from the .parquet data stored in the bucket and executing the dbt models located in `queries/models/brazilian_reits`, ensuring that the final tables needed for the project dashboard are materialized.

In short, the deployment was registered to run every day at 4pm (America/Chicago time). The flow checks whether there have been any updates to the available data and, if so, the files are downloaded, decompressed, transformed into parquet, uploaded to the GCS (both the parquet data and the raw data) and, from the bucket, the staging tables are created.

## Infrastructure

The tools used to carry out the project were these:

1. **Prefect**: Orchestrationn
   
2. **Google Cloud Storage (GCS)**: Data Lake
   
3. **Google Cloud Run**: Serverless task's runner
   
4. **BigQuery**: Data Warehouse
   
5. **dbt (data build tool)**: Transformation/Batch processing

6. **GH Actions**: CI/CD

7. **IAC**: Terraform
   
8. **Looker Studio**: Dashboard




The structuring of Prefect's orchestration and execution environments in this project is based on two fundamental parts of the Prefect "ecosystem": work pools and workers. According to the official Prefect documentation:


> It's helpful to think of work pools as a way to coordinate (potentially many) deployments with (potentially many) workers through a known channel: the pool itself. This is similar to how "topics" are used to connect producers and consumers in a > pub/sub or message-based system. By switching a deployment's work pool, users can quickly change the worker that will execute their runs, making it easy to promote runs through environments or even debug locally.


In short, the work pool sets up the "house" for the flow execution. When a deployment creates a run, that run enters the work pool queue for scheduling and then the worker running in the execution environment receives the scheduled flow and executes it.

In this project, the Prefect environment is entirely based on Google Cloud Run. The work pool schedules the flow, which is containerized in a Docker image hosted on the Google Artifact Registry, from the deployment created and configured via the `prefect.yml` file. At runtime, the worker "pulls" the work pool and executes the flow as a Cloud Run Job. This approach represented the MVP (Minimum Viable Product) found to execute the flows in the cloud in a cost-effective way and with less complexity, thanks to the serverless infrastructure provided by Cloud Run.

The underlying data infrastructure, including buckets and datasets, was  designed and implemented using Terraform. Terraform is an infrastructure-as-code tool that allows infrastructure resources to be created and managed efficiently and reproducibly.

Data processing is carried out with the help of DBT (Data Build Tool), a data building tool that has gained great prominence in the market for its ability to transform and version data efficiently and collaboratively.

To ensure that the data pipeline is always up to date and working as expected, a CI/CD treadmill was established using GitHub Actions. The `prefect-deploy.yml` action is triggered automatically with each push to the `main` branch, triggering a series of steps that guarantee the integrity and continuity of the pipeline.

Specifically, this action performs the following tasks:

1. **Docker Image Build:** The Docker image containing `brazilian-reits-flow` is built from the most recent source files.

2. **Deployment creation in Prefect:** The deployment in Prefect is created based on the newly built image, ensuring that the flow is up-to-date and ready to run.

3. **Upload to Google Artifact Registry:** The Docker image, now containing the updated flow, is automatically uploaded to the Google Artifact Registry, an artifact management system for developers and teams using Google Cloud Platform.

This automation ensures that the `brazilian-reits-flow` is always available and operational, minimizing the risk of human error and speeding up the deployment process, which is crucial for an agile and reliable operation.
### Diagram
![diagram-export-16-04-2024-19_20_38](https://github.com/arthurfg/brazilian-reits/assets/62671380/c0e53943-8756-4ae9-9ebf-a681d6f8e1e8)

## Workflow

1. **Data Extraction**: Data is extracted from the CVM open data using python. The extracted data is stored in GCS in its raw and staging format.
   
2. **Data Loading**: Data is loaded into staging BigQuery tables. 

 - Staging dataset and tables:
```bash
Google BigQuery
├── brazilian_reits_staging
│   ├── ativo_passivo_staging
│   ├── complemento_staging
│   └── geral_staging
```

3. **Data Transformation**: Dbt is used to query staging tables and make processing and cleaning tasks using containerized applications hosted on Google Cloud Run, creatind the _trusted_ tables in `brazilia_reits` dataset.

 - Trusted dataset, partitionated and clustered tables:
```bash
Google BigQuery
├── brazilian_reits
│   ├── ativo_passivo
│   ├── complemento
│   └── geral
```
   
4. **Dashboard Creation**: Finally, the transformed data is utilized to create interactive dashboards for visualizing key insights and performance metrics of REITs in Brazil. 

## Dashboard

### [**Link**](https://lookerstudio.google.com/embed/reporting/b97f7247-c3de-4927-b021-a3fe74d671d2/page/1M)
![Captura de Tela 2024-04-15 às 13 28 42](https://github.com/arthurfg/brazilian-reits/assets/62671380/75b8edfa-edeb-4649-af31-da2a124b2319)


# Running the pipeline locally
Make shure you have these requirements on your local machine:
- Terraform
- Docker Desktop
- Google Cloud SDK
- GCP service account with required permissions for terraform development
- GCP service account with required permissions for dbt|storage|bigquery
  
### Steps
1. Clone this repository:
```bash
git clone https://github.com/arthurfg/brazilian-reits.git
```

2. Go to the repo:
```bash
cd </path/to/repo>
```

3. Copy the `.env.example` file to a new file named `.env`:
```bash
cp .env.example .env
```
Replace the values of the variables with their respective values and load the environment variables from the `.env` file:
```bash
source .env
```

4. Go to terraform directory:
```bash
cd terraform
```

5. Run the terraform commands:
```bash
terraform plan
```
```bash
terraform apply
```

6. Create a `./dbt-service-account.json` file and paste your dbt|storage|bigquery service account content (it's on .gitignore, sorry for this):
```bash
cd ..
touch dbt-service-account.json
```

7. Build the Docker image:
```bash
docker build -t brazilian-reits-image .
```

8. Run the Docker image:
```bash
docker run brazilian-reits-image
```
