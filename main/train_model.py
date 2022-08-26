from src.model import classifiers
from google.cloud import bigquery
import os
from sklearn.model_selection import train_test_split

token = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
client = bigquery.Client.from_service_account_json(token)


def main():
    # e.g. load final train dataframes from cloud
    df = client.query('''
          SELECT
            *
          FROM `public-data-359023.new_york_trips.features`''').to_dataframe()

    # Choose the features and the label
    label = 'big_tip'
    features = list(df.columns.drop([label, 'tpep_pickup_datetime', 'tpep_dropoff_datetime']))

    # Initialize the model
    model = classifiers.GaussianNBModel(features=features, label=label)

    # get labels and features
    X, Y = model.preprocess(df)

    # Split the data into train and test
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    # Fit the model
    model.fit(x_train, y_train)

    # Plot the confusion matrix (normalized
    model.plot_confusion_matrix(x_test, y_test, normalize='true')


if __name__ == '__main__':
    main()
