"""
Create_dataset.py
Contains functions for importing and exporting data.
"""
import os
import pandas as pd

BUCKET_NAME = 'yellowtaxi-bucket'


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

    url = f'gs://{BUCKET_NAME}/tripdata/'
    file_path = f'{url}yellow_tripdata_{year}-{month}.csv'

    return file_path


def write_file(df: pd.DataFrame, suffix: str, scratch: bool = True) -> str:
    """
    This function writes the dataframe to a csv file in the bucket

    Args:
        df: The data to write.
        suffix: The suffix to add to the file name.
        scratch: Write the file with the suffix

    Returns:
        None
    """

    assert suffix.endswith('.csv'), 'Suffix must end with .csv'

    path = f'gs://{BUCKET_NAME}'

    if scratch:
        path = os.path.join(path, 'scratch')

    path = os.path.join(path, suffix)

    df.to_csv(path, index=False)

    return path


def get_output_file_name(stage: str, version: str = None) -> str:
    """
    This function returns the output file path for the given stage and version.

    Args:
        stage: The stage to write to.
        version: The version of the stage to write to.

    Returns:
        The file path for the given stage and version.
    """

    output_file_name = f'{stage}'

    if version is not None:
        path = os.path.join(output_file_name, version)

    path = os.path.join(output_file_name, stage)

    return path
