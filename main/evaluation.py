from src.model import classifiers
from src.dataset.create_dataset import get_output_data


def main():
    # e.g. load final test dataframes from cloud
    test_df = get_output_data('data/features/test/2014-2022')

    # Choose the features and the label
    label = 'big_tip'
    features = list(test_df.columns.drop([label, 'tpep_pickup_datetime', 'tpep_dropoff_datetime']))

    # Initialize the model
    model = classifiers.GaussianNBModel(features=features, label=label)

    # get labels and features
    x_test, y_test = model.preprocess(test_df)

    # Fit the model
    model.predict(x_test)

    # Plot the confusion matrix (normalized
    model.plot_confusion_matrix(x_test, y_test, normalize='true')


if __name__ == '__main__':
    main()
