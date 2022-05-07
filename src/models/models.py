from abc import ABC, abstractmethod
from typing import Any

import numpy as np
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import NearestCentroid
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler


class Model(ABC):
    """Abstract class for models."""

    def __init__(self, features=None, params=None):
        if features is None:
            features = []
        if params is None:
            params = {}
        self.features = features
        self.params = params
        self.model = None

    @abstractmethod
    def preprocess(self, df: pd.DataFrame, label: str):
        """ Any model specific preprocessing that needs to be done before training the model."""
        pass

    @abstractmethod
    def split(self, X, Y, test_size: float = 0.2):
        """Split the data into training and test sets."""
        return train_test_split(X, Y, test_size=test_size)

    @abstractmethod
    def normalize(self, X):
        """Normalize the data."""
        pass

    @abstractmethod
    def fit(self, X, Y):
        """Train the model."""
        pass

    @abstractmethod
    def predict(self, X):
        """Predict the labels for the given data."""
        pass

    def evaluate(self, X, Y):
        """Evaluate the model."""
        pass

    def cross_validate(self, X, Y, n_splits: int = 10):
        """Cross validate the model."""
        pass


class MultinomialNBModel(Model, ABC):
    """Multinomial Naive Bayes model."""

    def __init__(self, features=None, params=None):
        """Initialize the model with the given features and params."""
        model_params = {'n_jobs': -1, 'random_state': 0}
        params.update(model_params)
        super().__init__(features=features, params=params)

    def preprocess(self, df: pd.DataFrame, label: str) -> tuple[Any, Any]:
        """Preprocess the dataframe."""
        df.dropna(inplace=True)
        X = df[self.features].values
        Y = df[label].values
        return X, Y

    def split(self, X, Y, test_size: float = 0.2) -> (np.ndarray, np.ndarray, np.ndarray, np.ndarray):
        return train_test_split(X, Y, test_size=test_size, random_state=self.params['random_state'])

    def fit(self, X, Y) -> MultinomialNB:
        model = MultinomialNB(**self.params)
        model.fit(X, Y)
        model = self.model
        return model

    def predict(self, X) -> np.ndarray:
        return self.model.predict(X)
