import pandas as pd
import calendar


def remove_rows_with_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function removes rows with missing values.
    """
    return df.dropna()


def remove_fare_amount_with_zero_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function removes rows with zero values.
    """
    return df.loc[df['fare_amount'] > 0]


def remove_trip_distance_with_zero_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function removes rows with zero values.
    """
    return df.loc[df['trip_distance'] > 0]


def remove_out_of_range_data(df: pd.DataFrame, year: str = None, month: str = None) -> pd.DataFrame:
    """
    This function removes rows with values out of date range. (date range is workdays)
    """
    start, end = calendar.monthrange(int(year), int(month))
    start_day = f'{year}-{month}-{start:02d}'
    end_day = f'{year}-{month}-{end:02d}'

    df = df[df['tpep_dropoff_datetime'].astype('str') >= start_day]
    df = df[df['tpep_dropoff_datetime'].astype('str') <= end_day]

    return df
