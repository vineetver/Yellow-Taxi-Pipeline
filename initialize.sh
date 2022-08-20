# shellcheck disable=SC2034
year_month_regex="tripdata_([0-9]{4})-([0-9]{2})"

green_schema="(
vendor_id,
pickup_datetime,
dropoff_datetime,
store_and_fwd_flag,
rate_code,
pickup_location,
dropoff_location,
passenger_count,
trip_distance,
fare_amount,
extra,
mta_tax,
tip_amount,
tolls_amount,
ehail_fee,
improvement_surcharge,
total_amount,
payment_type,
trip_type,
congestion_surcharge
)"

yellow_schema="(
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
airport_fee
)"

for filename in /Volumes/SSDT5/NYC-Trips/20*/Green/green_tripdata_*.csv; do
  echo "$(date): Loading file ${filename}"
  sed $'s/\r$//' $filename | sed '/^$/d' | psql new_york_trips -c "COPY green_tripdata_staging ${schema} FROM stdin CSV HEADER;"
  psql new_york_trips -f schema/init_green.sql
  echo "$(date): done ${filename}"
done

for filename in /Volumes/SSDT5/NYC-Trips/20*/Yellow/yellow_tripdata_*.csv; do
  echo "$(date): Loading file ${filename}"
  sed $'s/\r$//' $filename | sed '/^$/d' | psql new_york_trips -c "COPY yellow_tripdata_staging ${schema} FROM stdin CSV HEADER;"
  psql new_york_trips -f schema/init_yellow.sql
  echo "$(date): done ${filename}"
done
