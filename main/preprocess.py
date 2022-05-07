from src.data.create_dataset import read_data, write_output_data
from src.features.data_cleaning import remove_rows_with_missing_values, remove_fare_amount_with_zero_values, \
    remove_trip_distance_with_zero_values, remove_out_of_range_data

YEAR = '2022'
MONTH = '02'


def main():
    """
    This function reads the data from the bucket and cleans the data

    Args:
        None
    Returns:
        None
    """
    # Read the data from the bucket
    df = read_data(YEAR, MONTH)

    # Remove rows with missing values in the data
    df = remove_rows_with_missing_values(df)

    # Remove rows with zero values in the fare_amount column
    df = remove_fare_amount_with_zero_values(df)

    # Remove rows with zero values in the trip_distance column
    df = remove_trip_distance_with_zero_values(df)

    # Remove rows with values out of date range (workdays only)
    df = remove_out_of_range_data(df, YEAR, MONTH)

    # Write the cleaned data to the bucket
    write_output_data(df, 'clean/2022_02', version='yes')


if __name__ == '__main__':
    main()
