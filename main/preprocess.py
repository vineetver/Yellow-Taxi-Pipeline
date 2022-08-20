from src.dataset.create_dataset import read_data, write_output_data
from src.feature.preprocessing import remove_rows_with_missing_values, remove_fare_amount_with_zero_values, \
    remove_trip_distance_with_zero_values, remove_out_of_range_data
import psycopg2
import pandas as pd

YEAR = '2014'
MONTH = '01'


def main():
    """
    This function reads the data from the bucket and cleans the data

    Args:
        None
    Returns:
        None
    """
    # Read the table from the postgresql database
    conn = psycopg2.connect(
        database="new_york_trips", user='vineetverma', password='*******', host='localhost', port='5432'
    )
    df = pd.read_sql_query("SELECT * FROM trips", conn)

    # Remove rows with missing values in the data
    df = remove_rows_with_missing_values(df)

    # Remove rows with zero values in the fare_amount column
    df = remove_fare_amount_with_zero_values(df)

    # Remove rows with zero values in the trip_distance column
    df = remove_trip_distance_with_zero_values(df)

    # Remove rows with values out of date range (workdays only)
    df = remove_out_of_range_data(df, YEAR, MONTH)

    # Write the cleaned data to the bucket
    write_output_data(df, 'clean/2014-2022', version='yes')


if __name__ == '__main__':
    main()
