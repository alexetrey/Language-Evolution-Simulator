"""
Personal Sleep Pattern Anomaly Detector - Visualization Engine
Creates professional charts and interactive dashboards for sleep analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

class SleepVisualizer:
    def __init__(self):
        plt.style.use('seaborn-v0_8')
        self.colors = {
            'normal': '#2E8B57',
            'anomaly': '#DC143C',
            'insomnia': '#8B0000',
            'circadian': '#FF8C00',
            'background': '#F5F5F5'
        }
        
    def create_sleep_timeline(self, df, anomalies=None, save_path=None, fig=None):
        """Create a comprehensive sleep timeline visualization"""
        if fig is None:
            fig, axes = plt.subplots(4, 1, figsize=(15, 12))
        else:
            axes = fig.axes if hasattr(fig, 'axes') else None
        fig.suptitle('Sleep Pattern Analysis Timeline', fontsize=16, fontweight='bold')
        
        # Convert date to datetime for plotting
        df['date_dt'] = pd.to_datetime(df['date'])
        
        # Plot 1: Sleep Duration
        axes[0].plot(df['date_dt'], df['sleep_duration'], 'o-', color=self.colors['normal'], 
                     markersize=4, linewidth=1.5, label='Sleep Duration')
        axes[0].axhline(y=7, color='gray', linestyle='--', alpha=0.7, label='Recommended 7-9h')
        axes[0].axhline(y=9, color='gray', linestyle='--', alpha=0.7)
        axes[0].fill_between(df['date_dt'], 6, 9, alpha=0.1, color='green', label='Healthy Range')
        
        if anomalies is not None and 'statistical_anomalies' in anomalies:
            anomaly_dates = pd.to_datetime(anomalies['statistical_anomalies']['date'])
            anomaly_durations = anomalies['statistical_anomalies']['sleep_duration']
            axes[0].scatter(anomaly_dates, anomaly_durations, color=self.colors['anomaly'], 
                           s=60, marker='x', label='Anomalies', zorder=5)
        
        axes[0].set_title('Sleep Duration Over Time', fontweight='bold')
        axes[0].set_ylabel('Hours')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Plot 2: Sleep Quality
        axes[1].plot(df['date_dt'], df['sleep_quality'], 'o-', color=self.colors['normal'], 
                     markersize=4, linewidth=1.5, label='Sleep Quality')
        axes[1].axhline(y=4, color='gray', linestyle='--', alpha=0.7, label='Good Quality Threshold')
        axes[1].fill_between(df['date_dt'], 4, 5, alpha=0.1, color='green', label='Good Quality Range')
        
        if anomalies is not None and 'statistical_anomalies' in anomalies:
            anomaly_qualities = anomalies['statistical_anomalies']['sleep_quality']
            axes[1].scatter(anomaly_dates, anomaly_qualities, color=self.colors['anomaly'], 
                           s=60, marker='x', label='Anomalies', zorder=5)
        
        axes[1].set_title('Sleep Quality Over Time', fontweight='bold')
        axes[1].set_ylabel('Quality (1-5)')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        # Plot 3: Bedtime and Wake Time
        axes[2].plot(df['date_dt'], df['bedtime_dt'].dt.hour + df['bedtime_dt'].dt.minute/60, 
                     'o-', color='blue', markersize=4, linewidth=1.5, label='Bedtime')
        axes[2].plot(df['date_dt'], df['wake_time_dt'].dt.hour + df['wake_time_dt'].dt.minute/60, 
                     'o-', color='orange', markersize=4, linewidth=1.5, label='Wake Time')
        axes[2].axhline(y=23, color='blue', linestyle='--', alpha=0.5, label='Recommended Bedtime')
        axes[2].axhline(y=7, color='orange', linestyle='--', alpha=0.5, label='Recommended Wake')
        
        axes[2].set_title('Bedtime and Wake Time Patterns', fontweight='bold')
        axes[2].set_ylabel('Hour of Day')
        axes[2].legend()
        axes[2].grid(True, alpha=0.3)
        
        # Plot 4: Weekend vs Weekday Comparison
        weekend_data = df[df['is_weekend'] == True]
        weekday_data = df[df['is_weekend'] == False]
        
        axes[3].scatter(weekday_data['date_dt'], weekday_data['sleep_duration'], 
                       color='lightblue', alpha=0.6, s=30, label='Weekdays')
        axes[3].scatter(weekend_data['date_dt'], weekend_data['sleep_duration'], 
                       color='lightcoral', alpha=0.6, s=30, label='Weekends')
        
        axes[3].set_title('Weekday vs Weekend Sleep Duration', fontweight='bold')
        axes[3].set_ylabel('Sleep Duration (Hours)')
        axes[3].set_xlabel('Date')
        axes[3].legend()
        axes[3].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
    def create_anomaly_heatmap(self, anomalies, save_path=None, fig=None):
        """Create a heatmap showing anomaly patterns"""
        if anomalies is None or len(anomalies.get('statistical_anomalies', [])) == 0:
            print("No anomalies to visualize")
            return
            
        anomaly_df = anomalies['statistical_anomalies'].copy()
        anomaly_df['date'] = pd.to_datetime(anomaly_df['date'])
        anomaly_df['day_of_week'] = anomaly_df['date'].dt.day_name()
        anomaly_df['week_number'] = anomaly_df['date'].dt.isocalendar().week
        
        # Create pivot table for heatmap
        heatmap_data = anomaly_df.groupby(['day_of_week', 'week_number']).size().unstack(fill_value=0)
        
        # Reorder days of week
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        heatmap_data = heatmap_data.reindex(day_order)
        
        plt.figure(figsize=(12, 6))
        sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='Reds', 
                   cbar_kws={'label': 'Number of Anomalies'})
        plt.title('Sleep Anomaly Distribution by Day of Week and Week', fontweight='bold')
        plt.xlabel('Week Number')
        plt.ylabel('Day of Week')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
    def create_sleep_quality_distribution(self, df, save_path=None, fig=None):
        """Create distribution plots for sleep metrics"""
        if fig is None:
            fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        else:
            axes = fig.axes if hasattr(fig, 'axes') else None
        fig.suptitle('Sleep Pattern Distributions', fontsize=16, fontweight='bold')
        
        # Sleep Duration Distribution
        axes[0, 0].hist(df['sleep_duration'], bins=20, color=self.colors['normal'], alpha=0.7, edgecolor='black')
        axes[0, 0].axvline(df['sleep_duration'].mean(), color='red', linestyle='--', 
                          label=f'Mean: {df["sleep_duration"].mean():.1f}h')
        axes[0, 0].set_title('Sleep Duration Distribution')
        axes[0, 0].set_xlabel('Hours')
        axes[0, 0].set_ylabel('Frequency')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Sleep Quality Distribution
        axes[0, 1].hist(df['sleep_quality'], bins=15, color=self.colors['normal'], alpha=0.7, edgecolor='black')
        axes[0, 1].axvline(df['sleep_quality'].mean(), color='red', linestyle='--', 
                          label=f'Mean: {df["sleep_quality"].mean():.1f}')
        axes[0, 1].set_title('Sleep Quality Distribution')
        axes[0, 1].set_xlabel('Quality Score')
        axes[0, 1].set_ylabel('Frequency')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # Weekday vs Weekend Comparison
        weekend_duration = df[df['is_weekend'] == True]['sleep_duration']
        weekday_duration = df[df['is_weekend'] == False]['sleep_duration']
        
        axes[1, 0].hist([weekday_duration, weekend_duration], bins=15, alpha=0.7, 
                       label=['Weekdays', 'Weekends'], color=['lightblue', 'lightcoral'])
        axes[1, 0].set_title('Sleep Duration: Weekdays vs Weekends')
        axes[1, 0].set_xlabel('Hours')
        axes[1, 0].set_ylabel('Frequency')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # Bedtime Distribution
        bedtime_hours = df['bedtime_dt'].dt.hour + df['bedtime_dt'].dt.minute/60
        axes[1, 1].hist(bedtime_hours, bins=20, color=self.colors['normal'], alpha=0.7, edgecolor='black')
        axes[1, 1].axvline(bedtime_hours.mean(), color='red', linestyle='--', 
                          label=f'Mean: {bedtime_hours.mean():.1f}h')
        axes[1, 1].set_title('Bedtime Distribution')
        axes[1, 1].set_xlabel('Hour of Day')
        axes[1, 1].set_ylabel('Frequency')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
    def create_interactive_plotly_dashboard(self, df, anomalies=None, save_path=None):
        """Create an interactive Plotly dashboard"""
        # Create subplots
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=('Sleep Duration Timeline', 'Sleep Quality Timeline',
                          'Bedtime vs Wake Time', 'Sleep Duration Distribution',
                          'Anomaly Types', 'Weekend vs Weekday Comparison'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Convert date to datetime
        df['date_dt'] = pd.to_datetime(df['date'])
        
        # Sleep Duration Timeline
        fig.add_trace(
            go.Scatter(x=df['date_dt'], y=df['sleep_duration'], 
                      mode='lines+markers', name='Sleep Duration',
                      line=dict(color=self.colors['normal'], width=2),
                      marker=dict(size=4)),
            row=1, col=1
        )
        
        # Add anomaly points if available
        if anomalies and len(anomalies.get('statistical_anomalies', [])) > 0:
            anomaly_df = anomalies['statistical_anomalies']
            anomaly_dates = pd.to_datetime(anomaly_df['date'])
            fig.add_trace(
                go.Scatter(x=anomaly_dates, y=anomaly_df['sleep_duration'],
                          mode='markers', name='Anomalies',
                          marker=dict(color=self.colors['anomaly'], size=8, symbol='x')),
                row=1, col=1
            )
        
        # Sleep Quality Timeline
        fig.add_trace(
            go.Scatter(x=df['date_dt'], y=df['sleep_quality'], 
                      mode='lines+markers', name='Sleep Quality',
                      line=dict(color='blue', width=2),
                      marker=dict(size=4)),
            row=1, col=2
        )
        
        # Bedtime vs Wake Time
        bedtime_hours = df['bedtime_dt'].dt.hour + df['bedtime_dt'].dt.minute/60
        wake_hours = df['wake_time_dt'].dt.hour + df['wake_time_dt'].dt.minute/60
        
        fig.add_trace(
            go.Scatter(x=df['date_dt'], y=bedtime_hours, 
                      mode='lines+markers', name='Bedtime',
                      line=dict(color='purple', width=2)),
            row=2, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=df['date_dt'], y=wake_hours, 
                      mode='lines+markers', name='Wake Time',
                      line=dict(color='orange', width=2)),
            row=2, col=1
        )
        
        # Sleep Duration Distribution
        fig.add_trace(
            go.Histogram(x=df['sleep_duration'], name='Duration Distribution',
                        marker_color=self.colors['normal'], opacity=0.7),
            row=2, col=2
        )
        
        # Anomaly Types (if available)
        if anomalies and len(anomalies.get('statistical_anomalies', [])) > 0:
            anomaly_types = []
            for types in anomalies['statistical_anomalies']['anomaly_types']:
                anomaly_types.extend(types)
            
            anomaly_counts = pd.Series(anomaly_types).value_counts()
            
            fig.add_trace(
                go.Bar(x=anomaly_counts.index, y=anomaly_counts.values,
                      name='Anomaly Types', marker_color=self.colors['anomaly']),
                row=3, col=1
            )
        
        # Weekend vs Weekday Comparison
        weekend_data = df[df['is_weekend'] == True]
        weekday_data = df[df['is_weekend'] == False]
        
        fig.add_trace(
            go.Box(y=weekday_data['sleep_duration'], name='Weekdays',
                  marker_color='lightblue'),
            row=3, col=2
        )
        
        fig.add_trace(
            go.Box(y=weekend_data['sleep_duration'], name='Weekends',
                  marker_color='lightcoral'),
            row=3, col=2
        )
        
        # Update layout
        fig.update_layout(
            title_text="Interactive Sleep Pattern Dashboard",
            title_x=0.5,
            height=1000,
            showlegend=True
        )
        
        # Update axes labels
        fig.update_xaxes(title_text="Date", row=1, col=1)
        fig.update_yaxes(title_text="Hours", row=1, col=1)
        fig.update_xaxes(title_text="Date", row=1, col=2)
        fig.update_yaxes(title_text="Quality Score", row=1, col=2)
        fig.update_xaxes(title_text="Date", row=2, col=1)
        fig.update_yaxes(title_text="Hour of Day", row=2, col=1)
        fig.update_xaxes(title_text="Sleep Duration (Hours)", row=2, col=2)
        fig.update_yaxes(title_text="Frequency", row=2, col=2)
        
        if save_path:
            fig.write_html(save_path)
        
        fig.show()
        
    def create_summary_report_visualization(self, analysis_results, save_path=None):
        """Create a summary visualization of the analysis results"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Sleep Analysis Summary Report', fontsize=16, fontweight='bold')
        
        # Summary statistics
        summary = analysis_results['summary']
        
        # Anomaly counts
        anomaly_counts = [
            summary['statistical_anomalies'],
            summary['ml_anomalies'],
            summary['insomnia_episodes'],
            summary['circadian_shifts']
        ]
        anomaly_labels = ['Statistical', 'ML-Detected', 'Insomnia Episodes', 'Circadian Shifts']
        
        axes[0, 0].bar(anomaly_labels, anomaly_counts, color=[self.colors['anomaly'], 'orange', 
                                                            self.colors['insomnia'], self.colors['circadian']])
        axes[0, 0].set_title('Detected Anomalies Summary')
        axes[0, 0].set_ylabel('Count')
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # Baseline statistics
        baseline = summary['baseline_stats']['overall']
        metrics = ['avg_duration', 'avg_quality', 'avg_efficiency']
        values = [baseline['avg_duration'], baseline['avg_quality'], baseline['avg_efficiency']]
        labels = ['Sleep Duration (h)', 'Sleep Quality', 'Sleep Efficiency']
        
        axes[0, 1].bar(labels, values, color=self.colors['normal'])
        axes[0, 1].set_title('Average Sleep Metrics')
        axes[0, 1].set_ylabel('Value')
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # Weekday vs Weekend comparison
        weekday_baseline = summary['baseline_stats']['weekdays']
        weekend_baseline = summary['baseline_stats']['weekends']
        
        x = np.arange(3)
        width = 0.35
        
        axes[1, 0].bar(x - width/2, [weekday_baseline['avg_duration'], weekday_baseline['avg_quality'], 
                                   weekday_baseline['avg_efficiency']], width, label='Weekdays', color='lightblue')
        axes[1, 0].bar(x + width/2, [weekend_baseline['avg_duration'], weekend_baseline['avg_quality'], 
                                   weekend_baseline['avg_efficiency']], width, label='Weekends', color='lightcoral')
        
        axes[1, 0].set_title('Weekday vs Weekend Comparison')
        axes[1, 0].set_ylabel('Value')
        axes[1, 0].set_xticks(x)
        axes[1, 0].set_xticklabels(['Duration', 'Quality', 'Efficiency'])
        axes[1, 0].legend()
        
        # Sleep health score (custom metric)
        health_score = self.calculate_sleep_health_score(summary)
        axes[1, 1].pie([health_score, 100-health_score], labels=['Healthy', 'Needs Improvement'], 
                      colors=[self.colors['normal'], self.colors['anomaly']], autopct='%1.1f%%')
        axes[1, 1].set_title(f'Sleep Health Score: {health_score:.1f}/100')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
    def calculate_sleep_health_score(self, summary):
        """Calculate a custom sleep health score (0-100)"""
        baseline = summary['baseline_stats']['overall']
        
        # Factors affecting health score
        duration_score = min(100, max(0, (baseline['avg_duration'] - 5) / 3 * 100))  # 5-8h is good
        quality_score = (baseline['avg_quality'] / 5) * 100  # 1-5 scale
        efficiency_score = baseline['avg_efficiency'] * 100  # 0-1 scale
        
        # Penalty for anomalies
        total_anomalies = (summary['statistical_anomalies'] + summary['ml_anomalies'] + 
                          summary['insomnia_episodes'] + summary['circadian_shifts'])
        anomaly_penalty = min(50, total_anomalies * 5)  # Max 50 point penalty
        
        health_score = (duration_score * 0.4 + quality_score * 0.4 + efficiency_score * 0.2) - anomaly_penalty
        return max(0, min(100, health_score))

# Production module - no test code needed
