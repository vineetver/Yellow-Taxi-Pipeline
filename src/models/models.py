from abc import ABC, abstractmethod
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import NearestCentroid
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split


class Model(ABC):
    """Abstract class for models."""

    @abstractmethod
    def train(self, X, y):
        """Train the model."""
        pass

    @abstractmethod
    def predict(self, X):
        """Predict the labels for the given data."""
        pass


class MultinomialNBModel(Model):
    """Multinomial Naive Bayes model."""

    def __init__(self):
