import great_expectations as gx
import duckdb


# =========================================================
# Configuration
# =========================================================

GX_ROOT = "/usr/local/airflow/include/gx"

DUCKDB_FILE = (
    "/usr/local/airflow/include/data/northwind.duckdb"
)

DATASOURCE_NAME = "northwind_pandas"
ASSET_NAME = "raw_orders_dataframe"
BATCH_DEFINITION_NAME = "raw_orders_batch"
SUITE_NAME = "raw_orders_suite"


def main():
    # =========================================================
    # 1. Load data from DuckDB Bronze into Pandas
    # =========================================================

    print("Reading bronze.raw_orders from DuckDB...")

    conn = duckdb.connect(DUCKDB_FILE)

    try:
        df = conn.execute(
            """
            SELECT *
            FROM bronze.raw_orders
            """
        ).fetchdf()

    finally:
        conn.close()

    print(
        f"Loaded {len(df)} rows from bronze.raw_orders."
    )

    # =========================================================
    # 2. Create / Load GX Context
    # =========================================================

    context = gx.get_context(
        mode="file",
        context_root_dir=GX_ROOT
    )

    print("GX context loaded.")

    # =========================================================
    # 3. Get Pandas Data Source
    # =========================================================

    datasource = context.data_sources.get(
        DATASOURCE_NAME
    )

    # =========================================================
    # 4. Get DataFrame Asset
    # =========================================================

    data_asset = datasource.get_asset(
        ASSET_NAME
    )

    # =========================================================
    # 5. Get Batch Definition
    # =========================================================

    batch_definition = data_asset.get_batch_definition(
        BATCH_DEFINITION_NAME
    )

    # =========================================================
    # 6. Create Batch using the runtime DataFrame
    # =========================================================

    batch = batch_definition.get_batch(
        batch_parameters={
            "dataframe": df
        }
    )

    # =========================================================
    # 7. Get Expectation Suite
    # =========================================================

    suite = context.suites.get(
        SUITE_NAME
    )

    # =========================================================
    # 8. Validate
    # =========================================================

    print("\nRunning Great Expectations validation...")

    validation_result = batch.validate(
        suite
    )

    print("\n==============================================")
    print(
        "Validation successful:",
        validation_result.success
    )
    print("==============================================\n")

    # =========================================================
    # 9. Stop pipeline if validation fails
    # =========================================================

    if not validation_result.success:
        print(validation_result)

        raise RuntimeError(
            "Great Expectations validation failed."
        )

    print(
        "Great Expectations validation passed."
    )


if __name__ == "__main__":
    main()
