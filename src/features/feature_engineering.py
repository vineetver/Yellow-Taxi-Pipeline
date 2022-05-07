"""
This file contains the code for feature generation.
"""
from typing import List
import pandas as pd
import numpy as np
from abc import ABC, abstractmethod


class FeatureEngineer(ABC):
    """
    Abstract class for feature engineering.
    """

    def __init__(self, feature_name: str, column_name: List[str]):
        """
        Initialize the feature engineering class with the feature name and the column(s) name used to create the feature.

        Args:
            feature_name (str): The name of the feature.
            column_name (List[str]): The name of the column(s) used to create the feature.
        """
        self.feature_name = feature_name
        self.column_name = column_name

    @abstractmethod
    def generate_feature(self, *args, **kwargs):
        """
        Generate feature.
        """
        pass

    @abstractmethod
    def feature_dtype(self):
        """
        indicates the dtype of the feature
        """
        pass


class TripFeature(FeatureEngineer):
    """
    This class generates the features for the distance.
    """

    def __init__(self):
        """
        Initialize the class.
        """
        super().__init__('trip', ['trip_distance', 'tolls_amount', 'tpep_pickup_datetime', 'tpep_dropoff_datetime'])

    def generate_feature(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate the feature.
        """
        df['trip_duration'] = (df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']).dt.total_seconds() / 60
        df['trip_speed'] = df['trip_distance'] / df['trip_duration']
        df['trip_tolls'] = df['tolls_amount']

        return df[self.feature_dtype().keys()]

    def feature_dtype(self):
        """
        indicates the dtype of the feature
        """
        return {
            'trip_duration': np.int32,
            'trip_speed'   : np.float32,
            'trip_tolls'   : np.float32
        }


class TimeFeature(FeatureEngineer):
    """
    This class generates the features for the pick-up date.
    """

    def __init__(self):
        """
        Initialize the class.
        """
        super().__init__('pick_up', ['tpep_pickup_datetime'])

    def generate_feature(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate the feature.
        """

        df['pickup_weekday'] = df.tpep_pickup_datetime.dt.dayofweek
        df['pickup_hour'] = df.tpep_pickup_datetime.dt.hour
        df['pickup_month'] = df.tpep_pickup_datetime.dt.month
        df['pickup_minute'] = df.tpep_pickup_datetime.dt.minute

        df['work_hours'] = (df['pickup_hour'] >= 8) & (df['pickup_hour'] <= 18) & (df['pickup_weekday'] < 5)

        return df[self.feature_dtype().keys()]

    def feature_dtype(self):
        """
        indicates the dtype of the feature
        """
        return {
            'pickup_weekday': np.int8,
            'pickup_hour'   : np.int8,
            'pickup_month'  : np.int8,
            'pickup_minute' : np.int8,
            'work_hours'    : np.bool
        }


class MeterFeature(FeatureEngineer):
    """
    This class encodes the categorical features.
    """

    def __init__(self):
        """
        Initialize the class.
        """
        super().__init__('meter', ['PULocationID', 'DOLocationID'])

    def generate_feature(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate the feature.
        """
        df['meter_eng'] = df['PULocationID']
        df['meter_dis'] = df['DOLocationID']

        return df[self.feature_dtype().keys()]

    def feature_dtype(self):
        """
        indicates the dtype of the feature
        """

        return {
            'meter_eng': np.int32,
            'meter_dis': np.int32
        }


class TipFeature(FeatureEngineer):
    """
    This class encodes the categorical features.
    """

    def __init__(self):
        """
        Initialize the class.
        """
        super().__init__('tip', ['tip_amount', 'fare_amount'])

    def generate_feature(self, df: pd.DataFrame, high_tip: float = 0.25) -> pd.DataFrame:
        """
        Generate the feature.
        """

        df['total_tip'] = df['tip_amount']
        df['total_fare'] = df['fare_amount']
        df['tip_percentage'] = df['total_tip'] / df['total_fare'] * 100

        df['big_tip'] = df['tip_percentage'] > high_tip

        return df[self.feature_dtype().keys()]

    def feature_dtype(self):
        """
        indicates the dtype of the feature
        """
        return {
            'total_tip'     : np.float32,
            'total_fare'    : np.float32,
            'tip_percentage': np.float32,
            'big_tip'       : np.bool
        }
