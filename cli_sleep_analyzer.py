
import argparse
import sys
import os
from datetime import datetime
import pandas as pd

# Import our custom modules
from sleep_data_generator import SleepDataGenerator
from sleep_analyzer import SleepAnalyzer
from sleep_visualizer import SleepVisualizer
from sleep_advisor import SleepAdvisor

class CLISleepAnalyzer:
    def __init__(self):
        self.visualizer = SleepVisualizer()
        self.analyzer = SleepAnalyzer()
        self.advisor = SleepAdvisor()
        
    def generate_sample_data(self, days=90, output_file=None):
        """Generate sample sleep data"""
        print(f"Generating {days} days of sample sleep data...")
        
        generator = SleepDataGenerator()
        data = generator.generate_complete_dataset(days)
        
        if output_file:
            data.to_csv(output_file, index=False)
            print(f"Sample data saved to: {output_file}")
        else:
            output_file = f"sample_sleep_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            data.to_csv(output_file, index=False)
            print(f"Sample data saved to: {output_file}")
        
        return data
    
    def load_data(self, file_path):
        """Load sleep data from CSV file"""
        try:
            data = pd.read_csv(file_path)
            
            # Add datetime columns if they don't exist
            if 'bedtime_dt' not in data.columns:
                data['bedtime_dt'] = pd.to_datetime(data['date'] + ' ' + data['bedtime'])
            if 'wake_time_dt' not in data.columns:
                data['wake_time_dt'] = pd.to_datetime(data['date'] + ' ' + data['wake_time'])
            if 'day_of_week' not in data.columns:
                data['day_of_week'] = pd.to_datetime(data['date']).dt.day_name()
            
            print(f"Loaded {len(data)} days of sleep data from: {file_path}")
            return data
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
    
    def analyze_data(self, data, verbose=False):
        """Analyze sleep data for anomalies"""
        print("Analyzing sleep patterns for anomalies...")
        
        results = self.analyzer.generate_anomaly_report(data)
        
        if verbose:
            self.print_detailed_results(results)
        else:
            self.print_summary_results(results)
        
        return results
    
    def print_summary_results(self, results):
        """Print summary of analysis results"""
        summary = results['summary']
        
        print("\n" + "="*60)
        print("SLEEP ANALYSIS SUMMARY")
        print("="*60)
        print(f"Total days analyzed: {summary['total_days']}")
        print(f"Statistical anomalies: {summary['statistical_anomalies']}")
        print(f"ML-detected anomalies: {summary['ml_anomalies']}")
        print(f"Insomnia episodes: {summary['insomnia_episodes']}")
        print(f"Circadian shifts: {summary['circadian_shifts']}")
        
        baseline = summary['baseline_stats']['overall']
        print(f"\nBaseline Statistics:")
        print(f"  Average sleep duration: {baseline['avg_duration']:.1f} hours")
        print(f"  Average sleep quality: {baseline['avg_quality']:.1f}/5")
        print(f"  Average sleep efficiency: {baseline['avg_efficiency']:.1%}")
        print(f"  Average bedtime: {baseline['avg_bedtime']:.1f} hours")
        print(f"  Average wake time: {baseline['avg_wake']:.1f} hours")
    
    def print_detailed_results(self, results):
        """Print detailed analysis results"""
        self.print_summary_results(results)
        
        # Statistical anomalies
        stat_anomalies = results['statistical_anomalies']
        if len(stat_anomalies) > 0:
            print(f"\n" + "-"*60)
            print("STATISTICAL ANOMALIES")
            print("-"*60)
            for idx, row in stat_anomalies.head(10).iterrows():
                print(f"Date: {row['date']}")
                print(f"  Types: {', '.join(row['anomaly_types'])}")
                print(f"  Duration: {row['sleep_duration']:.1f}h, Quality: {row['sleep_quality']:.1f}/5")
                print(f"  Efficiency: {row['sleep_efficiency']:.1%}")
                print()
        
        # Insomnia episodes
        insomnia_episodes = results['insomnia_episodes']
        if insomnia_episodes:
            print(f"\n" + "-"*60)
            print("INSOMNIA EPISODES")
            print("-"*60)
            for i, episode in enumerate(insomnia_episodes):
                print(f"Episode {i+1}: {len(episode)} consecutive days")
        
        # Circadian shifts
        circadian_shifts = results['circadian_shifts']
        if circadian_shifts:
            print(f"\n" + "-"*60)
            print("CIRCADIAN SHIFTS")
            print("-"*60)
            for i, shift in enumerate(circadian_shifts):
                print(f"Shift {i+1}: {shift['start_date']}")
                print(f"  Magnitude: {shift['shift_magnitude']:.1f} hours")
                print(f"  Before: {shift['before_avg_bedtime']:.1f}h, After: {shift['after_avg_bedtime']:.1f}h")
    
    def generate_advice(self, results, export_file=None):
        """Generate sleep improvement advice"""
        print("\nGenerating personalized sleep advice...")
        
        plan = self.advisor.generate_sleep_plan(results)
        
        # Print overview
        print("\n" + "="*60)
        print("SLEEP IMPROVEMENT PLAN")
        print("="*60)
        print(plan['overview'])
        
        # Print high priority issues
        if plan['high_priority']:
            print(f"\n" + "-"*60)
            print("HIGH PRIORITY ISSUES")
            print("-"*60)
            for advice in plan['high_priority']:
                print(f"\n{advice['title']} (Priority: {advice['priority']}/10)")
                print(f"Summary: {advice['data_summary']}")
                print("Top Tips:")
                for tip in advice['tips'][:3]:
                    print(f"  • {tip}")
        
        # Export advice if requested
        if export_file:
            self.advisor.export_advice_report(plan, export_file)
            print(f"\nDetailed advice report exported to: {export_file}")
        else:
            # Ask user if they want to export
            response = input("\nWould you like to export a detailed advice report? (y/n): ")
            if response.lower() in ['y', 'yes']:
                export_file = f"sleep_advice_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                self.advisor.export_advice_report(plan, export_file)
                print(f"Advice report exported to: {export_file}")
    
    def create_visualizations(self, data, results, output_dir=None):
        """Create visualizations"""
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        print("\nCreating visualizations...")
        
        try:
            # Sleep timeline
            timeline_file = f"{output_dir}/sleep_timeline.png" if output_dir else None
            self.visualizer.create_sleep_timeline(data, results, timeline_file)
            print("✓ Sleep timeline created")
            
            # Distribution plots
            dist_file = f"{output_dir}/sleep_distributions.png" if output_dir else None
            self.visualizer.create_sleep_quality_distribution(data, dist_file)
            print("✓ Distribution plots created")
            
            # Anomaly heatmap
            if len(results['statistical_anomalies']) > 0:
                heatmap_file = f"{output_dir}/anomaly_heatmap.png" if output_dir else None
                self.visualizer.create_anomaly_heatmap(results, heatmap_file)
                print("✓ Anomaly heatmap created")
            
            # Summary report
            summary_file = f"{output_dir}/summary_report.png" if output_dir else None
            self.visualizer.create_summary_report_visualization(results, summary_file)
            print("✓ Summary report created")
            
            # Interactive dashboard
            if output_dir:
                dashboard_file = f"{output_dir}/interactive_dashboard.html"
                self.visualizer.create_interactive_plotly_dashboard(data, results, dashboard_file)
                print(f"✓ Interactive dashboard created: {dashboard_file}")
            
        except Exception as e:
            print(f"Error creating visualizations: {e}")
    
    def run_full_analysis(self, data_file=None, days=90, verbose=False, create_viz=True, output_dir=None):
        """Run complete sleep analysis pipeline"""
        print("PERSONAL SLEEP PATTERN ANOMALY DETECTOR")
        print("="*60)
        
        # Load or generate data
        if data_file and os.path.exists(data_file):
            data = self.load_data(data_file)
        else:
            if data_file:
                print(f"File {data_file} not found. Generating sample data instead.")
            data = self.generate_sample_data(days)
        
        if data is None:
            print("Failed to load data. Exiting.")
            return
        
        # Analyze data
        results = self.analyze_data(data, verbose)
        
        # Generate advice
        self.generate_advice(results)
        
        # Create visualizations
        if create_viz:
            self.create_visualizations(data, results, output_dir)
        
        print(f"\n" + "="*60)
        print("ANALYSIS COMPLETE")
        print("="*60)
        print("Thank you for using the Sleep Pattern Anomaly Detector!")

def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="Personal Sleep Pattern Anomaly Detector - CLI Version",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate sample data and run full analysis
  python cli_sleep_analyzer.py --generate --days 90

  # Analyze existing CSV file
  python cli_sleep_analyzer.py --data my_sleep_data.csv --verbose

  # Run analysis with custom output directory
  python cli_sleep_analyzer.py --data data.csv --output-dir results --no-viz

  # Generate advice report only
  python cli_sleep_analyzer.py --data data.csv --advice-only --export-advice my_plan.txt
        """
    )
    
    # Data options
    parser.add_argument('--data', '-d', 
                       help='Path to CSV file containing sleep data')
    parser.add_argument('--generate', '-g', action='store_true',
                       help='Generate sample sleep data instead of loading from file')
    parser.add_argument('--days', type=int, default=90,
                       help='Number of days for sample data generation (default: 90)')
    parser.add_argument('--output-data', '-o',
                       help='Output file for generated sample data')
    
    # Analysis options
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show detailed analysis results')
    parser.add_argument('--advice-only', action='store_true',
                       help='Only generate advice, skip visualizations')
    
    # Output options
    parser.add_argument('--output-dir', 
                       help='Directory to save visualizations and reports')
    parser.add_argument('--export-advice',
                       help='Export detailed advice report to specified file')
    parser.add_argument('--no-viz', action='store_true',
                       help='Skip visualization generation')
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.data and not args.generate:
        print("Error: Either --data or --generate must be specified")
        parser.print_help()
        return
    
    if args.data and not os.path.exists(args.data):
        print(f"Error: Data file '{args.data}' not found")
        return
    
    # Create output directory if specified
    if args.output_dir and not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
        print(f"Created output directory: {args.output_dir}")
    
    # Initialize analyzer and run analysis
    analyzer = CLISleepAnalyzer()
    
    try:
        analyzer.run_full_analysis(
            data_file=args.data,
            days=args.days,
            verbose=args.verbose,
            create_viz=not args.no_viz and not args.advice_only,
            output_dir=args.output_dir
        )
        
        # Handle advice export
        if args.export_advice and args.data:
            data = analyzer.load_data(args.data)
            if data is not None:
                results = analyzer.analyze_data(data, args.verbose)
                analyzer.advisor.export_advice_report(
                    analyzer.advisor.generate_sleep_plan(results), 
                    args.export_advice
                )
                print(f"Advice report exported to: {args.export_advice}")
        
    except KeyboardInterrupt:
        print("\n\nAnalysis interrupted by user.")
    except Exception as e:
        print(f"\nError during analysis: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
