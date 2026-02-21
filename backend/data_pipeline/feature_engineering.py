"""
Feature Engineering Module
Creates derived features from the merged trip dataset
"""

import pandas as pd
import numpy as np

class FeatureEngineer:
    def __init__(self):
        self.features_created = []

    def engineer_features(self, df):
        """
        Main feature engineering pipeline using merged trips directly.
        
        Args:
            df: Merged trip dataframe (cleaned and merged with zones and geometries)
            
        Returns:
            DataFrame with engineered features
        """
        df = df.copy()
        
        # -----------------------------
        # 1. Temporal features
        # -----------------------------
        df['pickup_hour'] = df['tpep_pickup_datetime'].dt.hour
        df['pickup_day_of_week'] = df['tpep_pickup_datetime'].dt.dayofweek
        df['pickup_day_name'] = df['tpep_pickup_datetime'].dt.day_name()
        df['pickup_month'] = df['tpep_pickup_datetime'].dt.month
        df['is_weekend'] = df['pickup_day_of_week'].isin([5,6]).astype(int)
        
        # Time of day
        def time_of_day(hour):
            if 6 <= hour < 12: return 'Morning'
            elif 12 <= hour < 17: return 'Afternoon'
            elif 17 <= hour < 21: return 'Evening'
            else: return 'Night'
        df['time_of_day'] = df['pickup_hour'].apply(time_of_day)
        
        # Rush hour (weekday 7-9AM & 5-7PM)
        def is_rush(row):
            dow = row['pickup_day_of_week']
            h = row['pickup_hour']
            if dow < 5 and ((7 <= h <= 9) or (17 <= h <= 19)):
                return 1
            return 0
        df['is_rush_hour'] = df.apply(is_rush, axis=1)
        
        self.features_created.extend([
            'pickup_hour', 'pickup_day_of_week', 'pickup_day_name',
            'pickup_month', 'is_weekend', 'time_of_day', 'is_rush_hour'
        ])
        
        # -----------------------------
        # 2. Trip duration features
        # -----------------------------
        df['trip_duration_seconds'] = (df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']).dt.total_seconds()
        df['trip_duration_minutes'] = df['trip_duration_seconds'] / 60
        self.features_created.extend(['trip_duration_seconds', 'trip_duration_minutes'])
        
        # -----------------------------
        # 3. Fare and efficiency features
        # -----------------------------
        df['fare_per_mile'] = (df['fare_amount'] / df['trip_distance'].replace({0: np.nan})).fillna(0)
        df['revenue_per_minute'] = (df['total_amount'] / df['trip_duration_minutes'].replace({0: np.nan})).fillna(0)
        df['has_surcharge'] = (df['extra'] > 0).astype(int) if 'extra' in df.columns else 0
        
        # Tip features
        if 'tip_amount' in df.columns and 'fare_amount' in df.columns:
            df['tip_percentage'] = (df['tip_amount'] / df['fare_amount'] * 100).replace([np.inf, -np.inf], 0).fillna(0)
            def tip_category(t):
                if t == 0: return 'No Tip'
                elif t < 15: return 'Low Tip'
                elif t < 20: return 'Standard Tip'
                else: return 'Generous Tip'
            df['tip_category'] = df['tip_percentage'].apply(tip_category)
        
        self.features_created.extend([
            'fare_per_mile', 'revenue_per_minute', 'has_surcharge', 'tip_percentage', 'tip_category'
        ])
        
        # -----------------------------
        # 4. Trip characteristic features
        # -----------------------------
        # Average speed
        df['average_speed_mph'] = (df['trip_distance'] / (df['trip_duration_seconds']/3600)).replace([np.inf, -np.inf], 0)
        df.loc[df['trip_duration_seconds']==0, 'average_speed_mph'] = 0
        df.loc[df['average_speed_mph']>80, 'average_speed_mph'] = 80
        
        # Distance categories
        def distance_category(dist):
            if dist < 1: return 'Very Short (<1 mi)'
            elif dist < 3: return 'Short (1-3 mi)'
            elif dist < 10: return 'Medium (3-10 mi)'
            else: return 'Long (>10 mi)'
        df['distance_category'] = df['trip_distance'].apply(distance_category)
        
        # Duration categories
        def duration_category(mins):
            if mins < 10: return 'Quick (<10 min)'
            elif mins < 20: return 'Short (10-20 min)'
            elif mins < 40: return 'Medium (20-40 min)'
            else: return 'Long (>40 min)'
        df['duration_category'] = df['trip_duration_minutes'].apply(duration_category)
        
        # Congestion indicator
        df['is_congested'] = (df['average_speed_mph'] < 10).astype(int)
        
        self.features_created.extend([
            'average_speed_mph', 'distance_category', 'duration_category', 'is_congested'
        ])
        
        # -----------------------------
        # 5. Location-based features (already merged)
        # -----------------------------
        if 'pickup_borough' in df.columns and 'dropoff_borough' in df.columns:
            df['is_inter_borough'] = (df['pickup_borough'] != df['dropoff_borough']).astype(int)
            df['from_manhattan'] = (df['pickup_borough'] == 'Manhattan').astype(int)
            df['to_manhattan'] = (df['dropoff_borough'] == 'Manhattan').astype(int)
        
        if 'pickup_zone' in df.columns and 'dropoff_zone' in df.columns:
            airport_keywords = ['Airport','JFK','LaGuardia','Newark']
            df['from_airport'] = df['pickup_zone'].apply(lambda x: 1 if isinstance(x,str) and any(k in x for k in airport_keywords) else 0)
            df['to_airport'] = df['dropoff_zone'].apply(lambda x: 1 if isinstance(x,str) and any(k in x for k in airport_keywords) else 0)
        
        self.features_created.extend([
            'is_inter_borough','from_manhattan','to_manhattan','from_airport','to_airport'
        ])
        
        return df

    def summary(self):
        print(f"Total features created: {len(self.features_created)}")
        print(self.features_created)

