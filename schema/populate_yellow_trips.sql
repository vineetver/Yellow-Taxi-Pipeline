INSERT INTO trips
(cab_type_id,
 vendor_id,
 pickup_datetime,
 dropoff_datetime,
 passenger_count,
 trip_distance,
 rate_code,
 store_and_fwd_flag,
 pickup_location,
 dropoff_location,
 payment_type,
 fare_amount,
 extra,
 mta_tax,
 tip_amount,
 tolls_amount,
 improvement_surcharge,
 total_amount,
 congestion_surcharge,
 airport_fee)
SELECT cab_types.id,
       vendor_id,
       pickup_datetime::timestamp,
       dropoff_datetime::timestamp,
       passenger_count::numeric::integer,
       trip_distance::numeric,
       rate_code::numeric::integer,
       store_and_fwd_flag,
       pickup_location::numeric::integer,
       dropoff_location::numeric::integer,
       payment_type,
       fare_amount::numeric,
       extra::numeric,
       mta_tax::numeric,
       tip_amount::numeric,
       tolls_amount::numeric,
       improvement_surcharge::numeric,
       total_amount::numeric,
       congestion_surcharge::numeric,
       airport_fee::numeric

FROM yellow_tripdata_staging
         INNER JOIN cab_types ON cab_types.type = 'yellow';

TRUNCATE TABLE yellow_tripdata_staging;
VACUUM ANALYZE yellow_tripdata_staging;