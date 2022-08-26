from src.feature import feature_selection
from src.dataset.create_dataset import write_output_data
import pandas as pd
from google.cloud import bigquery
import os

token = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
client = bigquery.Client.from_service_account_json(token)


def main():
    """
    This function reads the cleaned data from the bucket and generates the features
    """
    df = client.query('''
      SELECT
        *
      FROM `public-data-359023.new_york_trips.trips_clean`''').to_dataframe()

    # Generate the feature
    trip_features = feature_selection.TripFeature().generate_feature(df)

    time_features = feature_selection.TimeFeature().generate_feature(df)

    meter_features = feature_selection.MeterFeature().generate_feature(df)

    tip_features = feature_selection.TipFeature().generate_feature(df)

    df = pd.concat([trip_features, time_features, meter_features, tip_features, df['tpep_pickup_datetime'].to_frame(),
                    df['tpep_dropoff_datetime'].to_frame()], axis=1)

    # Write to bigquery table
    job_config = bigquery.LoadJobConfig(schema=[
        bigquery.SchemaField("my_string", "STRING"),
    ])

    job = client.load_table_from_dataframe(
        df, 'new_york_trips.features', job_config=job_config
    )

    job.result()

    # Or write the feature to the bucket
    # write_output_data(df, 'features/2014-2022', version='yes')


if __name__ == '__main__':
    main()
