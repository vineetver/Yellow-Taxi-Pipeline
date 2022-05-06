"""
Create_dataset.py
Contains functions for importing and exporting data.
"""
import pandas as pd


def read_file(year: str, month: str) -> pd.DataFrame:
    """
    Reads the data for a given year and month.

    Args:
        year: The year to read.
        month: The month to read.

    Returns:
        The data for the given year and month.
    """

    file_path = get_file_path(year, month)

    df = pd.read_csv(file_path, parse_dates=['tpep_pickup_datetime', 'tpep_dropoff_datetime'], infer_datetime_format=True, low_memory=False)

    return df


def get_file_path(year: str, month: str) -> str:
    """
    Gets the file path for the given year and month.

    Args:
        year: The year to read.
        month: The month to read.

    Returns:
        The file path for the given year and month.
    """
    assert "2021" <= year <= "2022", 'No data for year {} available. Please select a year between 2021 and 2022.'.format(year)
    assert isinstance(year, str), 'Year must be an string.'
    assert isinstance(month, str), 'Month must be an string.'

    url = 'gs://yellowtaxi-bucket/'
    file_path = url + 'yellow_tripdata_{}-{}.csv'.format(year, month)

    return file_path
