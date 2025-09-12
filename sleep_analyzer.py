
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from scipy import stats
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class SleepAnalyzer:
    def __init__(self):
        self.baseline_stats = {}
        self.anomaly_thresholds = {
            'sleep_duration': {'low': 6, 'high': 9},
            'sleep_quality': {'low': 3.0, 'high': 5.0},
            'bedtime_variance': {'threshold': 2.0},  # hours
            'wake_variance': {'threshold': 1.5}  # hours
        }
        
    def extract_time_features(self, df):
        """Extract numerical features from time data"""
        df_features = df.copy()
        
        # Convert bedtime and wake time to hours since midnight
        df_features['bedtime_hour'] = df_features['bedtime_dt'].dt.hour + df_features['bedtime_dt'].dt.minute / 60
        df_features['wake_hour'] = df_features['wake_time_dt'].dt.hour + df_features['wake_time_dt'].dt.minute / 60
        
        # Handle bedtime after midnight (next day)
        df_features.loc[df_features['bedtime_hour'] < 12, 'bedtime_hour'] += 24
        
        # Calculate sleep efficiency (sleep duration / time in bed)
        df_features['time_in_bed'] = 24 - (df_features['bedtime_hour'] - df_features['wake_hour'])
        df_features['sleep_efficiency'] = df_features['sleep_duration'] / df_features['time_in_bed']
        
        # Day of week as numeric (0=Monday, 6=Sunday)
        df_features['day_of_week_num'] = pd.to_datetime(df_features['date']).dt.dayofweek
        
        return df_features
    
    def calculate_baseline_stats(self, df):
        """Calculate baseline statistics for normal sleep patterns"""
        df_features = self.extract_time_features(df)
        
        # Separate weekday and weekend data
        weekdays = df_features[df_features['is_weekend'] == False]
        weekends = df_features[df_features['is_weekend'] == True]
        
        self.baseline_stats = {
            'weekdays': {
                'avg_bedtime': weekdays['bedtime_hour'].mean(),
                'std_bedtime': weekdays['bedtime_hour'].std(),
                'avg_wake': weekdays['wake_hour'].mean(),
                'std_wake': weekdays['wake_hour'].std(),
                'avg_duration': weekdays['sleep_duration'].mean(),
                'std_duration': weekdays['sleep_duration'].std(),
                'avg_quality': weekdays['sleep_quality'].mean(),
                'std_quality': weekdays['sleep_quality'].std(),
                'avg_efficiency': weekdays['sleep_efficiency'].mean(),
                'std_efficiency': weekdays['sleep_efficiency'].std()
            },
            'weekends': {
                'avg_bedtime': weekends['bedtime_hour'].mean(),
                'std_bedtime': weekends['bedtime_hour'].std(),
                'avg_wake': weekends['wake_hour'].mean(),
                'std_wake': weekends['wake_hour'].std(),
                'avg_duration': weekends['sleep_duration'].mean(),
                'std_duration': weekends['sleep_duration'].std(),
                'avg_quality': weekends['sleep_quality'].mean(),
                'std_quality': weekends['sleep_quality'].std(),
                'avg_efficiency': weekends['sleep_efficiency'].mean(),
                'std_efficiency': weekends['sleep_efficiency'].std()
            },
            'overall': {
                'avg_bedtime': df_features['bedtime_hour'].mean(),
                'std_bedtime': df_features['bedtime_hour'].std(),
                'avg_wake': df_features['wake_hour'].mean(),
                'std_wake': df_features['wake_hour'].std(),
                'avg_duration': df_features['sleep_duration'].mean(),
                'std_duration': df_features['sleep_duration'].std(),
                'avg_quality': df_features['sleep_quality'].mean(),
                'std_quality': df_features['sleep_quality'].std(),
                'avg_efficiency': df_features['sleep_efficiency'].mean(),
                'std_efficiency': df_features['sleep_efficiency'].std()
            }
        }
        
        return df_features
    
    def detect_statistical_anomalies(self, df):
        """Detect anomalies using statistical methods"""
        df_features = self.calculate_baseline_stats(df)
        anomalies = []
        
        for idx, row in df_features.iterrows():
            is_weekend = row['is_weekend']
            baseline = self.baseline_stats['weekends' if is_weekend else 'weekdays']
            
            anomaly_flags = []
            
            # Sleep duration anomalies
            if row['sleep_duration'] < self.anomaly_thresholds['sleep_duration']['low']:
                anomaly_flags.append('insufficient_sleep')
            elif row['sleep_duration'] > self.anomaly_thresholds['sleep_duration']['high']:
                anomaly_flags.append('excessive_sleep')
            
            # Sleep quality anomalies
            if row['sleep_quality'] < self.anomaly_thresholds['sleep_quality']['low']:
                anomaly_flags.append('poor_sleep_quality')
            
            # Bedtime consistency (more than 2 hours from baseline)
            if abs(row['bedtime_hour'] - baseline['avg_bedtime']) > self.anomaly_thresholds['bedtime_variance']['threshold']:
                anomaly_flags.append('irregular_bedtime')
            
            # Wake time consistency
            if abs(row['wake_hour'] - baseline['avg_wake']) > self.anomaly_thresholds['wake_variance']['threshold']:
                anomaly_flags.append('irregular_wake_time')
            
            # Sleep efficiency
            if row['sleep_efficiency'] < 0.8:  # Less than 80% efficiency
                anomaly_flags.append('low_sleep_efficiency')
            
            if anomaly_flags:
                anomalies.append({
                    'date': row['date'],
                    'anomaly_types': anomaly_flags,
                    'sleep_duration': row['sleep_duration'],
                    'sleep_quality': row['sleep_quality'],
                    'bedtime_hour': row['bedtime_hour'],
                    'wake_hour': row['wake_hour'],
                    'sleep_efficiency': row['sleep_efficiency'],
                    'is_weekend': is_weekend
                })
        
        return pd.DataFrame(anomalies)
    
    def detect_machine_learning_anomalies(self, df):
        """Detect anomalies using statistical methods (Isolation Forest)"""
        df_features = self.calculate_baseline_stats(df)
        
        # Prepare features for analysis
        feature_columns = ['bedtime_hour', 'wake_hour', 'sleep_duration', 'sleep_quality', 'sleep_efficiency', 'day_of_week_num']
        X = df_features[feature_columns].values
        
        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Use statistical method for anomaly detection
        iso_forest = IsolationForest(contamination=0.1, random_state=42)
        anomaly_labels = iso_forest.fit_predict(X_scaled)
        
        # Get anomaly scores
        anomaly_scores = iso_forest.decision_function(X_scaled)
        
        # Create results dataframe
        df_features['ml_anomaly'] = anomaly_labels == -1
        df_features['anomaly_score'] = anomaly_scores
        
        # Filter anomalies
        ml_anomalies = df_features[df_features['ml_anomaly']].copy()
        
        return ml_anomalies, df_features
    
    def detect_pattern_anomalies(self, df):
        """Detect pattern-based anomalies like circadian shifts and insomnia episodes"""
        df_features = self.calculate_baseline_stats(df)
        pattern_anomalies = []
        
        # Detect insomnia episodes (consecutive days with poor sleep)
        insomnia_threshold = 3  # consecutive days
        poor_sleep_days = df_features[
            (df_features['sleep_duration'] < 5.5) | 
            (df_features['sleep_quality'] < 3.0)
        ].index.tolist()
        
        # Find consecutive sequences
        insomnia_episodes = []
        if poor_sleep_days:
            current_episode = [poor_sleep_days[0]]
            for i in range(1, len(poor_sleep_days)):
                if poor_sleep_days[i] == poor_sleep_days[i-1] + 1:
                    current_episode.append(poor_sleep_days[i])
                else:
                    if len(current_episode) >= insomnia_threshold:
                        insomnia_episodes.append(current_episode)
                    current_episode = [poor_sleep_days[i]]
            
            if len(current_episode) >= insomnia_threshold:
                insomnia_episodes.append(current_episode)
        
        # Detect circadian shifts (gradual change in sleep schedule)
        window_size = 7
        circadian_shifts = []
        
        for i in range(window_size, len(df_features) - window_size):
            # Compare bedtime patterns
            before_window = df_features.iloc[i-window_size:i]['bedtime_hour']
            after_window = df_features.iloc[i:i+window_size]['bedtime_hour']
            
            before_avg = before_window.mean()
            after_avg = after_window.mean()
            
            # Significant shift (> 1 hour average change)
            if abs(after_avg - before_avg) > 1.0:
                circadian_shifts.append({
                    'start_date': df_features.iloc[i]['date'],
                    'shift_magnitude': after_avg - before_avg,
                    'before_avg_bedtime': before_avg,
                    'after_avg_bedtime': after_avg
                })
        
        return insomnia_episodes, circadian_shifts
    
    def generate_anomaly_report(self, df):
        """Generate comprehensive anomaly detection report"""
        print("Analyzing sleep patterns for anomalies...")
        
        # Statistical anomalies
        stat_anomalies = self.detect_statistical_anomalies(df)
        print(f"Found {len(stat_anomalies)} statistical anomalies")
        
        # Advanced statistical anomalies
        ml_anomalies, df_with_scores = self.detect_machine_learning_anomalies(df)
        print(f"Found {len(ml_anomalies)} statistically-detected anomalies")
        
        # Pattern anomalies
        insomnia_episodes, circadian_shifts = self.detect_pattern_anomalies(df)
        print(f"Found {len(insomnia_episodes)} insomnia episodes")
        print(f"Found {len(circadian_shifts)} circadian shifts")
        
        # Summary statistics
        summary = {
            'total_days': len(df),
            'statistical_anomalies': len(stat_anomalies),
            'ml_anomalies': len(ml_anomalies),
            'insomnia_episodes': len(insomnia_episodes),
            'circadian_shifts': len(circadian_shifts),
            'baseline_stats': self.baseline_stats
        }
        
        return {
            'statistical_anomalies': stat_anomalies,
            'ml_anomalies': ml_anomalies,
            'insomnia_episodes': insomnia_episodes,
            'circadian_shifts': circadian_shifts,
            'summary': summary,
            'df_with_scores': df_with_scores
        }

