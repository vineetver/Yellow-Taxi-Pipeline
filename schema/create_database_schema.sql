CREATE EXTENSION postgis;

CREATE TABLE green_tripdata_staging (
  vendor_id text,
  pickup_datetime text,
  dropoff_datetime text,
  store_and_fwd_flag text,
  rate_code text,
  pickup_location numeric,
  dropoff_location numeric,
  passenger_count text,
  trip_distance text,
  fare_amount text,
  extra text,
  mta_tax text,
  tip_amount text,
  tolls_amount text,
  ehail_fee text,
  improvement_surcharge text,
  total_amount text,
  payment_type text,
  trip_type text,
  congestion_surcharge text
)
WITH (
  autovacuum_enabled = false,
  toast.autovacuum_enabled = false
);


CREATE TABLE yellow_tripdata_staging (
  vendor_id text,
  pickup_datetime text,
  dropoff_datetime text,
  passenger_count text,
  trip_distance text,
  rate_code text,
  store_and_fwd_flag text,
  pickup_location numeric,
  dropoff_location numeric,
  payment_type text,
  fare_amount text,
  extra text,
  mta_tax text,
  tip_amount text,
  tolls_amount text,
  improvement_surcharge text,
  total_amount text,
  congestion_surcharge text,
  airport_fee text
)
WITH (
  autovacuum_enabled = false,
  toast.autovacuum_enabled = false
);

CREATE TABLE cab_types (
  id serial primary key,
  type text
);

INSERT INTO cab_types (type) VALUES ('yellow'), ('green');

CREATE TABLE trips (
  id bigserial primary key,
  cab_type_id integer,
  vendor_id text,
  pickup_datetime timestamp without time zone,
  dropoff_datetime timestamp without time zone,
  store_and_fwd_flag text,
  rate_code integer,
  pickup_location numeric,
  dropoff_location numeric,
  passenger_count integer,
  trip_distance numeric,
  fare_amount numeric,
  extra numeric,
  mta_tax numeric,
  tip_amount numeric,
  tolls_amount numeric,
  ehail_fee numeric,
  improvement_surcharge numeric,
  congestion_surcharge numeric,
  total_amount numeric,
  payment_type text,
  trip_type integer,
  airport_fee numeric
);
