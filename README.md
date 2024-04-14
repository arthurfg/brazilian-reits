# Brazilian Real Estate Investment Funds (REIT's) Data Pipeline

This project establishes an end-to-end data pipeline utilizing Prefect, Google Cloud Storage (GCS), Google Cloud Run, BigQuery, and dbt. The pipeline extracts data from the Brazilian Securities and Exchange Commission (CVM) regarding Real Estate Investment Funds (REITs) in Brazil.

## Overview

The primary objective of this project is to automate the extraction, transformation, and loading (ETL) process of REIT data from the CVM database into a structured format for further analysis and visualization.

## Components

1. **Prefect**: Prefect is employed as the workflow orchestrator to manage and execute the various stages of the data pipeline. It ensures reliability, monitoring, and scheduling of tasks.
   
2. **Google Cloud Storage (GCS)**: GCS serves as the storage solution for raw and processed data. It enables seamless data transfer between different stages of the pipeline and provides durability and scalability.
   
3. **Google Cloud Run**: Google Cloud Run hosts the data processing tasks, providing a serverless environment for executing containerized applications. It offers scalability and cost-efficiency, handling tasks on-demand.
   
4. **BigQuery**: BigQuery acts as the data warehouse for storing the processed data. It offers powerful querying capabilities, real-time analytics, and seamless integration with other Google Cloud services.
   
5. **dbt (data build tool)**: dbt is utilized for data modeling and transformation. It enables the creation of structured datasets and facilitates the generation of insights from the raw data.

## Workflow

1. **Data Extraction**: Data is extracted from the CVM database using appropriate APIs or web scraping techniques. The extracted data is stored in GCS in its raw format.
   
2. **Data Transformation**: Data preprocessing and cleaning tasks are performed using containerized applications hosted on Google Cloud Run. This stage involves standardizing data formats, handling missing values, and ensuring data quality.
   
3. **Data Loading**: Processed data is loaded into BigQuery tables, organized in a schema suitable for analysis. dbt may be employed here to further refine the data model and create derived datasets.
   
4. **Dashboard Creation**: Finally, the transformed data is utilized to create interactive dashboards for visualizing key insights and performance metrics of REITs in Brazil. Tools like Data Studio or Looker can be integrated for dashboard creation.

## Benefits

- **Automation**: The pipeline automates the entire ETL process, reducing manual effort and minimizing errors.
- **Scalability**: Leveraging cloud-native services ensures scalability to handle large volumes of data efficiently.
- **Real-time Analysis**: The pipeline enables real-time analysis of REIT data, allowing stakeholders to make timely decisions.
- **Data-driven Insights**: By visualizing data through dashboards, stakeholders gain valuable insights into the performance and trends of REITs in Brazil.

