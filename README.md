\# Healthcare Cloud Data Pipeline



An end-to-end cloud data pipeline that extracts Medicare Part D drug spending 

data from the CMS API, transforms it, and loads it into AWS cloud infrastructure 

— fully automated with CI/CD.



\## Architecture

CMS API → Python ETL → Docker Container → AWS ECS Fargate

→ S3 Data Lake → RDS PostgreSQL → Power BI Dashboard



\## Tech Stack



\- \*\*Python\*\* — ETL pipeline (pandas, boto3, SQLAlchemy)

\- \*\*Docker\*\* — containerization

\- \*\*AWS S3\*\* — data lake (raw and processed data)

\- \*\*AWS ECR\*\* — container registry

\- \*\*AWS RDS PostgreSQL\*\* — structured data storage

\- \*\*AWS ECS Fargate\*\* — serverless container execution

\- \*\*AWS CloudWatch\*\* — logging and monitoring

\- \*\*AWS IAM\*\* — security and access management

\- \*\*Terraform\*\* — infrastructure as code

\- \*\*GitHub Actions\*\* — CI/CD pipeline



\## Project Structure

├── ETL.py                      # Main ETL pipeline script

├── Dockerfile                  # Container definition

├── requirements.txt            # Python dependencies

├── terraform/

│   ├── main.tf                 # Core AWS resources

│   ├── variables.tf            # Input variables

│   ├── outputs.tf              # Output values

│   └── iam.tf                  # IAM roles and policies

└── .github/

└── workflows/

└── deploy.yml          # CI/CD pipeline



\## Pipeline Overview



\### Phase 1 — Extract

\- Fetches 14,000+ Medicare Part D drug spending records from CMS API

\- Handles pagination (5,000 records per page)

\- Covers spending data from 2019-2023



\### Phase 2 — Transform

\- Cleans column names and removes duplicates

\- Converts numeric fields to proper data types

\- Produces raw and cleaned datasets



\### Phase 3 — Load

\- Saves raw CSV to S3 data lake

\- Saves processed CSV to S3 data lake

\- Loads structured data into PostgreSQL RDS



\## Infrastructure (Terraform)



All AWS infrastructure is defined as code and can be reproduced with:

```bash

terraform init

terraform apply

```



Resources provisioned:

\- S3 buckets (raw and processed)

\- ECR repository

\- ECS cluster

\- IAM roles and policies



\## CI/CD Pipeline (GitHub Actions)



Every push to `main` branch automatically:

1\. Builds Docker image

2\. Pushes image to AWS ECR

3\. Updates ECS task definition

4\. Runs ETL pipeline on ECS Fargate



\## Setup



\### Prerequisites

\- AWS account with appropriate permissions

\- Docker Desktop

\- Terraform

\- AWS CLI configured



\### Environment Variables

DB\_HOST=your-rds-endpoint

DB\_USER=postgres

DB\_PASSWORD=your-password

DB\_NAME=healthcare\_db

RAW\_BUCKET=your-raw-bucket

PROCESSED\_BUCKET=your-processed-bucket



\### Deploy Infrastructure

```bash

cd terraform

terraform init

terraform apply

```



\### Run Locally

```bash

docker build -t healthcare-etl .

docker run --env-file .env healthcare-etl

```



\## Data Source



CMS Medicare Part D Spending by Drug dataset — public data from the Centers 

for Medicare and Medicaid Services covering drug spending patterns across 

14,000+ drugs from 2019-2023.



https://data.cms.gov/summary-statistics-on-use-and-payments/medicare-medicaid-spending-by-drug/medicare-part-d-spending-by-drug

