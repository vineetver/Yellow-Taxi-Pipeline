"""
Create_dataset.py
Contains functions for importing and exporting data.
"""
import os
from datetime import datetime
import pandas as pd
from google.cloud import storage

BUCKET_NAME = 'yellow_taxi_vineet'
token = os.environ['GOOGLE_APPLICATION_CREDENTIALS']


def read_data(year: str, month: str) -> pd.DataFrame:
    """
    Reads the data for a given year and month.

    Args:
        year: The year to read.
        month: The month to read.

    Returns:
        The data for the given year and month.
    """

    file_path = get_raw_data_path(year, month)

    df = pd.read_csv(file_path, parse_dates=['tpep_pickup_datetime', 'tpep_dropoff_datetime'], infer_datetime_format=True, low_memory=False,
                     storage_options={'token': token})

    return df


def get_raw_data_path(year: str, month: str) -> str:
    """
    Gets the file path for the given year and month.

    Args:
        year: The year to read.
        month: The month to read.

    Returns:
        The file path for the given year and month.
    """

    assert "2020" <= year <= "2022", 'No data for year {} available. Please select a year between 2021 and 2022.'.format(year)
    assert isinstance(year, str), 'Year must be an string.'
    assert isinstance(month, str), 'Month must be an string.'

    url = f'gs://{BUCKET_NAME}/tripdata/'
    file_path = f'{url}yellow_tripdata_{year}-{month}.csv'

    return file_path


def write_data(df: pd.DataFrame, suffix: str, scratch: bool = True) -> str:
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

    path = f''

    if scratch:
        path = os.path.join(path, 'scratch')

    path = os.path.join(path, suffix).replace('\\', '/')

    client = storage.Client()
    bucket = client.get_bucket(BUCKET_NAME)
    blob = bucket.blob(path)
    blob.chunk_size = 262144

    blob.upload_from_string(df.to_csv(index=False, encoding='utf-8'))

    return path


def get_output_path(stage: str, version: str = None) -> str:
    """
    This function returns the output file path for the given stage and version.

    Args:
        stage: The stage to write to.
        version: The version of the stage to write to.

    Returns:
        The file path for the given stage and version.
    """

    output_path = f'{stage}'

    if version is not None:
        version = get_time_stamp()
    else:
        version = get_latest_time_stamp(list_files(output_path))

    path = os.path.join(output_path, version).replace('\\', '/')

    return path


def write_output_data(df: pd.DataFrame, stage: str, version: str = None, overwrite: bool = False) -> str:
    """
    This function writes the dataframe to a csv file in the bucket

    Args:
        df: The data to write.
        stage: The stage to write to (e.g. 'clean', 'preprocess').
        version: The version of the stage to write to.
        overwrite: Check if the file already exists

    Returns:
        None
    """

    assert len(stage) > 0, 'Please provide a stage name to write to. (e.g. "clean", "preprocess")'

    output_path = f'data/{get_output_path(stage, version)}'
    path = os.path.join(output_path + '.csv').replace('\\', '/')

    if overwrite is False:
        assert path not in list_files('data'), 'File already exists'

    client = storage.Client()
    bucket = client.get_bucket(BUCKET_NAME)
    blob = bucket.blob(path)
    blob.chunk_size = 262144

    blob.upload_from_string(df.to_csv(index=False, encoding='utf-8'))

    return path


def get_output_data(stage: str, version: str = None) -> pd.DataFrame:
    """
    This function returns the dataframe for the given stage and version.

    Args:
        stage: The stage to read from.
        version: The version of the stage to read from.

    Returns:
        The dataframe for the given stage and version.
    """

    assert len(stage) > 0, 'Please provide a stage name to read from. (e.g. "clean", "preprocess")'

    if version is None:
        version = get_latest_time_stamp(list_files('data'))

    output_path = f'gs://{BUCKET_NAME}/data/{stage}/{version}'
    path = os.path.join(output_path + '.csv').replace('\\', '/')

    print(f'Current version: {version}')

    df = pd.read_csv(path, parse_dates=['tpep_pickup_datetime', 'tpep_dropoff_datetime'], infer_datetime_format=True, low_memory=False,
                     storage_options={'token': token})

    return df


def get_time_stamp() -> str:
    """
    This function returns the time stamp for the current time.

    Returns:
        The time stamp for the given year and month.
    """

    time_stamp = pd.Timestamp.now().strftime('%Y%m%d-%H%M%S')

    return time_stamp


def get_latest_time_stamp(files: list) -> datetime:
    """
    This function returns the time stamp for the latest file.

    Returns:
        The time stamp for the latest file.
    """

    format = '%Y%m%d-%H%M%S'
    timestamps = []

    for file in files:
        if file.endswith('.csv'):
            suffix = file.split('/')[-1].split('.')[0]
            datetime.strptime(suffix, format)
            timestamps.append(suffix)

    return max(timestamps)


def list_files(dictionary: str) -> list:
    """
    This function returns a list of files in the given path.

    Args:
        dictionary: The dictionary to search

    Returns:
        The list of files in the given dictionary.
    """

    client = storage.Client()
    bucket = client.get_bucket(BUCKET_NAME)
    blobs = bucket.list_blobs(prefix=dictionary)

    return [blob.name for blob in blobs]
