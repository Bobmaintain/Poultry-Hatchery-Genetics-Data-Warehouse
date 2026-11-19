import pandas as pd
import sqlite3


def build_poultry_warehouse():
    print("1. Generating flat hatchery & farm production logs...")
    # Simulate a last CSV export from a farm management system
    flat_data = pd.DataFrame({
        "record_id": list(range(1, 11)),
        "flock_code": ["FLK-A1", "FLK-A1", "FLK-A1", "FLK-B2", "FLK-B2", "FLK-B2", "FLK-C3", "FLK-C3", "FLK-C3",
                       "FLK-C3"],
        "genetic_strain": ["Ross 308,", "Ross 308", "Ross 308", "Cobb 500", "Cobb 500", "Cobb 500", "Ross 308",
                           "Ross 308", "Ross 308", "Ross 308"],
        "barn_number": ["Barn 1", "Barn 1", "Barn 1", "Barn 2", "Barn 2", "Barn 2", "Barn 3", "Barn 3", "Barn 3",
                        "Barn 3"],
        "day_of_age": list((7, 14, 21, 7, 14, 21, 7, 14, 21, 28)),
        "feed_consumed_kg": list((180.5, 450.0, 890.2, 175.0, 440.5, 870.0, 185.0, 460.0, 910.5, 1420.0)),
        "total_bird_weight_kg": list((165.0, 380.0, 690.0, 158.0, 365.0, 665.0, 170.0, 390.0, 710.0, 1050.0)),
        "mortality_count": list((2, 1, 3, 4, 2, 1, 1, 0, 2, 1))
    })

    # 2. Data Modelling: Split flat data into Dimension and Fact tables
    # Dimension Table: Unique Flock Metadata
    dim_flocks = flat_data[['flock_code', 'genetic_strain', 'barn_number']].drop_duplicates().reset_index(drop=True)
    dim_flocks['flock_id'] = dim_flocks.index + 100  # Surrogate Key

    # Merge surrogate key back to create the Fact Table
    fact_production = flat_data.merge(dim_flocks, on=['flock_code', 'genetic_strain', 'barn_number'])
    fact_production = fact_production[['record_id', 'flock_id', 'day_of_age', 'feed_consumed_kg',
                                       'total_bird_weight_kg', 'mortality_count']]

    # 3. Load into SQLite Data Warehouse & Create Indexes
    conn = sqlite3.connect("poultry_genetics_dw.db")
    dim_flocks.to_sql("dim_flocks", conn, if_exists="replace", index=False)
    fact_production.to_sql("fact_daily_production", conn, if_exists="replace", index=False)

    # Create SQL Index to optimize join speeds
    conn.execute("CREATE INDEX IF NOT EXISTS idx_flock_id ON fact_daily_production(flock_id)")
    print("Star Schema built and indexed successfully.")

    # 4. Run an Analytical SQL Query to calculate Feed Conversion Ratio (FCR) by Genetic Strain
    query = """
        SELECT
            d.genetic_strain,
            SUM(f.feed_consumed_kg) AS total_feed_kg,
            SUM(f.total_bird_weight_kg) AS total_weight_kg,
            ROUND(CAST(SUM(f.feed_consumed_kg) AS FLOAT) / SUM(f.total_bird_weight_kg), 3) AS cumulative_fcr,
            SUM(f.mortality_count) AS total_mortality
        FROM fact_daily_production f
        JOIN dim_flocks d ON f.flock_id = d.flock_id
        GROUP BY d.genetic_strain
    """
    print("\n--- Analytical Warehouse Output: Genetic Performance ---")
    print(pd.read_sql(query, conn))
    conn.close()


if __name__ == "__main__":
    build_poultry_warehouse()
