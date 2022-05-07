from src.features import feature_engineering
from src.data.create_dataset import get_output_data, write_output_data


def main():
    """
    This function reads the cleaned data from the bucket and generates the features
    """

    # Read the data from the bucket
    df = get_output_data('clean')

    # Generate the feature
    df = feature_engineering.PickUpDateFeature().generate_feature(df)

    # Write the feature to the bucket
    write_output_data(df, 'features', version='yes')


if __name__ == '__main__':
    main()
