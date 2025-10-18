"""
Real Data Loader for Policy Simulation Assistant
Loads actual health indicator data from CSV files
"""

import pandas as pd
import os
from typing import Dict, List, Any, Optional
from pathlib import Path

class RealDataLoader:
    def __init__(self, data_dir: str = "adapt_context/data"):
        self.data_dir = Path(data_dir)
        self.data_cache = {}
        self.countries_cache = None
        
    def load_life_expectancy_data(self) -> pd.DataFrame:
        """Load life expectancy data from CSV"""
        if 'life_expectancy' not in self.data_cache:
            file_path = self.data_dir / "Life Expectancy.csv"
            if file_path.exists():
                df = pd.read_csv(file_path)
                # Filter for country-level data only
                df = df[df['DIM_GEO_CODE_TYPE'] == 'COUNTRY']
                self.data_cache['life_expectancy'] = df
            else:
                self.data_cache['life_expectancy'] = pd.DataFrame()
        return self.data_cache['life_expectancy']
    
    def load_doctor_density_data(self) -> pd.DataFrame:
        """Load doctor density data from CSV"""
        if 'doctor_density' not in self.data_cache:
            file_path = self.data_dir / "Density of Doctors.csv"
            if file_path.exists():
                df = pd.read_csv(file_path)
                # Filter for country-level data only
                df = df[df['DIM_GEO_CODE_TYPE'] == 'COUNTRY']
                self.data_cache['doctor_density'] = df
            else:
                self.data_cache['doctor_density'] = pd.DataFrame()
        return self.data_cache['doctor_density']
    
    def load_nurse_density_data(self) -> pd.DataFrame:
        """Load nurse density data from CSV"""
        if 'nurse_density' not in self.data_cache:
            file_path = self.data_dir / "Density of nurses and midwives.csv"
            if file_path.exists():
                df = pd.read_csv(file_path)
                # Filter for country-level data only
                df = df[df['DIM_GEO_CODE_TYPE'] == 'COUNTRY']
                self.data_cache['nurse_density'] = df
            else:
                self.data_cache['nurse_density'] = pd.DataFrame()
        return self.data_cache['nurse_density']
    
    def load_health_spending_data(self) -> pd.DataFrame:
        """Load health spending data from CSV"""
        if 'health_spending' not in self.data_cache:
            file_path = self.data_dir / "Government Spending.csv"
            if file_path.exists():
                df = pd.read_csv(file_path)
                # Filter for country-level data only
                df = df[df['DIM_GEO_CODE_TYPE'] == 'COUNTRY']
                self.data_cache['health_spending'] = df
            else:
                self.data_cache['health_spending'] = pd.DataFrame()
        return self.data_cache['health_spending']
    
    def get_available_countries(self) -> List[Dict[str, Any]]:
        """Get list of countries with their latest data"""
        if self.countries_cache is not None:
            return self.countries_cache
            
        countries = {}
        
        # Load life expectancy data to get countries
        life_exp_df = self.load_life_expectancy_data()
        if not life_exp_df.empty:
            # Get latest data for each country
            latest_data = life_exp_df.groupby('GEO_NAME_SHORT').apply(
                lambda x: x.loc[x['DIM_TIME'].idxmax()]
            ).reset_index(drop=True)
            
            for _, row in latest_data.iterrows():
                country_name = row['GEO_NAME_SHORT']
                year = row['DIM_TIME']
                life_exp = row['AMOUNT_N']
                gender = row['DIM_SEX']
                
                if country_name not in countries:
                    countries[country_name] = {
                        'name': country_name,
                        'year': year,
                        'life_expectancy': {},
                        'doctor_density': None,
                        'nurse_density': None,
                        'health_spending': None
                    }
                
                countries[country_name]['life_expectancy'][gender] = life_exp
        
        # Load other indicators
        doctor_df = self.load_doctor_density_data()
        if not doctor_df.empty:
            latest_doctor = doctor_df.groupby('GEO_NAME_SHORT').apply(
                lambda x: x.loc[x['DIM_TIME'].idxmax()]
            ).reset_index(drop=True)
            
            for _, row in latest_doctor.iterrows():
                country_name = row['GEO_NAME_SHORT']
                if country_name in countries:
                    countries[country_name]['doctor_density'] = row['RATE_PER_10000_N']
        
        nurse_df = self.load_nurse_density_data()
        if not nurse_df.empty:
            latest_nurse = nurse_df.groupby('GEO_NAME_SHORT').apply(
                lambda x: x.loc[x['DIM_TIME'].idxmax()]
            ).reset_index(drop=True)
            
            for _, row in latest_nurse.iterrows():
                country_name = row['GEO_NAME_SHORT']
                if country_name in countries:
                    countries[country_name]['nurse_density'] = row['RATE_PER_10000_N']
        
        spending_df = self.load_health_spending_data()
        if not spending_df.empty:
            latest_spending = spending_df.groupby('GEO_NAME_SHORT').apply(
                lambda x: x.loc[x['DIM_TIME'].idxmax()]
            ).reset_index(drop=True)
            
            for _, row in latest_spending.iterrows():
                country_name = row['GEO_NAME_SHORT']
                if country_name in countries:
                    countries[country_name]['health_spending'] = row['RATE_PER_100_N']
        
        # Convert to list format
        self.countries_cache = []
        for country_name, data in countries.items():
            # Calculate average life expectancy if we have both genders
            avg_life_exp = None
            if 'BOTH' in data['life_expectancy']:
                avg_life_exp = data['life_expectancy']['BOTH']
            elif 'MALE' in data['life_expectancy'] and 'FEMALE' in data['life_expectancy']:
                avg_life_exp = (data['life_expectancy']['MALE'] + data['life_expectancy']['FEMALE']) / 2
            
            country_data = {
                'code': country_name[:3].upper(),  # Use first 3 letters as code
                'name': country_name,
                'baseline': {
                    'life_expectancy': avg_life_exp or 75.0,  # Default life expectancy
                    'doctor_density': data['doctor_density'] or 30.0,  # Default doctor density
                    'nurse_density': data['nurse_density'] or 50.0,  # Default nurse density
                    'health_spending': data['health_spending'] or 8.0,  # Default health spending
                    'year': data['year']
                },
                'gender_baseline': {
                    'BOTH': {'life_expectancy': avg_life_exp or 75.0},
                    'MALE': {'life_expectancy': data['life_expectancy'].get('MALE', avg_life_exp or 75.0)},
                    'FEMALE': {'life_expectancy': data['life_expectancy'].get('FEMALE', avg_life_exp or 75.0)}
                }
            }
            self.countries_cache.append(country_data)
        
        return self.countries_cache
    
    def get_country_data(self, country_name: str) -> Optional[Dict[str, Any]]:
        """Get specific country data"""
        countries = self.get_available_countries()
        for country in countries:
            if country['name'].lower() == country_name.lower():
                return country
        return None
    
    def get_latest_data_for_country(self, country_name: str, indicator: str) -> Optional[float]:
        """Get latest data for a specific country and indicator"""
        country_data = self.get_country_data(country_name)
        if country_data and indicator in country_data['baseline']:
            return country_data['baseline'][indicator]
        return None

# Global data loader instance
data_loader = RealDataLoader()
