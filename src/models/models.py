from abc import ABC, abstractmethod
from typing import Any, List

import numpy as np
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import NearestCentroid
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import f1_score, plot_confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import StratifiedShuffleSplit, StratifiedKFold


class Model(ABC):
    """Abstract class for models."""

    def __init__(self, features: List[str] = None, label: str = None, params: dict = None):
        if features is None:
            features = []
        if label is None:
            label = []
        if params is None:
            params = {}
        self.label = label
        self.features = features
        self.params = params
        self.model = None

    def preprocess(self, df: pd.DataFrame):
        """ Any model specific preprocessing that needs to be done before training the model."""
        pass

    def split(self, X, Y, test_size: float):
        """Split the data into training and test sets."""
        pass

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

    @abstractmethod
    def evaluate(self, X, Y):
        """Evaluate the model."""
        pass

    @abstractmethod
    def cross_validate(self, X, Y, n_splits: int = 10):
        """Cross validate the model."""
        pass

    def feature_importance(self, X, Y):
        """Get the feature importance."""
        pass


class GaussianNBModel(Model, ABC):
    """Multinomial Naive Bayes model."""

    def __init__(self, features=None, label: str = None, params: dict = None):
        """Initialize the model with the given features and params."""
        if features is None:
            features = []
        super().__init__(features, label, params)

    def preprocess(self, df: pd.DataFrame) -> tuple[Any, Any]:
        """Preprocess the dataframe."""
        df.dropna(inplace=True)
        df = df[np.isfinite(df['trip_speed'])]  # drop rows with inf in trip_speed
        X = df[self.features].values
        Y = df[self.label].values
        return X, Y

    def fit(self, X, Y) -> GaussianNB:
        model = GaussianNB(**self.params)
        model.fit(X, Y)
        self.model = model
        return model

    def predict(self, X) -> np.ndarray:
        return self.model.predict(X)

    def evaluate(self, X, Y) -> tuple:
        y_pred = self.predict(X)
        f1 = f1_score(Y, y_pred)
        return f1

    def cross_validate(self, X, Y, n_splits: int = 10) -> List[tuple]:
        f1_scores = []
        for train, test in StratifiedKFold(n_splits=n_splits).split(X, Y):
            x_train, x_test, y_train, y_test = X[train], X[test], Y[train], Y[test]
            self.fit(x_train, y_train)
            f1_scores.append(self.evaluate(x_test, y_test))
        return f1_scores

    def feature_importance(self, X, Y) -> pd.DataFrame:
        model = self.model
        feature_importance = pd.DataFrame(model.feature_importances_, index=self.features, columns=['importance'])
        feature_importance.sort_values('importance', ascending=False, inplace=True)
        return feature_importance
