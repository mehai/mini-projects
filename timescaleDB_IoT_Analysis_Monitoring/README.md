# timescaleDB - IoT Analysis and Monitoring
This is a tutorial mini-project with the purpose of getting started
with timescaleDB for data storage and analysis.

Based on [this](https://docs.timescale.com/latest/tutorials/tutorial-hello-timescale) tutorial.

## How to
1. Run 1_create_db.sql to create the database and timescaleDB extension.
2. Run the nyc_data/nyc_data.sql script to create database objects (tables and indexes).
3. ```\COPY rides FROM nyc_data/nyc_data_rides.csv CSV;```
4. Perform analysis. Some queries can be found in analysis.sql.
5. (Optional) Continuous Aggregates. Detailed examples in contagg.sql.

## Notes
You need to download and decompress [this](https://timescaledata.blob.core.windows.net/datasets/nyc_data.tar.gz) archive.
This is the dataset with the sql script for creating the tables.
