import pytest
from mars_rover_pipeline.cleaning import clean_rover_data
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder.master("local[*]").appName("TestCleaning").getOrCreate()


def test_clean_rover_data_removes_invalid_and_duplicates(spark):
    test_data = [
        {
            "timestamp": "2024-11-20T14:23:05Z",
            "vehicle_id": "Rover-1",
            "temperature": -63.5,
            "position": {"x": 34.56, "y": -117.34, "z": 5.0},
        },
        {
            "timestamp": "2024-11-20T14:23:05Z",  # Duplicate
            "vehicle_id": "Rover-1",
            "temperature": -63.5,
            "position": {"x": 34.56, "y": -117.34, "z": 5.0},
        },
        {
            "timestamp": "2024-11-21T14:23:05Z",
            "vehicle_id": "Rover-2",
            "temperature": -200.0,  # Invalid temperature
            "position": {"x": 12.3, "y": 45.6, "z": 0.0},
        },
        {
            "timestamp": "2024-11-22T14:23:05Z",
            "vehicle_id": "Rover-3",
            "temperature": 20.0,
            "position": None,  # Missing position
        },
    ]

    df = spark.read.json(spark.sparkContext.parallelize(test_data, 1))
    cleaned_df = clean_rover_data(df)

    vehicle_ids = [
        row["vehicle_id"] for row in cleaned_df.select("vehicle_id").collect()
    ]
    assert vehicle_ids == ["Rover-1"]
