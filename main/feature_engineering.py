from src.feature import feature_selection
from src.dataset.create_dataset import get_output_data, write_output_data
import pandas as pd


def main():
    """
    This function reads the cleaned data from the bucket and generates the features
    """

    # Read the data from the bucket
    df = get_output_data('data/clean/2014-2022')

    # Generate the feature
    trip_features = feature_selection.TripFeature().generate_feature(df)

    time_features = feature_selection.TimeFeature().generate_feature(df)

    meter_features = feature_selection.MeterFeature().generate_feature(df)

    tip_features = feature_selection.TipFeature().generate_feature(df)

    df = pd.concat([trip_features, time_features, meter_features, tip_features, df['tpep_pickup_datetime'].to_frame(),
                    df['tpep_dropoff_datetime'].to_frame()], axis=1)
    
    # Write the feature to the bucket
    write_output_data(df, 'features/2014-2022', version='yes')


if __name__ == '__main__':
    main()
