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
    def generate_feature(self):
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


class PickUpDateFeature(FeatureEngineer):
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

        df['pick_up_weekday'] = df.tpep_pickup_datetime.dt.dayofweek
        df['pick_up_hour'] = df.tpep_pickup_datetime.dt.hour
        df['pick_up_month'] = df.tpep_pickup_datetime.dt.month
        df['pick_up_minute'] = df.tpep_pickup_datetime.dt.minute

        df['work_hours'] = (df.pick_up_hour >= 8) & (df.pick_up_hour <= 18) & (df.pick_up_weekday < 5)

        return df[self.feature_dtype().keys()]

    def feature_dtype(self):
        """
        indicates the dtype of the feature
        """
        return {
            'pick_up_weekday': np.int8,
            'pick_up_hour'   : np.int8,
            'pick_up_month'  : np.int8,
            'pick_up_minute' : np.int8,
            'work_hours'     : np.bool
        }
