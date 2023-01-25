# plant_db database creation

1. Install PostgreSQL DBMS server and PostGIS plugin, prepare an empty database  
2. Run `1_create_schema.sql` and `2_insert_data.sql`
3. Obtain latest version of `База данных породного состава.xlsx`, set database credentials and run `3_parse_xlsx_to_db.ipynb`

![database schema](plant_db_orthogonal-2022-08.png)