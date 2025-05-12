import pandas as pd
from pathlib import Path
import os
import urllib.request

def ensure_data_directory():
    """Create data directories if they don't exist"""
    Path("../data/raw").mkdir(parents=True, exist_ok=True)
    Path("../data/processed").mkdir(parents=True, exist_ok=True)

def download_raw_data():
    """Download the dataset if it doesn't exist"""
    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    raw_path = Path("../data/raw/owid-covid-data.csv")
    
    if not raw_path.exists():
        print("Downloading dataset...")
        urllib.request.urlretrieve(url, raw_path)
        print("Download complete!")
    else:
        print("Dataset already exists")

def load_raw_data():
    """Load raw dataset with error handling"""
    try:
        data_path = Path("../data/raw/owid-covid-data.csv")
        return pd.read_csv(data_path)
    except FileNotFoundError:
        print("Error: Data file not found. Please download it first.")
        raise
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        raise

def clean_data(df):
    """Perform data cleaning operations"""
    # Convert date column
    df['date'] = pd.to_datetime(df['date'])
    
    # Select key columns and countries
    key_columns = [
        'date', 'location', 'total_cases', 'new_cases',
        'total_deaths', 'new_deaths', 'total_vaccinations',
        'people_vaccinated', 'population'
    ]
    
    countries = [
        'United States', 'India', 'Brazil', 
        'Germany', 'Kenya', 'United Kingdom'
    ]
    
    df = df[key_columns]
    df = df[df['location'].isin(countries)]
    
    # Forward fill missing values within each country
    df = df.groupby('location').apply(lambda x: x.ffill())
    
    return df.reset_index(drop=True)

def save_clean_data(df):
    """Save processed data to CSV"""
    output_path = Path("../data/processed/cleaned_covid_data.csv")
    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to {output_path}")

if __name__ == "__main__":
    print("Processing COVID-19 data...")
    
    try:
        # Ensure directory structure exists
        ensure_data_directory()
        
        # Download data if needed
        download_raw_data()
        
        # Process data
        raw_df = load_raw_data()
        clean_df = clean_data(raw_df)
        save_clean_data(clean_df)
        
        print("Data processing completed successfully!")
    except Exception as e:
        print(f"Data processing failed: {str(e)}")
        print("Please check:")
        print("- Internet connection for downloading")
        print("- Directory permissions")
        print("- Available disk space")