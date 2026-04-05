import os
import io
import requests
import pandas as pd
import boto3
from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv()

BASE_URL = "https://data.cms.gov/data-api/v1/dataset/7e0b4365-fd63-4a29-8f5e-e0ac9f66a81b/data"
STATS_URL = f"{BASE_URL}/stats"
PAGE_SIZE = 5000

# S3 bucket names
RAW_BUCKET = os.getenv("RAW_BUCKET", "healthcare-pipeline-raw-clouduser-cl")
PROCESSED_BUCKET = os.getenv("PROCESSED_BUCKET", "healthcare-pipeline-processed-clouduser-cl")

# Database config from environment variables
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "healthcare_db")

s3 = boto3.client("s3")


def get_engine():
    return create_engine(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


def get_total_rows() -> int:
    response = requests.get(STATS_URL, timeout=30)
    response.raise_for_status()
    stats = response.json()
    return int(stats["total_rows"])


def fetch_page(offset: int, size: int = PAGE_SIZE) -> list[dict]:
    params = {
        "size": size,
        "offset": offset
    }
    response = requests.get(BASE_URL, params=params, timeout=60)
    response.raise_for_status()
    return response.json()


def fetch_all_data() -> pd.DataFrame:
    total_rows = get_total_rows()
    print(f"Total rows available: {total_rows}")

    all_rows = []
    offset = 0

    while offset < total_rows:
        print(f"Fetching rows {offset} to {offset + PAGE_SIZE}")
        page = fetch_page(offset)
        if not page:
            break
        all_rows.extend(page)
        offset += PAGE_SIZE

    df = pd.DataFrame(all_rows)
    print(f"Downloaded {len(df)} rows")
    return df


def basic_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [
        col.strip().lower().replace(" ", "_")
        for col in df.columns
    ]
    df = df.drop_duplicates()
    return df


def clean_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    numeric_cols = [
        "tot_mftr",
        "tot_spndng_2019","tot_dsg_unts_2019","tot_clms_2019","tot_benes_2019",
        "avg_spnd_per_dsg_unt_wghtd_2019","avg_spnd_per_clm_2019","avg_spnd_per_bene_2019",
        "tot_spndng_2020","tot_dsg_unts_2020","tot_clms_2020","tot_benes_2020",
        "avg_spnd_per_dsg_unt_wghtd_2020","avg_spnd_per_clm_2020","avg_spnd_per_bene_2020",
        "tot_spndng_2021","tot_dsg_unts_2021","tot_clms_2021","tot_benes_2021",
        "avg_spnd_per_dsg_unt_wghtd_2021","avg_spnd_per_clm_2021","avg_spnd_per_bene_2021",
        "tot_spndng_2022","tot_dsg_unts_2022","tot_clms_2022","tot_benes_2022",
        "avg_spnd_per_dsg_unt_wghtd_2022","avg_spnd_per_clm_2022","avg_spnd_per_bene_2022",
        "tot_spndng_2023","tot_dsg_unts_2023","tot_clms_2023","tot_benes_2023",
        "avg_spnd_per_dsg_unt_wghtd_2023","avg_spnd_per_clm_2023","avg_spnd_per_bene_2023",
        "chg_avg_spnd_per_dsg_unt_22_23",
        "cagr_avg_spnd_per_dsg_unt_19_23"
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def save_to_s3(df: pd.DataFrame, bucket: str, key: str):
    """Save a DataFrame as CSV directly to S3 without writing to disk."""
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=csv_buffer.getvalue()
    )
    print(f"Saved to s3://{bucket}/{key}")


def load_to_postgres(df: pd.DataFrame):
    engine = get_engine()
    df.to_sql(
        "drug_spending_wide",
        engine,
        if_exists="replace",
        index=False
    )
    print("Loaded data into PostgreSQL table: drug_spending_wide")


def main():
    df_raw = fetch_all_data()

    df_clean = basic_cleaning(df_raw)
    df_clean = clean_numeric_columns(df_clean)

    print("\nColumns:")
    print(df_clean.columns.tolist())

    print("\nPreview:")
    print(df_clean.head())

    # Save to S3
    save_to_s3(df_raw, RAW_BUCKET, "cms_part_d_raw.csv")
    save_to_s3(df_clean, PROCESSED_BUCKET, "cms_part_d_clean.csv")

    # Load to RDS
    load_to_postgres(df_clean)


if __name__ == "__main__":