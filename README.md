# Sleep Pattern Anomaly Detector

A Python tool for analyzing sleep patterns, detecting anomalies, and generating personalized improvement recommendations.

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```bash
# GUI Application
python sleep_pattern_app.py

# Command Line Interface
python cli_sleep_analyzer.py --help
```

## Features

- **Anomaly Detection**: Statistical analysis + ML (Isolation Forest)
- **Visualizations**: Timeline charts, distributions, heatmaps, interactive dashboards
- **Personalized Advice**: Priority-based recommendations with improvement timeline
- **Export Options**: CSV, PNG, HTML, TXT formats
- **Dual Interface**: GUI and CLI support

## Data Format

CSV with required columns:
```csv
date,bedtime,wake_time,sleep_duration,sleep_quality,is_weekend
2024-01-01,22:30,07:00,8.5,4.5,False
```

## Architecture

```
├── sleep_pattern_app.py      # GUI application
├── cli_sleep_analyzer.py     # CLI interface
├── sleep_data_generator.py   # Sample data generation
├── sleep_analyzer.py         # Core analysis engine
├── sleep_visualizer.py       # Visualization engine
├── sleep_advisor.py          # Advice generation
└── requirements.txt          # Dependencies
```

## Usage

### GUI
1. `python sleep_pattern_app.py`
2. Generate sample data or load CSV
3. Run analysis
4. View results and export

### CLI
```bash
# Generate and analyze
python cli_sleep_analyzer.py --generate --days 90 --verbose

# Analyze existing data
python cli_sleep_analyzer.py --data sleep_data.csv --verbose

# Export advice
python cli_sleep_analyzer.py --data data.csv --export-advice report.txt
```

### Programmatic Usage
```python
from sleep_analyzer import SleepAnalyzer
from sleep_advisor import SleepAdvisor
import pandas as pd

# Load data
data = pd.read_csv('sleep_data.csv')

# Analyze
analyzer = SleepAnalyzer()
results = analyzer.generate_anomaly_report(data)

# Get advice
advisor = SleepAdvisor()
plan = advisor.generate_sleep_plan(results)
```

## Dependencies

- pandas >= 1.5.0
- numpy >= 1.21.0
- scikit-learn >= 1.1.0
- matplotlib >= 3.5.0
- plotly >= 5.10.0
- seaborn >= 0.11.0
- scipy >= 1.9.0

## Algorithm Details

### Anomaly Detection Methods
1. **Statistical**: Threshold-based detection for sleep duration, quality, consistency
2. **ML**: Isolation Forest for complex pattern anomalies
3. **Pattern**: Consecutive anomaly detection, circadian shift analysis

### Analysis Pipeline
1. Data preprocessing and feature extraction
2. Baseline statistical modeling
3. Multi-method anomaly detection
4. Pattern recognition and classification
5. Personalized recommendation generation

## Output Examples

```
SLEEP ANALYSIS SUMMARY
Total Days: 90
Statistical Anomalies: 12
ML Anomalies: 8
Insomnia Episodes: 2
Circadian Shifts: 1

HIGH PRIORITY ISSUES
Insufficient Sleep (Priority: 9/10)
- Aim for 7-9 hours per night
- Establish consistent bedtime routine
- Avoid screens 1 hour before bed
```

## License

MIT License
