"""
Data Loader Module
Loads raw NYC Taxi data from CSV, Parquet, and spatial files
"""

import pandas as pd
import geopandas as gpd
import json
import os
from typing import Optional, Tuple

print("Script started...")


class DataLoader:
    def __init__(self, data_dir: Optional[str] = None):
        if data_dir is None:
            # Set data_dir relative to this script's location
            self.data_dir = os.path.abspath(
                os.path.join(os.path.dirname(__file__), '../../data/raw')
            )
        else:
            self.data_dir = data_dir

        self.trip_data = None
        self.zone_lookup = None
        self.zone_geometries = None

    # ==========================================================
    # TRIP DATA
    # ==========================================================
    def load_trip_data(
        self,
        filename: str = 'yellow_tripdata_2019-01.csv',
        sample_size: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Load trip data from CSV or Parquet file
        """

        filepath = os.path.join(self.data_dir, filename)
        print(f"Loading trip data from {filepath}...")

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Trip data file not found: {filepath}")

        # Load based on file extension
        if filename.endswith('.parquet'):
            df = pd.read_parquet(filepath)
        elif filename.endswith('.csv'):
            df = pd.read_csv(
                filepath,
                low_memory=False,
                parse_dates=[
                    "tpep_pickup_datetime",
                    "tpep_dropoff_datetime"
                ]
            )
        else:
            raise ValueError('Unsupported file format for trip data')

        if sample_size:
            df = df.head(sample_size)
            print(f"Loaded {len(df)} rows (sample)")
        else:
            print(f"Loaded {len(df)} rows (full dataset)")

        self.trip_data = df

        print(f"Columns: {list(df.columns)}")
        print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

        return df

    # ==========================================================
    # ZONE LOOKUP TABLE
    # ==========================================================
    def load_zone_lookup(self, filename: str = 'taxi_zone_lookup.csv') -> pd.DataFrame:
        """
        Load taxi zone lookup table (Borough and Service Zone mapping)
        """

        filepath = os.path.join(self.data_dir, filename)
        print(f"Loading zone lookup from {filepath}...")

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Zone lookup file not found: {filepath}")

        self.zone_lookup = pd.read_csv(filepath)

        print(f"Loaded {len(self.zone_lookup)} taxi zones")
        print(f"Unique Boroughs: {self.zone_lookup['Borough'].nunique()}")

        return self.zone_lookup

    # ==========================================================
    # ZONE GEOMETRIES (Shapefile or GeoJSON)
    # ==========================================================
    def load_zone_geometries(self) -> gpd.GeoDataFrame:
        """
        Load spatial boundaries for taxi zones.
        Supports:
        - taxi_zones folder containing shapefile
        - taxi_zones.geojson file
        """

        print("Loading zone geometries...")

        # First check for GeoJSON file
        geojson_path = os.path.join(self.data_dir, "taxi_zones.geojson")

        if os.path.exists(geojson_path):
            print(f"Found GeoJSON: {geojson_path}")
            self.zone_geometries = gpd.read_file(geojson_path)
            print(f"Loaded {len(self.zone_geometries)} zone geometries (GeoJSON)")
            return self.zone_geometries

        # Otherwise check for shapefile folder
        shapefile_folder = os.path.join(self.data_dir, "taxi_zones")

        if os.path.exists(shapefile_folder):
            shp_files = [
                f for f in os.listdir(shapefile_folder)
                if f.endswith(".shp")
            ]

            if not shp_files:
                raise FileNotFoundError(
                    "No .shp file found inside taxi_zones folder"
                )

            shp_path = os.path.join(shapefile_folder, shp_files[0])

            print(f"Found Shapefile: {shp_path}")

            self.zone_geometries = gpd.read_file(shp_path)

            print(f"Loaded {len(self.zone_geometries)} zone geometries (Shapefile)")
            return self.zone_geometries

        raise FileNotFoundError(
            "No taxi_zones.geojson file or taxi_zones shapefile folder found in raw directory"
        )

    # ==========================================================
    # LOAD ALL
    # ==========================================================
    def load_all(
        self,
        sample_size: Optional[int] = None
    ) -> Tuple[pd.DataFrame, pd.DataFrame, gpd.GeoDataFrame]:

        print("=" * 60)
        print("LOADING ALL DATA FILES")
        print("=" * 60)

        trips = self.load_trip_data(sample_size=sample_size)
        zones = self.load_zone_lookup()
        geometries = self.load_zone_geometries()

        print("\n✓ All data files loaded successfully!")

        #merged_data = trips.merge(zones,
         #   left_on = "PULocationID",
          #  right_on = "LocationID",
           # how = "left"
        #)
        #print(f"Integration complete: {merged_data.shape[0]} rows, {merged_data.shape[1]} columns")




        return trips, zones, geometries
    
   # merged_data = trips.merge(zones
                 



    # ==========================================================
    # SUMMARY
    # ==========================================================
    def get_data_summary(self):
        """Print summary statistics of loaded data"""

        if self.trip_data is None:
            print("No trip data loaded yet")
            return

        print("\n" + "=" * 60)
        print("DATA SUMMARY")
        print("=" * 60)

        print(f"\nTrip Data Shape: {self.trip_data.shape}")

        print("\nColumn Data Types:")
        print(self.trip_data.dtypes)

        print("\nMissing Values:")
        print(self.trip_data.isnull().sum())

        #print("merge data:")
        #print(self.merged_data)

        print("\nBasic Statistics:")
        print(self.trip_data.describe())

        if self.zone_lookup is not None:
            print(f"\nZone Lookup Shape: {self.zone_lookup.shape}")
            print(f"Unique Boroughs: {self.zone_lookup['Borough'].nunique()}")

        if self.zone_geometries is not None:
            print(f"\nZone Geometries Shape: {self.zone_geometries.shape}")


# ==========================================================
# TESTING
# ==========================================================
if __name__ == "__main__":
    print("Inside main block...")

    loader = DataLoader()

    trips, zones, geometries = loader.load_all(sample_size=10000)


    print("\nTop 5 Trips:")
    print(trips.head())

    print("\nTop 5 Zones:")
    print(zones.head())

    print("\nTop 5 Geometries:")
    print(geometries.head())




    loader.get_data_summary()
    
    

