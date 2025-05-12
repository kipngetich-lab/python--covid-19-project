import pandas as pd
from pathlib import Path
from visualization import *
import os

def ensure_reports_directory():
    """Create reports directory if it doesn't exist"""
    Path("../reports").mkdir(parents=True, exist_ok=True)

def load_clean_data():
    """Load processed dataset with error handling"""
    try:
        data_path = Path("../data/processed/cleaned_covid_data.csv")
        return pd.read_csv(data_path, parse_dates=['date'])
    except FileNotFoundError:
        print("Error: Cleaned data file not found. Please run data_processing.py first.")
        raise
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        raise

def calculate_metrics(df):
    """Compute derived metrics with error handling"""
    try:
        df['death_rate'] = df['total_deaths'] / df['total_cases']
        df['cases_per_million'] = (df['total_cases'] / df['population']) * 1e6
        return df
    except Exception as e:
        print(f"Error calculating metrics: {str(e)}")
        raise

def generate_report(df):
    """Create analysis report with key insights"""
    try:
        latest_data = df.groupby('location').last().reset_index()
        
        # Generate visualizations
        plot_time_series(df, 'total_cases', 
                        'Total COVID-19 Cases Over Time', 
                        'Total Cases', 
                        'total_cases_trend')
        
        plot_vaccination_progress(df, 'vaccination_progress')
        
        # Calculate key statistics
        stats = {
            'highest_cases': latest_data.loc[latest_data['total_cases'].idxmax()],
            'highest_vaccination': latest_data.loc[latest_data['people_vaccinated'].idxmax()],
            'highest_death_rate': latest_data.loc[latest_data['death_rate'].idxmax()]
        }
        
        return stats
    except Exception as e:
        print(f"Error generating report: {str(e)}")
        raise

if __name__ == "__main__":
    print("Running COVID-19 analysis...")
    
    try:
        # Ensure directory structure exists
        ensure_reports_directory()
        
        # Process data
        df = load_clean_data()
        df = calculate_metrics(df)
        report = generate_report(df)
        
        # Save insights
        insights_path = Path("../reports/insights.md")
        with open(insights_path, 'w') as f:
            f.write("# COVID-19 Analysis Insights\n\n")
            f.write(f"Highest cases: {report['highest_cases']['location']} ({report['highest_cases']['total_cases']:,})\n")
            f.write(f"Highest vaccination: {report['highest_vaccination']['location']} ({report['highest_vaccination']['people_vaccinated']:,})\n")
            f.write(f"Highest death rate: {report['highest_death_rate']['location']} ({report['highest_death_rate']['death_rate']:.2%})\n")
        
        print("Analysis complete! Results saved in reports/")
    except Exception as e:
        print(f"Analysis failed: {str(e)}")
        print("Please check:")
        print("- Data availability (run data_processing.py first)")
        print("- Directory permissions")