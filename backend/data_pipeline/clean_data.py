
"""
Data Cleaner Module
Handles data validation, outlier detection, and cleaning operations
Maintains detailed logs of all exclusions and transformations
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

class DataCleaner:
    def __init__(self, log_dir='../data/logs'):
        self.log_dir = log_dir
        self.exclusion_log = []
        self.stats = {
            'original_count': 0,
            'final_count': 0,
            'excluded_by_reason': {}
        }
        
        # Create log directory if it doesn't exist
        os.makedirs(log_dir, exist_ok=True)
        
    def clean_trip_data(self, df):
        """
        Main cleaning pipeline for trip data
        
        Args:
            df: Raw trip dataframe
            
        Returns:
            Cleaned dataframe
        """
        print("\n" + "=" * 60)
        print("STARTING DATA CLEANING PIPELINE")
        print("=" * 60)
        
        self.stats['original_count'] = len(df)
        print(f"Original records: {len(df):,}")
        
        # Make a copy to avoid modifying original
        df_clean = df.copy()
        
        # 1. Remove duplicates
        df_clean = self._remove_duplicates(df_clean)
        
        # 2. Clean temporal data
        df_clean = self._clean_temporal_data(df_clean)
        
        # 3. Clean location data
        df_clean = self._clean_location_data(df_clean)
        
        # 4. Clean distance data
        df_clean = self._clean_distance_data(df_clean)
        
        # 5. Clean fare data
        df_clean = self._clean_fare_data(df_clean)
        
        # 6. Clean passenger count
        df_clean = self._clean_passenger_count(df_clean)
        
        # 7. Remove remaining nulls
        df_clean = self._handle_missing_values(df_clean)
        
        self.stats['final_count'] = len(df_clean)
        
        # Save exclusion log
        self._save_exclusion_log()
        
        # Print summary
        self._print_cleaning_summary()
        
        return df_clean
    
    def _remove_duplicates(self, df):
        """Remove duplicate records"""
        before = len(df)
        df = df.drop_duplicates()
        removed = before - len(df)
        
        if removed > 0:
            self._log_exclusion('duplicates', removed, "Exact duplicate records")
            print(f"✓ Removed {removed:,} duplicate records")
        
        return df
    
    def _clean_temporal_data(self, df):
        """Clean and validate temporal fields"""
        print("\nCleaning temporal data...")
        
        # Ensure datetime types
        datetime_cols = ['tpep_pickup_datetime', 'tpep_dropoff_datetime']
        for col in datetime_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Remove records with null timestamps
        before = len(df)
        df = df.dropna(subset=datetime_cols)
        removed = before - len(df)
        if removed > 0:
            self._log_exclusion('null_timestamp', removed, "Null pickup or dropoff timestamp")
        
        # Remove records where dropoff is before pickup
        before = len(df)
        df = df[df['tpep_dropoff_datetime'] > df['tpep_pickup_datetime']]
        removed = before - len(df)
        if removed > 0:
            self._log_exclusion('invalid_time_order', removed, "Dropoff before pickup")
        
        # Remove trips longer than 24 hours (likely errors)
        df['trip_duration_seconds'] = (df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']).dt.total_seconds()
        before = len(df)
        df = df[df['trip_duration_seconds'] <= 86400]  # 24 hours
        removed = before - len(df)
        if removed > 0:
            self._log_exclusion('excessive_duration', removed, "Trip duration > 24 hours")
        
        # Remove trips shorter than 1 minute (likely errors)
        before = len(df)
        df = df[df['trip_duration_seconds'] >= 60]
        removed = before - len(df)
        if removed > 0:
            self._log_exclusion('too_short_duration', removed, "Trip duration < 1 minute")
        
        print(f"✓ Temporal data cleaned")
        return df
    
    def _clean_location_data(self, df):
        """Clean and validate location IDs"""
        print("\nCleaning location data...")
        
        location_cols = ['PULocationID', 'DOLocationID']
        
        # Remove null locations
        before = len(df)
        df = df.dropna(subset=location_cols)
        removed = before - len(df)
        if removed > 0:
            self._log_exclusion('null_location', removed, "Null pickup or dropoff location")
        
        # LocationIDs should be positive integers (typically 1-263 for NYC)
        for col in location_cols:
            before = len(df)
            df = df[(df[col] > 0) & (df[col] <= 300)]  # Reasonable upper bound
            removed = before - len(df)
            if removed > 0:
                self._log_exclusion(f'invalid_{col}', removed, f"Invalid {col} value")
        
        print(f"✓ Location data cleaned")
        return df
    
    def _clean_distance_data(self, df):
        """Clean trip distance outliers"""
        print("\nCleaning distance data...")
        
        if 'trip_distance' not in df.columns:
            return df
        
        # Remove negative distances
        before = len(df)
        df = df[df['trip_distance'] >= 0]
        removed = before - len(df)
        if removed > 0:
            self._log_exclusion('negative_distance', removed, "Negative trip distance")
        
        # Remove unrealistic distances (> 200 miles)
        before = len(df)
        df = df[df['trip_distance'] <= 200]
        removed = before - len(df)
        if removed > 0:
            self._log_exclusion('excessive_distance', removed, "Trip distance > 200 miles")
        
        # Remove zero distance with significant duration (likely GPS errors)
        before = len(df)
        df = df[~((df['trip_distance'] == 0) & (df['trip_duration_seconds'] > 300))]
        removed = before - len(df)
        if removed > 0:
            self._log_exclusion('zero_distance_long_duration', removed, "Zero distance but long duration")
        
        print(f"✓ Distance data cleaned")
        return df
    
    def _clean_fare_data(self, df):
        """Clean fare-related outliers"""
        print("\nCleaning fare data...")
        
        fare_cols = ['fare_amount', 'total_amount']
        
        # Remove negative fares
        for col in fare_cols:
            if col in df.columns:
                before = len(df)
                df = df[df[col] >= 0]
                removed = before - len(df)
                if removed > 0:
                    self._log_exclusion(f'negative_{col}', removed, f"Negative {col}")
        
        # Remove unrealistic fares (> $500)
        if 'total_amount' in df.columns:
            before = len(df)
            df = df[df['total_amount'] <= 500]
            removed = before - len(df)
            if removed > 0:
                self._log_exclusion('excessive_fare', removed, "Total amount > $500")
        
        # Remove zero fare with significant distance (likely errors)
        if 'fare_amount' in df.columns and 'trip_distance' in df.columns:
            before = len(df)
            df = df[~((df['fare_amount'] == 0) & (df['trip_distance'] > 1))]
            removed = before - len(df)
            if removed > 0:
                self._log_exclusion('zero_fare_with_distance', removed, "Zero fare but significant distance")
        
        print(f"✓ Fare data cleaned")
        return df
    
    def _clean_passenger_count(self, df):
        """Clean passenger count data"""
        print("\nCleaning passenger count...")
        
        if 'passenger_count' not in df.columns:
            return df
        
        # Passenger count should be 1-6 (taxi capacity)
        before = len(df)
        df = df[(df['passenger_count'] >= 1) & (df['passenger_count'] <= 6)]
        removed = before - len(df)
        if removed > 0:
            self._log_exclusion('invalid_passenger_count', removed, "Passenger count not between 1-6")
        
        print(f"✓ Passenger count cleaned")
        return df
    
    def _handle_missing_values(self, df):
        """Handle remaining missing values"""
        print("\nHandling missing values...")
        
        # Count nulls per column
        null_counts = df.isnull().sum()
        
        # For critical columns, remove rows with nulls
        critical_cols = [
            'tpep_pickup_datetime', 'tpep_dropoff_datetime',
            'PULocationID', 'DOLocationID',
            'trip_distance', 'fare_amount', 'total_amount'
        ]
        
        critical_cols = [col for col in critical_cols if col in df.columns]
        
        before = len(df)
        df = df.dropna(subset=critical_cols)
        removed = before - len(df)
        
        if removed > 0:
            self._log_exclusion('missing_critical_values', removed, "Missing values in critical columns")
        
        print(f"✓ Missing values handled")
        return df
    
    def _log_exclusion(self, reason, count, description):
        """Log excluded records"""
        self.exclusion_log.append({
            'reason': reason,
            'count': count,
            'description': description,
            'timestamp': datetime.now()
        })
        
        if reason not in self.stats['excluded_by_reason']:
            self.stats['excluded_by_reason'][reason] = 0
        self.stats['excluded_by_reason'][reason] += count
    
    def _save_exclusion_log(self):
        """Save exclusion log to file"""
        log_file = os.path.join(self.log_dir, f'excluded_records_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        
        with open(log_file, 'w') as f:
            f.write("NYC TAXI DATA CLEANING - EXCLUSION LOG\n")
            f.write("=" * 80 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Original Records: {self.stats['original_count']:,}\n")
            f.write(f"Final Records: {self.stats['final_count']:,}\n")
            f.write(f"Total Excluded: {self.stats['original_count'] - self.stats['final_count']:,}\n")
            f.write("=" * 80 + "\n\n")
            
            f.write("EXCLUSIONS BY REASON:\n")
            f.write("-" * 80 + "\n")
            
            for entry in self.exclusion_log:
                f.write(f"\n{entry['reason'].upper()}\n")
                f.write(f"  Count: {entry['count']:,}\n")
                f.write(f"  Description: {entry['description']}\n")
                f.write(f"  Timestamp: {entry['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        print(f"\n✓ Exclusion log saved to: {log_file}")
    
    def _print_cleaning_summary(self):
        """Print summary of cleaning operations"""
        print("\n" + "=" * 60)
        print("DATA CLEANING SUMMARY")
        print("=" * 60)
        
        print(f"Original records:  {self.stats['original_count']:>12,}")
        print(f"Final records:     {self.stats['final_count']:>12,}")
        print(f"Excluded records:  {self.stats['original_count'] - self.stats['final_count']:>12,}")
        print(f"Retention rate:    {(self.stats['final_count'] / self.stats['original_count'] * 100):>11.2f}%")
        
        print("\nExclusions by reason:")
        for reason, count in sorted(self.stats['excluded_by_reason'].items(), key=lambda x: x[1], reverse=True):
            percentage = (count / self.stats['original_count']) * 100
            print(f"  {reason:.<40} {count:>8,} ({percentage:>5.2f}%)")


if __name__ == "__main__":
    # Test the cleaner
    from data_loader import DataLoader
    
    loader = DataLoader()
    trips, _, _ = loader.load_all(sample_size=10000)
    
    cleaner = DataCleaner()
    cleaned_trips = cleaner.clean_trip_data(trips)
    
    print(f"\nCleaned data shape: {cleaned_trips.shape}")

