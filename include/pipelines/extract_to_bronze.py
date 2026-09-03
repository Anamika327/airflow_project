import os
import sys
import requests
import pandas as pd
import duckdb
from datetime import datetime

# Astro container absolute path to your dbt project folder
DB_FILE = "/usr/local/airflow/include/dbt_project/northwind.duckdb"

def extract_and_load_endpoint(endpoint_name):
    """
    Extracts data from the public Northwind API and streams it into the local DuckDB [Bronze Layer]
    """
    API_URL = f"https://northwind.vercel.app/api/{endpoint_name}"
    print(f"[{datetime.now()}] Starting extraction for endpoint: '{endpoint_name}'")
    print(f"[{datetime.now()}] Requesting data from: {API_URL}")
    
    try:
        response = requests.get(API_URL, timeout=30)
        
        # 1. SDET Quality Check: Verify API network layer integrity
        if response.status_code != 200:
            raise RuntimeError(f"API extraction failed for '{endpoint_name}'. HTTP Status Code: {response.status_code}")
            
        data = response.json()
        
        # 2. SDET Quality Check: Verify payload is not empty or malformed
        if not data:
            print(f"⚠️ Warning: Endpoint '{endpoint_name}' returned a successful HTTP 200 but payload was empty.")
            return
            
        print(f"[{datetime.now()}] Successfully fetched {len(data)} raw records.")

        # 3. Data Transformation Layer: Convert raw JSON to a structured Pandas DataFrame
        df = pd.DataFrame(data)
        
        # 4. DataOps Metadata Injection: Tag the ingestion timeline (Crucial for Medallion tracking)
        df['ingested_at'] = datetime.utcnow()
        
        # 5. Database Connectivity Layer: Establish isolated DuckDB workspace session
        # Ensure the directory path exists before creating the database file
        os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
        conn = duckdb.connect(DB_FILE)
        
        # Enforce Bronze standard logical schemas
        conn.execute("CREATE SCHEMA IF NOT EXISTS bronze;")
        
        # Register the local memory dataframe view to pass directly to DuckDB engine
        table_name = f"bronze.raw_{endpoint_name}"
        conn.register('df_view', df)
        
        # Write/Overwrite the table to act as our pristine Raw Landing Zone
        conn.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM df_view")
        
        print(f"Success: Populated raw datasets into DuckDB table: '{table_name}'\n")
        
    except requests.exceptions.RequestException as req_err:
        print(f"Network/API Error encountered during extraction layer of '{endpoint_name}': {str(req_err)}")
        raise req_err
    except Exception as e:
        print(f"General System Failure processing pipeline task for '{endpoint_name}': {str(e)}")
        raise e
    finally:
        # Guarantee resources are safely disposed of if connection was built
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    # Core target business objects needed to build out a complete transactional star schema
    target_endpoints = ["orders", "customers", "products", "suppliers", "categories"]
    
    print("==================================================================")
    print(f"INGESTION STARTING AT: {datetime.now()}")
    print(f"TARGET STORE: {DB_FILE}")
    print("==================================================================\n")
    
    for endpoint in target_endpoints:
        try:
            extract_and_load_endpoint(endpoint)
        except Exception as abort_pipeline:
            print(f"Critical Pipeline Interruption: Execution stopped due to failure on '{endpoint}'.")
            sys.exit(1)
            
    print("==================================================================")
    print("   BRONZE DATA EXTRACTION COMPLETE FOR ALL ENDPOINTS")
    print("==================================================================")
