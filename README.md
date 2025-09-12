# Sleep Pattern Analyzer

Analyze sleep data to find patterns and get sleep improvement tips.

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
python sleep_pattern_app.py
```

## Data Format

Your CSV needs these columns:
```csv
date,bedtime,wake_time,sleep_duration,sleep_quality,is_weekend
2024-01-01,22:30,07:00,8.5,4.5,False
```

## How It Works

1. Load your sleep data or generate sample data
2. Run analysis to find unusual patterns
3. Get personalized recommendations
4. View charts and export reports

## Files

- `sleep_pattern_app.py` - Main application
- `cli_sleep_analyzer.py` - Command line version
- `sleep_analyzer.py` - Analysis logic
- `sleep_visualizer.py` - Charts and graphs
- `sleep_advisor.py` - Recommendations
- `sleep_data_generator.py` - Sample data

## Dependencies

pandas, numpy, scikit-learn, matplotlib, plotly, seaborn, scipy
