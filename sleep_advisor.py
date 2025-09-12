
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class SleepAdvisor:
    def __init__(self):
        self.advice_database = {
            'insufficient_sleep': {
                'title': 'Insufficient Sleep Detected',
                'severity': 'high',
                'tips': [
                    "Aim for 7-9 hours of sleep per night for optimal health",
                    "Establish a consistent bedtime routine to improve sleep quality",
                    "Avoid caffeine and electronic devices 1 hour before bed",
                    "Create a cool, dark, and quiet sleep environment",
                    "Consider going to bed 15-30 minutes earlier each night gradually"
                ],
                'lifestyle_changes': [
                    "Reduce screen time before bed",
                    "Avoid large meals close to bedtime",
                    "Engage in relaxing activities like reading or meditation",
                    "Ensure your bedroom temperature is between 60-67°F"
                ]
            },
            'excessive_sleep': {
                'title': 'Excessive Sleep Detected',
                'severity': 'medium',
                'tips': [
                    "While 7-9 hours is recommended, consistently sleeping over 9 hours may indicate underlying issues",
                    "Check if you're experiencing depression, stress, or other health conditions",
                    "Ensure you're getting quality sleep rather than just quantity",
                    "Consider consulting a healthcare provider if excessive sleep persists"
                ],
                'lifestyle_changes': [
                    "Maintain a consistent sleep schedule even on weekends",
                    "Get regular exercise during the day",
                    "Ensure exposure to natural light in the morning",
                    "Evaluate your sleep environment for comfort and quality"
                ]
            },
            'poor_sleep_quality': {
                'title': 'Poor Sleep Quality Detected',
                'severity': 'high',
                'tips': [
                    "Focus on sleep hygiene practices to improve sleep quality",
                    "Create a relaxing pre-sleep routine",
                    "Ensure your mattress and pillows are comfortable and supportive",
                    "Keep your bedroom cool, dark, and quiet",
                    "Avoid alcohol and heavy meals before bed"
                ],
                'lifestyle_changes': [
                    "Establish a consistent bedtime routine",
                    "Limit naps to 20-30 minutes if needed",
                    "Exercise regularly but not within 3 hours of bedtime",
                    "Practice relaxation techniques like deep breathing or meditation"
                ]
            },
            'irregular_bedtime': {
                'title': 'Irregular Bedtime Pattern Detected',
                'severity': 'medium',
                'tips': [
                    "Consistency is key for healthy sleep patterns",
                    "Try to go to bed within the same 30-minute window each night",
                    "Gradually adjust your bedtime by 15 minutes until you reach your target",
                    "Avoid sleeping in on weekends to maintain consistency"
                ],
                'lifestyle_changes': [
                    "Set a fixed bedtime alarm reminder",
                    "Create a wind-down routine that starts 1 hour before bed",
                    "Avoid caffeine after 2 PM",
                    "Keep a sleep diary to track patterns"
                ]
            },
            'irregular_wake_time': {
                'title': 'Irregular Wake Time Pattern Detected',
                'severity': 'medium',
                'tips': [
                    "Consistent wake times help regulate your circadian rhythm",
                    "Set an alarm for the same time every day, even on weekends",
                    "Get exposure to bright light immediately upon waking",
                    "Avoid hitting the snooze button repeatedly"
                ],
                'lifestyle_changes': [
                    "Place your alarm across the room to force you to get up",
                    "Open curtains or turn on bright lights immediately upon waking",
                    "Have a morning routine that starts at the same time daily",
                    "Avoid staying in bed after waking up"
                ]
            },
            'low_sleep_efficiency': {
                'title': 'Low Sleep Efficiency Detected',
                'severity': 'medium',
                'tips': [
                    "Sleep efficiency measures how much time in bed is actually spent sleeping",
                    "Aim for sleep efficiency of 85% or higher",
                    "Only go to bed when you're actually sleepy",
                    "If you can't sleep within 20 minutes, get up and do something relaxing"
                ],
                'lifestyle_changes': [
                    "Avoid using your bed for activities other than sleep",
                    "Limit time in bed to your actual sleep need",
                    "Practice the 10-3-2-1-0 sleep rule",
                    "Consider cognitive behavioral therapy for insomnia (CBT-I)"
                ]
            },
            'insomnia_episodes': {
                'title': 'Insomnia Episodes Detected',
                'severity': 'high',
                'tips': [
                    "Multiple consecutive nights of poor sleep indicate an insomnia episode",
                    "Don't try to 'catch up' on sleep by sleeping longer",
                    "Maintain your regular sleep schedule even after poor nights",
                    "Consider professional help if insomnia persists for more than 2 weeks"
                ],
                'lifestyle_changes': [
                    "Practice good sleep hygiene consistently",
                    "Avoid clock-watching during the night",
                    "Use relaxation techniques to manage stress and anxiety",
                    "Consider keeping a worry journal to clear your mind before bed"
                ]
            },
            'circadian_shifts': {
                'title': 'Circadian Rhythm Shift Detected',
                'severity': 'medium',
                'tips': [
                    "Your natural sleep-wake cycle appears to be shifting",
                    "Gradual changes in sleep schedule can disrupt your circadian rhythm",
                    "Try to maintain consistent light exposure patterns",
                    "Consider light therapy to help reset your internal clock"
                ],
                'lifestyle_changes': [
                    "Get bright light exposure in the morning",
                    "Avoid bright screens 2 hours before bedtime",
                    "Maintain consistent meal times",
                    "Consider melatonin supplements under medical supervision"
                ]
            }
        }
        
        self.general_tips = [
            "Keep a consistent sleep schedule, even on weekends",
            "Create a bedtime routine that helps you wind down",
            "Make your bedroom cool, dark, and quiet",
            "Avoid large meals, caffeine, and alcohol before bedtime",
            "Get regular exercise, but not too close to bedtime",
            "Limit daytime naps to 20-30 minutes",
            "Manage stress through relaxation techniques",
            "Invest in a comfortable mattress and pillows",
            "Use your bed only for sleep and intimacy",
            "If you can't sleep, get up and do something relaxing until you feel sleepy"
        ]
    
    def analyze_anomalies(self, analysis_results):
        """Analyze detected anomalies and generate personalized advice"""
        advice_list = []
        
        # Check for different types of anomalies
        stat_anomalies = analysis_results.get('statistical_anomalies', pd.DataFrame())
        insomnia_episodes = analysis_results.get('insomnia_episodes', [])
        circadian_shifts = analysis_results.get('circadian_shifts', [])
        
        # Analyze statistical anomalies
        if len(stat_anomalies) > 0:
            anomaly_types = set()
            for types in stat_anomalies['anomaly_types']:
                anomaly_types.update(types)
            
            for anomaly_type in anomaly_types:
                if anomaly_type in self.advice_database:
                    advice_list.append(self._create_advice_entry(anomaly_type, stat_anomalies))
        
        # Analyze insomnia episodes
        if len(insomnia_episodes) > 0:
            advice_list.append(self._create_advice_entry('insomnia_episodes', insomnia_episodes))
        
        # Analyze circadian shifts
        if len(circadian_shifts) > 0:
            advice_list.append(self._create_advice_entry('circadian_shifts', circadian_shifts))
        
        return advice_list
    
    def _create_advice_entry(self, anomaly_type, data):
        """Create a detailed advice entry for a specific anomaly type"""
        advice_info = self.advice_database[anomaly_type]
        
        entry = {
            'type': anomaly_type,
            'title': advice_info['title'],
            'severity': advice_info['severity'],
            'tips': advice_info['tips'],
            'lifestyle_changes': advice_info['lifestyle_changes'],
            'data_summary': self._summarize_anomaly_data(anomaly_type, data),
            'priority': self._calculate_priority(anomaly_type, data)
        }
        
        return entry
    
    def _summarize_anomaly_data(self, anomaly_type, data):
        """Summarize the data for a specific anomaly type"""
        if anomaly_type in ['insomnia_episodes', 'circadian_shifts']:
            return f"Detected {len(data)} episodes/events"
        else:
            if isinstance(data, pd.DataFrame) and len(data) > 0:
                avg_duration = data['sleep_duration'].mean() if 'sleep_duration' in data.columns else 0
                avg_quality = data['sleep_quality'].mean() if 'sleep_quality' in data.columns else 0
                return f"Affected {len(data)} days, avg duration: {avg_duration:.1f}h, avg quality: {avg_quality:.1f}"
            return f"Detected in {len(data)} instances"
    
    def _calculate_priority(self, anomaly_type, data):
        """Calculate priority score for advice (1-10, higher = more urgent)"""
        base_priority = {
            'insufficient_sleep': 9,
            'poor_sleep_quality': 8,
            'insomnia_episodes': 9,
            'excessive_sleep': 6,
            'irregular_bedtime': 7,
            'irregular_wake_time': 7,
            'low_sleep_efficiency': 6,
            'circadian_shifts': 7
        }
        
        priority = base_priority.get(anomaly_type, 5)
        
        # Adjust priority based on frequency/severity
        if isinstance(data, pd.DataFrame):
            frequency_factor = min(len(data) / 10, 2)  # More frequent = higher priority
            priority += int(frequency_factor)
        elif isinstance(data, list):
            frequency_factor = min(len(data), 2)
            priority += frequency_factor
        
        return min(priority, 10)
    
    def generate_sleep_plan(self, analysis_results):
        """Generate a comprehensive sleep improvement plan"""
        advice_list = self.analyze_anomalies(analysis_results)
        
        # Sort by priority
        advice_list.sort(key=lambda x: x['priority'], reverse=True)
        
        plan = {
            'overview': self._generate_overview(analysis_results),
            'high_priority': [advice for advice in advice_list if advice['priority'] >= 8],
            'medium_priority': [advice for advice in advice_list if 5 <= advice['priority'] < 8],
            'low_priority': [advice for advice in advice_list if advice['priority'] < 5],
            'general_recommendations': self.general_tips,
            'timeline': self._generate_improvement_timeline(advice_list)
        }
        
        return plan
    
    def _generate_overview(self, analysis_results):
        """Generate an overview of the sleep analysis"""
        summary = analysis_results['summary']
        baseline = summary['baseline_stats']['overall']
        
        health_score = self._calculate_sleep_health_score(summary)
        
        overview = f"""
        Sleep Analysis Overview:
        • Total days analyzed: {summary['total_days']}
        • Average sleep duration: {baseline['avg_duration']:.1f} hours
        • Average sleep quality: {baseline['avg_quality']:.1f}/5
        • Sleep efficiency: {baseline['avg_efficiency']:.1%}
        • Overall sleep health score: {health_score:.1f}/100
        
        Detected Issues:
        • {summary['statistical_anomalies']} statistical anomalies
        • {summary['ml_anomalies']} ML-detected anomalies
        • {summary['insomnia_episodes']} insomnia episodes
        • {summary['circadian_shifts']} circadian shifts
        """
        
        return overview.strip()
    
    def _calculate_sleep_health_score(self, summary):
        """Calculate overall sleep health score"""
        baseline = summary['baseline_stats']['overall']
        
        # Duration score (optimal: 7-8 hours)
        duration_score = max(0, 100 - abs(baseline['avg_duration'] - 7.5) * 20)
        
        # Quality score (optimal: 4-5)
        quality_score = (baseline['avg_quality'] / 5) * 100
        
        # Efficiency score (optimal: 0.85+)
        efficiency_score = min(100, baseline['avg_efficiency'] * 120)
        
        # Anomaly penalty
        total_anomalies = (summary['statistical_anomalies'] + summary['ml_anomalies'] + 
                          summary['insomnia_episodes'] + summary['circadian_shifts'])
        anomaly_penalty = min(40, total_anomalies * 3)
        
        health_score = (duration_score * 0.4 + quality_score * 0.4 + efficiency_score * 0.2) - anomaly_penalty
        return max(0, min(100, health_score))
    
    def _generate_improvement_timeline(self, advice_list):
        """Generate a timeline for sleep improvements"""
        timeline = {
            'week_1': [
                "Establish consistent bedtime and wake time",
                "Create a relaxing bedtime routine",
                "Optimize sleep environment (temperature, darkness, quiet)"
            ],
            'week_2': [
                "Implement good sleep hygiene practices",
                "Limit caffeine and screen time before bed",
                "Start keeping a sleep diary"
            ],
            'week_3': [
                "Focus on stress management techniques",
                "Evaluate and adjust sleep schedule if needed",
                "Continue monitoring sleep patterns"
            ],
            'week_4': [
                "Assess progress and adjust plan",
                "Maintain consistent habits",
                "Consider professional help if needed"
            ]
        }
        
        return timeline
    
    def export_advice_report(self, plan, filename="sleep_advice_report.txt"):
        """Export advice plan to a text file"""
        with open(filename, 'w') as f:
            f.write("PERSONAL SLEEP IMPROVEMENT PLAN\n")
            f.write("=" * 50 + "\n\n")
            
            f.write("OVERVIEW\n")
            f.write("-" * 20 + "\n")
            f.write(plan['overview'] + "\n\n")
            
            # High priority items
            if plan['high_priority']:
                f.write("HIGH PRIORITY ISSUES\n")
                f.write("-" * 30 + "\n")
                for advice in plan['high_priority']:
                    f.write(f"\n{advice['title']}\n")
                    f.write(f"Priority: {advice['priority']}/10\n")
                    f.write(f"Summary: {advice['data_summary']}\n")
                    f.write("Tips:\n")
                    for tip in advice['tips']:
                        f.write(f"• {tip}\n")
                    f.write("Lifestyle Changes:\n")
                    for change in advice['lifestyle_changes']:
                        f.write(f"• {change}\n")
                f.write("\n")
            
            # Medium priority items
            if plan['medium_priority']:
                f.write("MEDIUM PRIORITY ISSUES\n")
                f.write("-" * 30 + "\n")
                for advice in plan['medium_priority']:
                    f.write(f"\n{advice['title']}\n")
                    f.write(f"Priority: {advice['priority']}/10\n")
                    f.write("Key Tips:\n")
                    for tip in advice['tips'][:3]:  # Show first 3 tips
                        f.write(f"• {tip}\n")
                f.write("\n")
            
            # General recommendations
            f.write("GENERAL SLEEP RECOMMENDATIONS\n")
            f.write("-" * 40 + "\n")
            for tip in plan['general_recommendations']:
                f.write(f"• {tip}\n")
            
            # Timeline
            f.write("\n\nIMPROVEMENT TIMELINE\n")
            f.write("-" * 25 + "\n")
            for week, tasks in plan['timeline'].items():
                f.write(f"\n{week.replace('_', ' ').title()}:\n")
                for task in tasks:
                    f.write(f"• {task}\n")
        
        print(f"Sleep advice report exported to {filename}")

