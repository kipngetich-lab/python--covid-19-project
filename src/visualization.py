import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path
import os

def ensure_figures_directory():
    """Create figures directory if it doesn't exist"""
    Path("../reports/figures").mkdir(parents=True, exist_ok=True)

def configure_plots():
    """Set consistent plot styling"""
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (12, 6)
    plt.rcParams['font.size'] = 12

def plot_time_series(df, metric, title, ylabel, filename):
    """Plot metric over time for all countries"""
    ensure_figures_directory()
    configure_plots()
    
    plt.figure()
    for country in df['location'].unique():
        country_data = df[df['location'] == country]
        plt.plot(country_data['date'], country_data[metric], label=country)
    
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel(ylabel)
    plt.legend()
    plt.tight_layout()
    
    save_path = Path(f'../reports/figures/{filename}.png')
    try:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved visualization to {save_path}")
    except Exception as e:
        print(f"Error saving visualization: {str(e)}")
    finally:
        plt.close()

def plot_vaccination_progress(df, filename):
    """Plot vaccination percentage over time"""
    ensure_figures_directory()
    configure_plots()
    
    plt.figure()
    for country in df['location'].unique():
        country_data = df[df['location'] == country]
        vaccinated_pct = (country_data['people_vaccinated'] / 
                         country_data['population']) * 100
        plt.plot(country_data['date'], vaccinated_pct, label=country)
    
    plt.title('COVID-19 Vaccination Progress')
    plt.xlabel('Date')
    plt.ylabel('% Population Vaccinated')
    plt.legend()
    plt.tight_layout()
    
    save_path = Path(f'../reports/figures/{filename}.png')
    try:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved visualization to {save_path}")
    except Exception as e:
        print(f"Error saving visualization: {str(e)}")
    finally:
        plt.close()