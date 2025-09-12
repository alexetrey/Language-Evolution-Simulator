# How to Use Your Own Sleep Data

## Option 1: Edit the CSV File

Edit `my_sleep_data.csv` with your actual sleep times:

```csv
date,bedtime,wake_time,sleep_duration,sleep_quality,is_weekend
2024-01-01,23:00,07:00,8.0,4.5,False
2024-01-02,22:30,06:30,8.0,4.0,False
```

### Column Format:
- **date**: YYYY-MM-DD format
- **bedtime**: HH:MM format (24-hour)
- **wake_time**: HH:MM format (24-hour) 
- **sleep_duration**: Hours as decimal (7.5 = 7h 30min)
- **sleep_quality**: 1-5 scale (1=terrible, 5=excellent)
- **is_weekend**: true or false

## Option 2: Use the GUI

1. Run: `python sleep_pattern_app.py`
2. Click "Load CSV File"
3. Select your sleep data file
4. Click "Analyze Sleep Patterns"

## Option 3: Use Command Line

```bash
python cli_sleep_analyzer.py --data my_sleep_data.csv --verbose
```

## Example Sleep Times:

### Good Sleep Pattern:
- Bedtime: 22:30-23:00
- Wake time: 06:30-07:00  
- Duration: 7.5-8.5 hours
- Quality: 4-5

### Poor Sleep Pattern:
- Bedtime: After midnight
- Wake time: Before 6 AM or after 9 AM
- Duration: Less than 6 hours or more than 10 hours
- Quality: 1-3
