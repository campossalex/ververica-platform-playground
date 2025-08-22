CREATE USER root WITH PASSWORD 'admin1';

CREATE DATABASE report;

GRANT ALL PRIVILEGES ON DATABASE report TO root;

CREATE TABLE purchase_report (dim_item VARCHAR(255), dim_category VARCHAR(255), dim_state VARCHAR(255), purchase_window TIMESTAMP, fact_count_transactions FLOAT, fact_sum_quantity FLOAT, fact_sum_price FLOAT, fact_sum_member_discount FLOAT, fact_sum_supplement_price FLOAT, fact_sum_total_purchase FLOAT, fact_avg_total_purchase FLOAT, PRIMARY KEY(dim_item, dim_category, dim_state, purchase_window));

CREATE INDEX idx_timestamp ON transaction_report (dim_transaction_time);

ALTER TABLE transaction_report OWNER TO root;
