# Feast feature schema configuration definition
from datetime import timedelta
from feast import Entity, FeatureView, Field, FileSource
from feast.types import Float32, Int64

# Define raw parquet file source
driver_stats_source = FileSource(
    path="/tmp/feast-lab/my_feature_repository/data/driver_stats.parquet",
    event_timestamp_column="datetime",
    created_timestamp_column="created",
)

# Define entity
driver = Entity(name="driver_id", value_type=Int64, description="driver id")

# Define feature view
driver_stats_view = FeatureView(
    name="driver_stats",
    entities=[driver],
    ttl=timedelta(days=90),
    schema=[
        Field(name="conv_rate", dtype=Float32),
        Field(name="acc_rate", dtype=Float32),
    ],
    online=True,
    source=driver_stats_source,
)
