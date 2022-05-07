from src.models import models
from src.data.create_dataset import *


def main():
    # e.g. load final dataframes from cloud (month 1 is for training, month 2 is for testing)
    train_df = get_output_data('data/features/2022_01')
    test_df = get_output_data('data/features/2022_02')

    # Choose the features and the label
    label = 'big_tip'
    features = list(train_df.columns.drop([label, 'tpep_pickup_datetime', 'tpep_dropoff_datetime']))

    # Initialize the model
    model = models.GaussianNBModel(features=features, label=label)

    # Split the data into train and test
    x_train, y_train = model.preprocess(train_df)
    x_test, y_test = model.preprocess(test_df)

    # Fit the model
    model.fit(x_train, y_train)

    # Plot the confusion matrix (normalized
    model.plot_confusion_matrix(x_test, y_test, normalize='true')


if __name__ == '__main__':
    main()
