"""
Personal Sleep Pattern Anomaly Detector - Enhanced GUI Application
Modern, user-friendly interface with custom styling and improved UX
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import os
from datetime import datetime, timedelta
import webbrowser

# Import our custom modules
from sleep_data_generator import SleepDataGenerator
from sleep_analyzer import SleepAnalyzer
from sleep_visualizer import SleepVisualizer
from sleep_advisor import SleepAdvisor

class ModernSleepPatternApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌙 Personal Sleep Pattern Anomaly Detector")
        self.root.geometry("1400x900")
        
        # Modern color scheme
        self.colors = {
            'primary': '#2C3E50',      # Dark blue-gray
            'secondary': '#3498DB',     # Blue
            'accent': '#E74C3C',        # Red
            'success': '#27AE60',       # Green
            'warning': '#F39C12',       # Orange
            'background': '#ECF0F1',    # Light gray
            'card': '#FFFFFF',          # White
            'text': '#2C3E50',          # Dark text
            'text_light': '#7F8C8D',    # Light text
            'border': '#BDC3C7'         # Border gray
        }
        
        # Configure root window
        self.root.configure(bg=self.colors['background'])
        
        # Initialize components
        self.sleep_data = None
        self.analysis_results = None
        self.visualizer = SleepVisualizer()
        self.analyzer = SleepAnalyzer()
        self.advisor = SleepAdvisor()
        
        # Create the enhanced interface
        self.create_modern_interface()
        
    def create_modern_interface(self):
        """Create the modern, enhanced GUI interface"""
        # Main container with padding
        main_container = tk.Frame(self.root, bg=self.colors['background'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header section
        self.create_header(main_container)
        
        # Main content area
        content_frame = tk.Frame(main_container, bg=self.colors['background'])
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # Left panel - Controls
        self.create_control_panel(content_frame)
        
        # Right panel - Results
        self.create_results_panel(content_frame)
        
        # Status bar
        self.create_status_bar(main_container)
        
    def create_header(self, parent):
        """Create the application header"""
        header_frame = tk.Frame(parent, bg=self.colors['primary'], height=80)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            header_frame, 
            text="🌙 Personal Sleep Pattern Anomaly Detector",
            font=('Segoe UI', 24, 'bold'),
            fg='white',
            bg=self.colors['primary']
        )
        title_label.pack(pady=20)
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Advanced Sleep Analysis & Personalized Recommendations",
            font=('Segoe UI', 12),
            fg='#BDC3C7',
            bg=self.colors['primary']
        )
        subtitle_label.pack()
        
    def create_control_panel(self, parent):
        """Create the enhanced control panel"""
        # Left panel frame
        control_frame = tk.Frame(parent, bg=self.colors['background'])
        control_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Data section
        self.create_data_section(control_frame)
        
        # Analysis section
        self.create_analysis_section(control_frame)
        
        # Visualization section
        self.create_visualization_section(control_frame)
        
        # Export section
        self.create_export_section(control_frame)
        
    def create_data_section(self, parent):
        """Create the data input section"""
        data_card = self.create_card(parent, "📊 Data Management")
        
        # Generate sample data
        generate_btn = self.create_modern_button(
            data_card, 
            "🎲 Generate Sample Data", 
            self.generate_sample_data,
            self.colors['secondary']
        )
        generate_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Load CSV file
        load_btn = self.create_modern_button(
            data_card,
            "📁 Load CSV File",
            self.load_csv_file,
            self.colors['success']
        )
        load_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Data info
        self.data_info_label = tk.Label(
            data_card,
            text="No data loaded",
            font=('Segoe UI', 10),
            fg=self.colors['text_light'],
            bg=self.colors['card']
        )
        self.data_info_label.pack(pady=(10, 0))
        
    def create_analysis_section(self, parent):
        """Create the analysis section"""
        analysis_card = self.create_card(parent, "🔍 Analysis")
        
        self.analyze_btn = self.create_modern_button(
            analysis_card,
            "⚡ Analyze Sleep Patterns",
            self.analyze_sleep_data,
            self.colors['accent']
        )
        self.analyze_btn.pack(fill=tk.X)
        self.analyze_btn.config(state='disabled')
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            analysis_card,
            variable=self.progress_var,
            maximum=100,
            style='Modern.Horizontal.TProgressbar'
        )
        self.progress_bar.pack(fill=tk.X, pady=(10, 0))
        
    def create_visualization_section(self, parent):
        """Create the visualization section"""
        viz_card = self.create_card(parent, "📈 Visualizations")
        
        # Visualization buttons
        viz_buttons = [
            ("📊 Sleep Timeline", self.show_sleep_timeline, self.colors['secondary']),
            ("📉 Distribution Plots", self.show_distributions, self.colors['warning']),
            ("🔥 Anomaly Heatmap", self.show_anomaly_heatmap, self.colors['accent']),
            ("🌐 Interactive Dashboard", self.show_interactive_dashboard, self.colors['success'])
        ]
        
        for text, command, color in viz_buttons:
            btn = self.create_modern_button(viz_card, text, command, color)
            btn.pack(fill=tk.X, pady=(0, 8))
            
    def create_export_section(self, parent):
        """Create the export section"""
        export_card = self.create_card(parent, "💾 Export Results")
        
        # Export buttons
        export_btn = self.create_modern_button(
            export_card,
            "📄 Export Advice Report",
            self.export_advice_report,
            self.colors['primary']
        )
        export_btn.pack(fill=tk.X, pady=(0, 10))
        
        export_all_btn = self.create_modern_button(
            export_card,
            "📦 Export All Results",
            self.export_all_results,
            self.colors['success']
        )
        export_all_btn.pack(fill=tk.X)
        
    def create_results_panel(self, parent):
        """Create the enhanced results panel"""
        # Right panel frame
        results_frame = tk.Frame(parent, bg=self.colors['background'])
        results_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Results header
        results_header = tk.Frame(results_frame, bg=self.colors['primary'], height=50)
        results_header.pack(fill=tk.X)
        results_header.pack_propagate(False)
        
        results_title = tk.Label(
            results_header,
            text="📋 Analysis Results",
            font=('Segoe UI', 16, 'bold'),
            fg='white',
            bg=self.colors['primary']
        )
        results_title.pack(pady=12)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(results_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Style the notebook
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook.Tab', padding=[20, 10])
        
        # Create tabs
        self.create_summary_tab()
        self.create_anomalies_tab()
        self.create_advice_tab()
        self.create_visualizations_tab()
        
    def create_summary_tab(self):
        """Create the summary tab"""
        self.summary_frame = tk.Frame(self.notebook, bg=self.colors['card'])
        self.notebook.add(self.summary_frame, text="📊 Summary")
        
        # Create scrollable text widget
        text_frame = tk.Frame(self.summary_frame, bg=self.colors['card'])
        text_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        self.summary_text = tk.Text(
            text_frame,
            wrap=tk.WORD,
            font=('Consolas', 11),
            bg=self.colors['card'],
            fg=self.colors['text'],
            relief=tk.FLAT,
            borderwidth=0
        )
        
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.summary_text.yview)
        self.summary_text.configure(yscrollcommand=scrollbar.set)
        
        self.summary_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_anomalies_tab(self):
        """Create the anomalies tab"""
        self.anomalies_frame = tk.Frame(self.notebook, bg=self.colors['card'])
        self.notebook.add(self.anomalies_frame, text="⚠️ Anomalies")
        
        # Create scrollable text widget
        text_frame = tk.Frame(self.anomalies_frame, bg=self.colors['card'])
        text_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        self.anomalies_text = tk.Text(
            text_frame,
            wrap=tk.WORD,
            font=('Consolas', 11),
            bg=self.colors['card'],
            fg=self.colors['text'],
            relief=tk.FLAT,
            borderwidth=0
        )
        
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.anomalies_text.yview)
        self.anomalies_text.configure(yscrollcommand=scrollbar.set)
        
        self.anomalies_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_advice_tab(self):
        """Create the advice tab"""
        self.advice_frame = tk.Frame(self.notebook, bg=self.colors['card'])
        self.notebook.add(self.advice_frame, text="💡 Sleep Advice")
        
        # Create scrollable text widget
        text_frame = tk.Frame(self.advice_frame, bg=self.colors['card'])
        text_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        self.advice_text = tk.Text(
            text_frame,
            wrap=tk.WORD,
            font=('Consolas', 11),
            bg=self.colors['card'],
            fg=self.colors['text'],
            relief=tk.FLAT,
            borderwidth=0
        )
        
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.advice_text.yview)
        self.advice_text.configure(yscrollcommand=scrollbar.set)
        
        self.advice_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Export button
        button_frame = tk.Frame(self.advice_frame, bg=self.colors['card'])
        button_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        export_advice_btn = self.create_modern_button(
            button_frame,
            "📄 Export Advice Report",
            self.export_advice_report,
            self.colors['primary']
        )
        export_advice_btn.pack(side=tk.LEFT)
        
    def create_visualizations_tab(self):
        """Create the visualizations tab"""
        self.viz_frame = tk.Frame(self.notebook, bg=self.colors['card'])
        self.notebook.add(self.viz_frame, text="📈 Charts")
        
    def create_status_bar(self, parent):
        """Create the status bar"""
        status_frame = tk.Frame(parent, bg=self.colors['primary'], height=30)
        status_frame.pack(fill=tk.X, pady=(20, 0))
        status_frame.pack_propagate(False)
        
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to analyze your sleep patterns")
        
        status_label = tk.Label(
            status_frame,
            textvariable=self.status_var,
            font=('Segoe UI', 10),
            fg='white',
            bg=self.colors['primary']
        )
        status_label.pack(pady=5)
        
    def create_card(self, parent, title):
        """Create a modern card container"""
        card_frame = tk.Frame(parent, bg=self.colors['card'], relief=tk.FLAT, bd=0)
        card_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Add subtle shadow effect
        shadow_frame = tk.Frame(parent, bg=self.colors['border'], height=2)
        shadow_frame.pack(fill=tk.X, pady=(0, 18))
        
        # Card header
        header_frame = tk.Frame(card_frame, bg=self.colors['primary'], height=40)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text=title,
            font=('Segoe UI', 12, 'bold'),
            fg='white',
            bg=self.colors['primary']
        )
        title_label.pack(pady=10)
        
        # Card content
        content_frame = tk.Frame(card_frame, bg=self.colors['card'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        return content_frame
        
    def create_modern_button(self, parent, text, command, color):
        """Create a modern styled button"""
        button = tk.Button(
            parent,
            text=text,
            command=command,
            font=('Segoe UI', 10, 'bold'),
            bg=color,
            fg='white',
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        
        # Add hover effects
        def on_enter(e):
            button.config(bg=self.lighten_color(color))
            
        def on_leave(e):
            button.config(bg=color)
            
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
        return button
        
    def lighten_color(self, color):
        """Lighten a hex color"""
        color_map = {
            '#2C3E50': '#34495E',  # primary
            '#3498DB': '#5DADE2',  # secondary
            '#E74C3C': '#EC7063',  # accent
            '#27AE60': '#58D68D',  # success
            '#F39C12': '#F7DC6F'   # warning
        }
        return color_map.get(color, color)
        
    def generate_sample_data(self):
        """Generate sample sleep data with progress indication"""
        self.status_var.set("Generating sample sleep data...")
        self.progress_var.set(0)
        self.root.update()
        
        def generate_data():
            try:
                self.progress_var.set(25)
                generator = SleepDataGenerator()
                
                self.progress_var.set(50)
                self.sleep_data = generator.generate_complete_dataset(90)
                
                self.progress_var.set(100)
                self.status_var.set(f"✅ Generated {len(self.sleep_data)} days of sample data")
                self.analyze_btn.config(state='normal')
                self.update_data_info()
                self.update_summary_display()
                
            except Exception as e:
                self.status_var.set(f"❌ Error generating data: {str(e)}")
                messagebox.showerror("Error", f"Failed to generate sample data: {str(e)}")
            finally:
                self.progress_var.set(0)
        
        # Run in separate thread
        thread = threading.Thread(target=generate_data)
        thread.daemon = True
        thread.start()
        
    def load_csv_file(self):
        """Load sleep data from CSV file"""
        file_path = filedialog.askopenfilename(
            title="Select Sleep Data CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.sleep_data = pd.read_csv(file_path)
                self.status_var.set(f"✅ Loaded {len(self.sleep_data)} days of data from {os.path.basename(file_path)}")
                self.analyze_btn.config(state='normal')
                self.update_data_info()
                self.update_summary_display()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load CSV file: {str(e)}")
                self.status_var.set("❌ Error loading file")
    
    def analyze_sleep_data(self):
        """Analyze sleep data for anomalies"""
        if self.sleep_data is None:
            messagebox.showwarning("Warning", "Please load or generate sleep data first")
            return
        
        self.status_var.set("🔍 Analyzing sleep patterns...")
        self.analyze_btn.config(state='disabled')
        self.progress_var.set(0)
        self.root.update()
        
        def analyze_data():
            try:
                self.progress_var.set(25)
                self.analysis_results = self.analyzer.generate_anomaly_report(self.sleep_data)
                
                self.progress_var.set(75)
                self.status_var.set("✅ Analysis completed successfully")
                self.analyze_btn.config(state='normal')
                
                # Update all display panels
                self.update_summary_display()
                self.update_anomalies_display()
                self.update_advice_display()
                
            except Exception as e:
                self.status_var.set(f"❌ Error during analysis: {str(e)}")
                messagebox.showerror("Error", f"Analysis failed: {str(e)}")
                self.analyze_btn.config(state='normal')
            finally:
                self.progress_var.set(100)
                self.root.after(1000, lambda: self.progress_var.set(0))
        
        # Run in separate thread
        thread = threading.Thread(target=analyze_data)
        thread.daemon = True
        thread.start()
    
    def update_data_info(self):
        """Update the data information display"""
        if self.sleep_data is not None:
            date_range = f"{self.sleep_data['date'].min()} to {self.sleep_data['date'].max()}"
            avg_duration = self.sleep_data['sleep_duration'].mean()
            avg_quality = self.sleep_data['sleep_quality'].mean()
            
            info_text = f"📊 {len(self.sleep_data)} days • {date_range}\n⏰ Avg: {avg_duration:.1f}h sleep • {avg_quality:.1f}/5 quality"
            self.data_info_label.config(text=info_text)
        else:
            self.data_info_label.config(text="No data loaded")
    
    def update_summary_display(self):
        """Update the summary tab display"""
        self.summary_text.delete(1.0, tk.END)
        
        if self.sleep_data is None:
            self.summary_text.insert(tk.END, "No data loaded")
            return
        
        # Generate summary text
        summary_text = self.generate_summary_text()
        self.summary_text.insert(tk.END, summary_text)
        
    def update_anomalies_display(self):
        """Update the anomalies tab display"""
        self.anomalies_text.delete(1.0, tk.END)
        
        if self.analysis_results is None:
            self.anomalies_text.insert(tk.END, "No analysis results available")
            return
        
        # Generate anomalies text
        anomalies_text = self.generate_anomalies_text()
        self.anomalies_text.insert(tk.END, anomalies_text)
        
    def update_advice_display(self):
        """Update the advice tab display"""
        self.advice_text.delete(1.0, tk.END)
        
        if self.analysis_results is None:
            self.advice_text.insert(tk.END, "No analysis results available")
            return
        
        # Generate advice plan
        plan = self.advisor.generate_sleep_plan(self.analysis_results)
        
        # Generate advice text
        advice_text = self.generate_advice_text(plan)
        self.advice_text.insert(tk.END, advice_text)
    
    def generate_summary_text(self):
        """Generate summary text for display"""
        if self.sleep_data is None:
            return "No data available"
        
        summary = []
        summary.append("🌙 SLEEP DATA SUMMARY")
        summary.append("=" * 50)
        summary.append(f"📅 Total Days Analyzed: {len(self.sleep_data)}")
        summary.append(f"📅 Date Range: {self.sleep_data['date'].min()} to {self.sleep_data['date'].max()}")
        summary.append("")
        
        # Basic statistics
        summary.append("📊 BASIC STATISTICS")
        summary.append("-" * 30)
        summary.append(f"⏰ Average Sleep Duration: {self.sleep_data['sleep_duration'].mean():.1f} hours")
        summary.append(f"⭐ Average Sleep Quality: {self.sleep_data['sleep_quality'].mean():.1f}/5")
        summary.append(f"📈 Sleep Duration Range: {self.sleep_data['sleep_duration'].min():.1f} - {self.sleep_data['sleep_duration'].max():.1f} hours")
        summary.append(f"📈 Sleep Quality Range: {self.sleep_data['sleep_quality'].min():.1f} - {self.sleep_data['sleep_quality'].max():.1f}")
        summary.append("")
        
        # Weekend vs weekday comparison
        weekday_data = self.sleep_data[self.sleep_data['is_weekend'] == False]
        weekend_data = self.sleep_data[self.sleep_data['is_weekend'] == True]
        
        summary.append("📅 WEEKDAY vs WEEKEND COMPARISON")
        summary.append("-" * 35)
        summary.append(f"🏢 Weekdays ({len(weekday_data)} days):")
        summary.append(f"   ⏰ Average Duration: {weekday_data['sleep_duration'].mean():.1f} hours")
        summary.append(f"   ⭐ Average Quality: {weekday_data['sleep_quality'].mean():.1f}/5")
        summary.append(f"🏠 Weekends ({len(weekend_data)} days):")
        summary.append(f"   ⏰ Average Duration: {weekend_data['sleep_duration'].mean():.1f} hours")
        summary.append(f"   ⭐ Average Quality: {weekend_data['sleep_quality'].mean():.1f}/5")
        summary.append("")
        
        # Analysis results if available
        if self.analysis_results:
            results_summary = self.analysis_results['summary']
            summary.append("🔍 ANOMALY DETECTION RESULTS")
            summary.append("-" * 35)
            summary.append(f"⚠️  Statistical Anomalies: {results_summary['statistical_anomalies']}")
            summary.append(f"🤖 ML-Detected Anomalies: {results_summary['ml_anomalies']}")
            summary.append(f"😴 Insomnia Episodes: {results_summary['insomnia_episodes']}")
            summary.append(f"🔄 Circadian Shifts: {results_summary['circadian_shifts']}")
            summary.append("")
            
            # Baseline statistics
            baseline = results_summary['baseline_stats']['overall']
            summary.append("📈 BASELINE STATISTICS")
            summary.append("-" * 25)
            summary.append(f"🌙 Average Bedtime: {baseline['avg_bedtime']:.1f} hours")
            summary.append(f"☀️  Average Wake Time: {baseline['avg_wake']:.1f} hours")
            summary.append(f"⚡ Average Sleep Efficiency: {baseline['avg_efficiency']:.1%}")
            summary.append("")
        
        return "\n".join(summary)
    
    def generate_anomalies_text(self):
        """Generate anomalies text for display"""
        if self.analysis_results is None:
            return "No analysis results available"
        
        text = []
        text.append("⚠️  DETECTED ANOMALIES")
        text.append("=" * 50)
        text.append("")
        
        # Statistical anomalies
        stat_anomalies = self.analysis_results['statistical_anomalies']
        if len(stat_anomalies) > 0:
            text.append("📊 STATISTICAL ANOMALIES")
            text.append("-" * 25)
            for idx, row in stat_anomalies.head(10).iterrows():
                text.append(f"📅 Date: {row['date']}")
                text.append(f"   🏷️  Types: {', '.join(row['anomaly_types'])}")
                text.append(f"   ⏰ Sleep Duration: {row['sleep_duration']:.1f} hours")
                text.append(f"   ⭐ Sleep Quality: {row['sleep_quality']:.1f}/5")
                text.append(f"   ⚡ Sleep Efficiency: {row['sleep_efficiency']:.1%}")
                text.append("")
            
            if len(stat_anomalies) > 10:
                text.append(f"... and {len(stat_anomalies) - 10} more anomalies")
                text.append("")
        
        # Insomnia episodes
        insomnia_episodes = self.analysis_results['insomnia_episodes']
        if insomnia_episodes:
            text.append("😴 INSOMNIA EPISODES")
            text.append("-" * 20)
            for i, episode in enumerate(insomnia_episodes):
                start_date = self.sleep_data.iloc[episode[0]]['date']
                end_date = self.sleep_data.iloc[episode[-1]]['date']
                text.append(f"📅 Episode {i+1}: {start_date} to {end_date} ({len(episode)} days)")
            text.append("")
        
        # Circadian shifts
        circadian_shifts = self.analysis_results['circadian_shifts']
        if circadian_shifts:
            text.append("🔄 CIRCADIAN SHIFTS")
            text.append("-" * 18)
            for i, shift in enumerate(circadian_shifts):
                text.append(f"📅 Shift {i+1}: {shift['start_date']}")
                text.append(f"   📊 Magnitude: {shift['shift_magnitude']:.1f} hours")
                text.append(f"   🌙 Before: {shift['before_avg_bedtime']:.1f}h, After: {shift['after_avg_bedtime']:.1f}h")
            text.append("")
        
        return "\n".join(text)
    
    def generate_advice_text(self, plan):
        """Generate advice text for display"""
        text = []
        text.append("💡 PERSONAL SLEEP IMPROVEMENT PLAN")
        text.append("=" * 50)
        text.append("")
        text.append(plan['overview'])
        text.append("")
        
        # High priority issues
        if plan['high_priority']:
            text.append("🚨 HIGH PRIORITY ISSUES")
            text.append("-" * 30)
            for advice in plan['high_priority']:
                text.append(f"\n📋 {advice['title']} (Priority: {advice['priority']}/10)")
                text.append(f"📊 Summary: {advice['data_summary']}")
                text.append("💡 Tips:")
                for tip in advice['tips']:
                    text.append(f"   • {tip}")
                text.append("🔄 Lifestyle Changes:")
                for change in advice['lifestyle_changes']:
                    text.append(f"   • {change}")
                text.append("")
        
        # Medium priority issues
        if plan['medium_priority']:
            text.append("⚠️  MEDIUM PRIORITY ISSUES")
            text.append("-" * 30)
            for advice in plan['medium_priority']:
                text.append(f"\n📋 {advice['title']} (Priority: {advice['priority']}/10)")
                text.append("💡 Key Tips:")
                for tip in advice['tips'][:3]:
                    text.append(f"   • {tip}")
                text.append("")
        
        # General recommendations
        text.append("🌟 GENERAL SLEEP RECOMMENDATIONS")
        text.append("-" * 40)
        for tip in plan['general_recommendations']:
            text.append(f"   • {tip}")
        
        # Timeline
        text.append("\n\n📅 IMPROVEMENT TIMELINE")
        text.append("-" * 25)
        for week, tasks in plan['timeline'].items():
            text.append(f"\n📆 {week.replace('_', ' ').title()}:")
            for task in tasks:
                text.append(f"   • {task}")
        
        return "\n".join(text)
    
    def show_sleep_timeline(self):
        """Show sleep timeline visualization"""
        if self.sleep_data is None:
            messagebox.showwarning("Warning", "Please load or generate sleep data first")
            return
        
        self.clear_visualization_frame()
        self.status_var.set("📊 Creating sleep timeline visualization...")
        
        try:
            # Create matplotlib figure
            fig = plt.figure(figsize=(12, 8))
            self.visualizer.create_sleep_timeline(self.sleep_data, self.analysis_results, fig=fig)
            
            # Embed in tkinter
            canvas = FigureCanvasTkAgg(fig, self.viz_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            self.status_var.set("✅ Sleep timeline created successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create timeline visualization: {str(e)}")
            self.status_var.set("❌ Error creating visualization")
    
    def show_distributions(self):
        """Show distribution plots"""
        if self.sleep_data is None:
            messagebox.showwarning("Warning", "Please load or generate sleep data first")
            return
        
        self.clear_visualization_frame()
        self.status_var.set("📊 Creating distribution plots...")
        
        try:
            # Create matplotlib figure
            fig = plt.figure(figsize=(12, 8))
            self.visualizer.create_sleep_quality_distribution(self.sleep_data, fig=fig)
            
            # Embed in tkinter
            canvas = FigureCanvasTkAgg(fig, self.viz_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            self.status_var.set("✅ Distribution plots created successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create distribution plots: {str(e)}")
            self.status_var.set("❌ Error creating visualization")
    
    def show_anomaly_heatmap(self):
        """Show anomaly heatmap"""
        if self.analysis_results is None:
            messagebox.showwarning("Warning", "Please run analysis first")
            return
        
        self.clear_visualization_frame()
        self.status_var.set("🔥 Creating anomaly heatmap...")
        
        try:
            # Create matplotlib figure
            fig = plt.figure(figsize=(12, 8))
            self.visualizer.create_anomaly_heatmap(self.analysis_results, fig=fig)
            
            # Embed in tkinter
            canvas = FigureCanvasTkAgg(fig, self.viz_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            self.status_var.set("✅ Anomaly heatmap created successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create anomaly heatmap: {str(e)}")
            self.status_var.set("❌ Error creating visualization")
    
    def show_interactive_dashboard(self):
        """Show interactive dashboard"""
        if self.sleep_data is None:
            messagebox.showwarning("Warning", "Please load or generate sleep data first")
            return
        
        self.status_var.set("🌐 Creating interactive dashboard...")
        
        try:
            # Create interactive dashboard
            dashboard_file = f"interactive_dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            self.visualizer.create_interactive_plotly_dashboard(
                self.sleep_data, self.analysis_results, dashboard_file
            )
            
            # Open in browser
            webbrowser.open(f"file://{os.path.abspath(dashboard_file)}")
            self.status_var.set(f"✅ Interactive dashboard opened: {dashboard_file}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create interactive dashboard: {str(e)}")
            self.status_var.set("❌ Error creating dashboard")
    
    def clear_visualization_frame(self):
        """Clear the visualization frame"""
        for widget in self.viz_frame.winfo_children():
            widget.destroy()
    
    def export_advice_report(self):
        """Export advice report"""
        if self.analysis_results is None:
            messagebox.showwarning("Warning", "Please run analysis first")
            return
        
        try:
            plan = self.advisor.generate_sleep_plan(self.analysis_results)
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Save Sleep Advice Report"
            )
            
            if filename:
                self.advisor.export_advice_report(plan, filename)
                self.status_var.set(f"✅ Advice report exported to {os.path.basename(filename)}")
                messagebox.showinfo("Success", f"Advice report saved to:\n{filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export advice report: {str(e)}")
    
    def export_all_results(self):
        """Export all results"""
        if self.sleep_data is None or self.analysis_results is None:
            messagebox.showwarning("Warning", "Please run complete analysis first")
            return
        
        try:
            # Ask for export directory
            export_dir = filedialog.askdirectory(title="Select Export Directory")
            if not export_dir:
                return
            
            self.status_var.set("💾 Exporting all results...")
            
            # Export data
            data_file = os.path.join(export_dir, "sleep_data.csv")
            self.sleep_data.to_csv(data_file, index=False)
            
            # Export advice report
            plan = self.advisor.generate_sleep_plan(self.analysis_results)
            advice_file = os.path.join(export_dir, "sleep_advice_report.txt")
            self.advisor.export_advice_report(plan, advice_file)
            
            # Export visualizations
            self.visualizer.create_sleep_timeline(
                self.sleep_data, self.analysis_results, 
                os.path.join(export_dir, "sleep_timeline.png")
            )
            self.visualizer.create_sleep_quality_distribution(
                self.sleep_data, 
                os.path.join(export_dir, "sleep_distributions.png")
            )
            self.visualizer.create_anomaly_heatmap(
                self.analysis_results, 
                os.path.join(export_dir, "anomaly_heatmap.png")
            )
            self.visualizer.create_summary_report_visualization(
                self.analysis_results, 
                os.path.join(export_dir, "summary_report.png")
            )
            
            self.status_var.set(f"✅ All results exported to {export_dir}")
            messagebox.showinfo("Success", f"All results exported successfully to:\n{export_dir}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export results: {str(e)}")

def main():
    """Main function to run the enhanced application"""
    root = tk.Tk()
    app = ModernSleepPatternApp(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
