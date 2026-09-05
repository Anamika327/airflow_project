import great_expectations as gx


GX_ROOT = "/usr/local/airflow/include/gx"

DATASOURCE_NAME = "northwind_pandas"
ASSET_NAME = "raw_orders_dataframe"
BATCH_DEFINITION_NAME = "raw_orders_batch"
SUITE_NAME = "raw_orders_suite"


# =========================================================
# 1. Create / load GX context
# =========================================================

context = gx.get_context(
    mode="file",
    context_root_dir=GX_ROOT
)

print("GX context created.")


# =========================================================
# 2. Create Pandas Data Source
# =========================================================

try:
    datasource = context.data_sources.get(
        DATASOURCE_NAME
    )
    print(f"Data source already exists: {DATASOURCE_NAME}")

except Exception:
    datasource = context.data_sources.add_pandas(
        name=DATASOURCE_NAME
    )
    print(f"Data source created: {DATASOURCE_NAME}")


# =========================================================
# 3. Create DataFrame Data Asset
# =========================================================

try:
    data_asset = datasource.get_asset(
        ASSET_NAME
    )
    print(f"Data asset already exists: {ASSET_NAME}")

except Exception:
    data_asset = datasource.add_dataframe_asset(
        name=ASSET_NAME
    )
    print(f"Data asset created: {ASSET_NAME}")


# =========================================================
# 4. Create Batch Definition
# =========================================================

try:
    batch_definition = data_asset.get_batch_definition(
        BATCH_DEFINITION_NAME
    )
    print(
        f"Batch definition already exists: "
        f"{BATCH_DEFINITION_NAME}"
    )

except Exception:
    batch_definition = (
        data_asset.add_batch_definition_whole_dataframe(
            BATCH_DEFINITION_NAME
        )
    )

    print(
        f"Batch definition created: "
        f"{BATCH_DEFINITION_NAME}"
    )


# =========================================================
# 5. Get / Create Expectation Suite
# =========================================================

try:
    suite = context.suites.get(
        SUITE_NAME
    )

    print(
        f"Expectation suite already exists: "
        f"{SUITE_NAME}"
    )

except Exception:
    suite = gx.ExpectationSuite(
        name=SUITE_NAME
    )

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToNotBeNull(
            column="id"
        )
    )

    context.suites.add(suite)

    print(
        f"Expectation suite created: "
        f"{SUITE_NAME}"
    )


# =========================================================
# Done
# =========================================================

print("\n==============================================")
print("GX PANDAS SETUP COMPLETE")
print("==============================================")
