"""
Data processing service for health indicators.
Handles data ingestion, validation, and normalization.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class HealthDataProcessor:
    """Processes and validates health indicator data."""
    
    def __init__(self):
        self.country_mapping = {
            'Spain': 'ESP',
            'Sweden': 'SWE', 
            'Greece': 'GRC',
            'Portugal': 'PRT',
            'Germany': 'DEU',
            'France': 'FRA',
            'Italy': 'ITA',
            'United Kingdom': 'GBR',
            'United States': 'USA',
            'Canada': 'CAN'
        }
        
        self.metric_mapping = {
            'Life expectancy (at birth)': 'life_expectancy',
            'Density of doctors': 'doctor_density',
            'Density of nurses and midwives': 'nurse_density',
            'Density of pharmacists': 'pharmacist_density',
            'Government expenditure on health': 'health_spending'
        }
    
    def load_life_expectancy_data(self, file_path: str) -> pd.DataFrame:
        """Load and process life expectancy data."""
        try:
            df = pd.read_csv(file_path)
            
            # Filter for countries and recent years
            df = df[df['DIM_GEO_CODE_TYPE'] == 'COUNTRY']
            df = df[df['DIM_TIME'] >= 2010]  # Focus on recent data
            
            # Extract country name and map to ISO codes
            df['country'] = df['GEO_NAME_SHORT'].map(self.country_mapping)
            df = df.dropna(subset=['country'])
            
            # Normalize metric name
            df['metric'] = 'life_expectancy'
            df['value'] = df['AMOUNT_N']
            df['year'] = df['DIM_TIME']
            
            return df[['country', 'year', 'metric', 'value']].copy()
            
        except Exception as e:
            logger.error(f"Error loading life expectancy data: {e}")
            raise
    
    def load_workforce_data(self, file_path: str, metric_name: str) -> pd.DataFrame:
        """Load and process workforce density data."""
        try:
            df = pd.read_csv(file_path)
            
            # Filter for countries and recent years
            df = df[df['DIM_GEO_CODE_TYPE'] == 'COUNTRY']
            df = df[df['DIM_TIME'] >= 2010]
            
            # Extract country name and map to ISO codes
            df['country'] = df['GEO_NAME_SHORT'].map(self.country_mapping)
            df = df.dropna(subset=['country'])
            
            # Normalize metric name
            df['metric'] = self.metric_mapping.get(metric_name, metric_name.lower().replace(' ', '_'))
            
            # Convert rate per 10,000 to rate per 1,000
            if 'RATE_PER_10000_N' in df.columns:
                df['value'] = df['RATE_PER_10000_N'] / 10
            else:
                df['value'] = df['AMOUNT_N']
            
            df['year'] = df['DIM_TIME']
            
            return df[['country', 'year', 'metric', 'value']].copy()
            
        except Exception as e:
            logger.error(f"Error loading workforce data for {metric_name}: {e}")
            raise
    
    def load_spending_data(self, file_path: str) -> pd.DataFrame:
        """Load and process government health spending data."""
        try:
            df = pd.read_csv(file_path)
            
            # Filter for countries and recent years
            df = df[df['DIM_GEO_CODE_TYPE'] == 'COUNTRY']
            df = df[df['DIM_TIME'] >= 2010]
            
            # Extract country name and map to ISO codes
            df['country'] = df['GEO_NAME_SHORT'].map(self.country_mapping)
            df = df.dropna(subset=['country'])
            
            # Normalize metric name
            df['metric'] = 'health_spending'
            df['value'] = df['AMOUNT_N']
            df['year'] = df['DIM_TIME']
            
            return df[['country', 'year', 'metric', 'value']].copy()
            
        except Exception as e:
            logger.error(f"Error loading spending data: {e}")
            raise
    
    def merge_health_data(self, data_dir: str) -> pd.DataFrame:
        """Merge all health indicator data into a single dataset."""
        try:
            data_dir = Path(data_dir)
            all_data = []
            
            # Load life expectancy data
            life_exp_file = data_dir / "Life Expectancy.csv"
            if life_exp_file.exists():
                life_exp_df = self.load_life_expectancy_data(str(life_exp_file))
                all_data.append(life_exp_df)
            
            # Load workforce data
            workforce_files = [
                ("Density of Doctors.csv", "Density of doctors"),
                ("Density of nurses and midwives.csv", "Density of nurses and midwives"),
                ("Density of pharmacists.csv", "Density of pharmacists")
            ]
            
            for filename, metric_name in workforce_files:
                file_path = data_dir / filename
                if file_path.exists():
                    workforce_df = self.load_workforce_data(str(file_path), metric_name)
                    all_data.append(workforce_df)
            
            # Load spending data
            spending_file = data_dir / "Government Spending.csv"
            if spending_file.exists():
                spending_df = self.load_spending_data(str(spending_file))
                all_data.append(spending_df)
            
            if not all_data:
                raise ValueError("No data files found")
            
            # Merge all data
            merged_df = pd.concat(all_data, ignore_index=True)
            
            # Pivot to have metrics as columns
            pivoted_df = merged_df.pivot_table(
                index=['country', 'year'], 
                columns='metric', 
                values='value', 
                aggfunc='mean'
            ).reset_index()
            
            # Fill missing values with forward fill
            pivoted_df = pivoted_df.fillna(method='ffill').fillna(method='bfill')
            
            return pivoted_df
            
        except Exception as e:
            logger.error(f"Error merging health data: {e}")
            raise
    
    def get_baseline_data(self, df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        """Get baseline data for each country (most recent year)."""
        try:
            baseline_data = {}
            
            for country in df['country'].unique():
                country_data = df[df['country'] == country].copy()
                
                # Get most recent year with complete data
                country_data = country_data.dropna()
                if country_data.empty:
                    continue
                
                latest_year = country_data['year'].max()
                latest_data = country_data[country_data['year'] == latest_year].iloc[0]
                
                baseline_data[country] = {
                    'life_expectancy': float(latest_data.get('life_expectancy', 0)),
                    'doctor_density': float(latest_data.get('doctor_density', 0)),
                    'nurse_density': float(latest_data.get('nurse_density', 0)),
                    'pharmacist_density': float(latest_data.get('pharmacist_density', 0)),
                    'health_spending': float(latest_data.get('health_spending', 0)),
                    'year': int(latest_year)
                }
            
            return baseline_data
            
        except Exception as e:
            logger.error(f"Error getting baseline data: {e}")
            raise
    
    def validate_data_quality(self, df: pd.DataFrame) -> Dict[str, float]:
        """Calculate data quality metrics."""
        try:
            total_records = len(df)
            
            # Completeness
            completeness = (1 - df.isnull().sum().sum() / (total_records * len(df.columns))) * 100
            
            # Validity (check for reasonable ranges)
            validity_checks = []
            
            if 'life_expectancy' in df.columns:
                life_exp_valid = ((df['life_expectancy'] >= 30) & (df['life_expectancy'] <= 100)).sum()
                validity_checks.append(life_exp_valid / len(df) * 100)
            
            if 'doctor_density' in df.columns:
                doctor_valid = ((df['doctor_density'] >= 0) & (df['doctor_density'] <= 20)).sum()
                validity_checks.append(doctor_valid / len(df) * 100)
            
            if 'nurse_density' in df.columns:
                nurse_valid = ((df['nurse_density'] >= 0) & (df['nurse_density'] <= 50)).sum()
                validity_checks.append(nurse_valid / len(df) * 100)
            
            if 'health_spending' in df.columns:
                spending_valid = ((df['health_spending'] >= 0) & (df['health_spending'] <= 20)).sum()
                validity_checks.append(spending_valid / len(df) * 100)
            
            validity = np.mean(validity_checks) if validity_checks else 100
            
            # Consistency (check for duplicates)
            duplicates = df.duplicated().sum()
            consistency = (1 - duplicates / total_records) * 100
            
            # Overall quality score
            overall_quality = (completeness + validity + consistency) / 3
            
            return {
                'completeness': completeness,
                'validity': validity,
                'consistency': consistency,
                'overall_quality': overall_quality
            }
            
        except Exception as e:
            logger.error(f"Error calculating data quality: {e}")
            return {
                'completeness': 0,
                'validity': 0,
                'consistency': 0,
                'overall_quality': 0
            }
