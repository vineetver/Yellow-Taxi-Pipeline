from src.dataset.create_dataset import write_output_data
from src.feature.preprocessing import remove_rows_with_missing_values, remove_fare_amount_with_zero_values, \
    remove_trip_distance_with_zero_values, remove_out_of_range_data
from google.cloud import bigquery
import os

YEAR = '2014'
MONTH = '01'
token = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
client = bigquery.Client.from_service_account_json(token)


def main():
    """
    This function reads the data from the bucket and cleans the data

    Args:
        None
    Returns:
        None
    """
    # Read the table from the bigquery
    df = client.query('''
      SELECT
        *
      FROM `public-data-359023.new_york_trips.trips`''').to_dataframe()

    # Remove rows with missing values in the data
    df = remove_rows_with_missing_values(df)

    # Remove rows with zero values in the fare_amount column
    df = remove_fare_amount_with_zero_values(df)

    # Remove rows with zero values in the trip_distance column
    df = remove_trip_distance_with_zero_values(df)

    # Remove rows with values out of date range (workdays only)
    df = remove_out_of_range_data(df, YEAR, MONTH)

    # Write to bigquery table
    job_config = bigquery.LoadJobConfig(schema=[
        bigquery.SchemaField("my_string", "STRING"),
    ])

    job = client.load_table_from_dataframe(
        df, 'new_york_trips.trips_clean', job_config=job_config
    )

    job.result()

    # Or write the cleaned data to the bucket
    # write_output_data(df, 'clean/2014-2022', version='yes')


if __name__ == '__main__':
    main()
