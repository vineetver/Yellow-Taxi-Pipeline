<h2 align="center">Yellow Taxi Pipeline</h2>

## Description

An exploration of New York City's vernacular neighbourhoods, traffic, taxi usage, and more through a dataset of over 1 billion NYC Taxi trips.

The New York City Taxi & Limousine Commission (TLC) regulates and licenses all taxi and for-hire vehicles in New York City. The TLC makes data on all taxi trips taken in New York City available to the public, and this dataset includes information on over 1.1 billion taxi trips in NYC from 2009 to 2022. The data is more than just a record of where people have been and when - it's a portrait of New York City and how it has changed over time. What months are the busiest for taxi usage? What are the most popular destinations? What are the most common pickup and drop-off locations? How bad is traffic in Manhattan, and how has it changed over time? What time do hedge fund managers hail their taxis? The dataset answers all these questions and many more.

I also explore to deploy and maintain a machine learning model that can predict whether a passenger of New York City's Yellow Taxi will make a large tip or not. A tip is significantly big if the tip is greater than 25% of the total fare. Since the target variable `big_tip (boolean)` is binary, it is a classification problem.

The best model so far is `GaussianNB` (baseline) with a 10-fold cross-validation **F1 score** of 82%. 

![download](https://user-images.githubusercontent.com/66165922/185767641-3170351a-e9e7-4b4d-b015-1aeb79b53b21.jpg)

(Normalized)

## About the Data

The data is from the [**NYC Yellow Taxi Data**](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page). The
data is a collection of taxi trips taken by the city of New York City in the years 2014-2022. The yellow
taxi trip records include fields such as pickup and dropoff datetime, passenger count, fare amount, etc.

The data is stored in a private **Google Cloud Storage** bucket.

| Column Name            | Description                                                                                                                                                                                                                                                 |
|-----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **VendorID**              | A code indicating the TPEP provider that provided the record. <br/> <strong>1= Creative Mobile Technologies, LLC; 2= VeriFone Inc.</strong>                                                                                                                 |
| **tpep_pickup_datetime**  | The date and time when the meter was engaged.                                                                                                                                                                                                               |
| **tpep_dropoff_datetime** | The date and time when the meter was disengaged.                                                                                                                                                                                                            |
| **Passenger_count**       | The number of passengers in the vehicle. <br/>This is a driver-entered value.                                                                                                                                                                               |
| **Trip_distance**         | The elapsed trip distance in miles reported by the taximeter.                                                                                                                                                                                               |
| **PULocationID**          | TLC Taxi Zone in which the taximeter was engaged                                                                                                                                                                                                            |
| **DOLocationID**          | TLC Taxi Zone in which the taximeter was disengaged                                                                                                                                                                                                         |
| **RateCodeID**            | The final rate code in effect at the end of the trip. <br/> **1= Standard rate, 2=JFK, 3=Newark, 4=Nassau or Westchester, 5=Negotiated fare, 6=Group ride**                                                                                                 |
| **Store_and_fwd_flag**    | This flag indicates whether the trip record was held in vehicle memory before sending to the vendor, aka “store and forward,” because the vehicle did not have a connection to the server. <br/> Y= store and forward trip, N= not a store and forward trip |
| **Payment_type**          | A numeric code signifying how the passenger paid for the trip. </br> **1= Credit card, 2= Cash, 3= No charge, 4= Dispute, 5= Unknown, 6= Voided trip**                                                                                                          |
| **Fare_amount**           | The time-and-distance fare calculated by the meter.                                                                                                                                                                                                         | 
| **Extra**                 | Miscellaneous extras and surcharges. Currently, this only includes the $0.50 and $1 rush hour and overnight charges.                                                                                                                                        |
| **MTA_tax**               | $0.50 MTA tax that is automatically triggered based on the metered rate in use.                                                                                                                                                                             | 
| **Improvement_surcharge** | $0.30 improvement surcharge assessed trips at the flag drop. The improvement surcharge began being levied in 2015.                                                                                                                                          | 
| **Tip_amount**            | Tip amount – This field is automatically populated for credit card tips. Cash tips are not included.                                                                                                                                                        | 
| **Tolls_amount**          | Total amount of all tolls paid in trip.                                                                                                                                                                                                                     | 
| **Total_amount**          | The total amount charged to passengers. Does not include cash tips.                                                                                                                                                                                         |

## Postgres Database and BigQuery

All the raw data is stored in a Postgresql Database for fast access. The raw data is transferred into BigQuery to run analytical queries. All the data from different stages of the pipeline e.g cleaning, processing is stored in BigQuery with proper indexing fast access. Since the data is stored in BigQuery, it is accessible from anywhere in the world. Beware that the data can be very large and can take a while to load.

The following script can be used to populate the Postgres Database given all the data is downloaded and converted into CSV. 

   ```initialize.sh ```

 The directory `/schema` contains the schema for all the tables in the database.
 
Airbyte is used to schedule data transfer data from PostgreSQL into BigQuery.


## Model Wrapper

`src/models/classifiers.py` contains the wrapper for the models.
The wrapper is used to train and test the models.

Here is the code for  an abstract class that implements the wrapper.

```python
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
```


## Dependencies

    $ pip install -r requirements.txt



## Running the pipeline

Before you run the pipeline PostgresQL must be populated with raw csv data. To do so please download the data from [**NYC Yellow Taxi Data**](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page) and make proper changes to the `initialize.sh` script.

    $ git clone repo.git
    $ cd repo
    
    load raw data -> clean data -> process data -> train model -> evaluate -> deployment

    $ python ./main/preprocess.py
    $ python ./main/feature_engineering.py
    $ python ./main/train_model.py
    $ python ./main/evaluation.py
    
    $ python ./inference/inference.py 

## Running the tests

    py.test tests
    
## License

Distributed under the MIT License. See `LICENSE.md` for more information.


## Contact

Vineet Verma - vineetver@hotmail.com - [Goodbyeweekend.io](https://www.goodbyeweekend.io/)

