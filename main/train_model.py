from src.model import classifiers
from src.dataset.create_dataset import get_output_data


def main():
    # e.g. load final train dataframes from cloud
    train_df = get_output_data('data/features/train/2014-2022')

    # Choose the features and the label
    label = 'big_tip'
    features = list(train_df.columns.drop([label, 'tpep_pickup_datetime', 'tpep_dropoff_datetime']))

    # Initialize the model
    model = classifiers.GaussianNBModel(features=features, label=label)

    # get labels and features
    x_train, y_train = model.preprocess(train_df)

    # Fit the model
    model.fit(x_train, y_train)


if __name__ == '__main__':
    main()
