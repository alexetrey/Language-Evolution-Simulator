"""
Personal Sleep Pattern Anomaly Detector - Data Generator
Generates realistic synthetic sleep data for testing and demonstration
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class SleepDataGenerator:
    def __init__(self):
        self.weekdays_bedtime = [22, 23, 23.5]  # 10 PM, 11 PM, 11:30 PM
        self.weekends_bedtime = [23.5, 24, 1, 1.5]  # 11:30 PM, 12 AM, 1 AM, 1:30 AM
        self.weekdays_wake = [6, 6.5, 7]  # 6 AM, 6:30 AM, 7 AM
        self.weekends_wake = [7.5, 8, 8.5, 9]  # 7:30 AM, 8 AM, 8:30 AM, 9 AM
        
    def generate_normal_sleep_data(self, days=90):
        """Generate normal sleep patterns"""
        data = []
        start_date = datetime.now() - timedelta(days=days)
        
        for i in range(days):
            current_date = start_date + timedelta(days=i)
            is_weekend = current_date.weekday() >= 5
            
            # Normal sleep patterns
            if is_weekend:
                bedtime_hour = random.choice(self.weekends_bedtime)
                wake_hour = random.choice(self.weekends_wake)
            else:
                bedtime_hour = random.choice(self.weekdays_bedtime)
                wake_hour = random.choice(self.weekdays_wake)
            
            # Calculate sleep duration (handle overnight sleep)
            if bedtime_hour > wake_hour:  # Sleep crosses midnight
                sleep_duration = (24 - bedtime_hour) + wake_hour
            else:  # Sleep within same day (shouldn't happen normally)
                sleep_duration = wake_hour - bedtime_hour
                
            # Ensure valid hour ranges (0-23)
            bedtime_hour = bedtime_hour % 24
            wake_hour = wake_hour % 24
            
            # Normal sleep quality (4-5 on 1-5 scale)
            sleep_quality = random.uniform(4.0, 5.0)
            
            data.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'bedtime': f"{int(bedtime_hour):02d}:{random.randint(0, 59):02d}",
                'wake_time': f"{int(wake_hour):02d}:{random.randint(0, 59):02d}",
                'sleep_duration': round(sleep_duration, 1),
                'sleep_quality': round(sleep_quality, 1),
                'is_weekend': is_weekend
            })
            
        return pd.DataFrame(data)
    
    def add_insomnia_episodes(self, df, num_episodes=3, episode_duration=5):
        """Add insomnia episodes to the data"""
        df_modified = df.copy()
        
        for _ in range(num_episodes):
            # Random start point for insomnia episode
            start_idx = random.randint(0, len(df) - episode_duration)
            
            for i in range(episode_duration):
                if start_idx + i < len(df_modified):
                    # Very late bedtime and early wake time
                    df_modified.loc[start_idx + i, 'bedtime'] = f"{random.randint(1, 3):02d}:{random.randint(0, 59):02d}"
                    df_modified.loc[start_idx + i, 'wake_time'] = f"{random.randint(5, 7):02d}:{random.randint(0, 59):02d}"
                    df_modified.loc[start_idx + i, 'sleep_duration'] = round(random.uniform(3.0, 5.0), 1)
                    df_modified.loc[start_idx + i, 'sleep_quality'] = round(random.uniform(1.0, 2.5), 1)
                    
        return df_modified
    
    def add_circadian_shift(self, df, shift_days=7, shift_amount=2):
        """Add circadian rhythm shift (gradual change in sleep schedule)"""
        df_modified = df.copy()
        
        # Find a random starting point
        start_idx = random.randint(10, len(df) - shift_days)
        
        for i in range(shift_days):
            if start_idx + i < len(df_modified):
                current_idx = start_idx + i
                
                # Get current bedtime and wake time
                current_bedtime = df_modified.loc[current_idx, 'bedtime']
                current_wake = df_modified.loc[current_idx, 'wake_time']
                
                # Parse times
                bed_hour, bed_min = map(int, current_bedtime.split(':'))
                wake_hour, wake_min = map(int, current_wake.split(':'))
                
                # Gradually shift later
                shift_hours = (shift_amount * i) / shift_days
                
                new_bed_hour = (bed_hour + shift_hours) % 24
                new_wake_hour = (wake_hour + shift_hours) % 24
                
                df_modified.loc[current_idx, 'bedtime'] = f"{int(new_bed_hour):02d}:{bed_min:02d}"
                df_modified.loc[current_idx, 'wake_time'] = f"{int(new_wake_hour):02d}:{wake_min:02d}"
                
                # Adjust sleep quality slightly during shift
                current_quality = df_modified.loc[current_idx, 'sleep_quality']
                df_modified.loc[current_idx, 'sleep_quality'] = round(max(2.0, current_quality - 0.5), 1)
                
        return df_modified
    
    def add_irregular_patterns(self, df, num_irregular_days=10):
        """Add random irregular sleep patterns"""
        df_modified = df.copy()
        
        irregular_indices = random.sample(range(len(df)), num_irregular_days)
        
        for idx in irregular_indices:
            # Random extreme bedtime and wake time
            bedtime_hour = random.randint(22, 23)  # Valid range 22-23
            wake_hour = random.randint(5, 10)
            
            df_modified.loc[idx, 'bedtime'] = f"{bedtime_hour:02d}:{random.randint(0, 59):02d}"
            df_modified.loc[idx, 'wake_time'] = f"{wake_hour:02d}:{random.randint(0, 59):02d}"
            df_modified.loc[idx, 'sleep_duration'] = round(random.uniform(4.0, 9.0), 1)
            df_modified.loc[idx, 'sleep_quality'] = round(random.uniform(2.0, 4.0), 1)
            
        return df_modified
    
    def generate_complete_dataset(self, days=90):
        """Generate a complete dataset with normal patterns and various anomalies"""
        print("Generating normal sleep patterns...")
        df = self.generate_normal_sleep_data(days)
        
        print("Adding insomnia episodes...")
        df = self.add_insomnia_episodes(df, num_episodes=2, episode_duration=4)
        
        print("Adding circadian shift...")
        df = self.add_circadian_shift(df, shift_days=6, shift_amount=1.5)
        
        print("Adding irregular patterns...")
        df = self.add_irregular_patterns(df, num_irregular_days=8)
        
        # Convert time strings to datetime objects for easier analysis
        df['bedtime_dt'] = pd.to_datetime(df['date'] + ' ' + df['bedtime'])
        df['wake_time_dt'] = pd.to_datetime(df['date'] + ' ' + df['wake_time'])
        
        # Add day of week
        df['day_of_week'] = pd.to_datetime(df['date']).dt.day_name()
        
        return df

# Production module - no test code needed
