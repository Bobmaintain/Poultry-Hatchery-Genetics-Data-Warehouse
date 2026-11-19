# Poultry Hatchery & Genetics Data Warehouse (Data Modelling)

## The Scenario
Large breeding operations track millions of birds across generations to optimize traits like Feed Conversion Ratio (FCR)
and egg production.

## The Engineering Goal
Design a **Star Schema** data warehouse from scratch. It takes flat, unorganized farm logs and split them into clean Fact
and Dimension tables.

## What It Shows:
**Dimensional Modelling:** Designed `dim_flock`, `dim_breed`, `dim_barn_environment`, and `fact_daily_production` tables.

**Complex SQL Joins:** Analytical SQL queries to calculate rolling 7-day mortality rates or FCR across different genetic lines.

**Database Optimization:** Created indexes on high-volume (`flock_id`, `date`) to speed up query performance.

