from src.models import models
from src.data.create_dataset import *
import pandas as pd


def main():
    train_df = get_output_data('data/features/2022_01')
    test_df = get_output_data('data/features/2022_02')

    label = 'big_tip'
    features = list(train_df.columns.drop([label, 'tpep_pickup_datetime', 'tpep_dropoff_datetime']))

    model = models.GaussianNBModel(features=features, label=label)

    x_train, y_train = model.preprocess(train_df)
    x_test, y_test = model.preprocess(test_df)

    history = model.fit(x_train, y_train)


if __name__ == '__main__':
    main()
