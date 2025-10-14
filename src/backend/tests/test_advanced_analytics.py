"""
Tests for Advanced Analytics Service
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import MagicMock, patch
from datetime import datetime

from src.backend.services.advanced_analytics import AdvancedAnalyticsService
from src.backend.core.exceptions import DataNotFoundError, ValidationError

class TestAdvancedAnalyticsService:
    """Test cases for AdvancedAnalyticsService"""
    
    @pytest.fixture
    def mock_data_processor(self):
        """Mock data processor for testing"""
        processor = MagicMock()
        processor.merged_df = pd.DataFrame({
            'year': [2020, 2021, 2022, 2023, 2024],
            'country': ['PRT', 'PRT', 'PRT', 'PRT', 'PRT'],
            'life_expectancy': [81.2, 81.5, 81.8, 82.1, 82.4],
            'doctor_density': [2.1, 2.2, 2.3, 2.4, 2.5],
            'nurse_density': [5.2, 5.4, 5.6, 5.8, 6.0],
            'government_spending': [5.8, 6.0, 6.2, 6.4, 6.6]
        })
        return processor
    
    @pytest.fixture
    def analytics_service(self, mock_data_processor):
        """Analytics service instance for testing"""
        return AdvancedAnalyticsService(mock_data_processor)
    
    def test_perform_trend_analysis_success(self, analytics_service):
        """Test successful trend analysis"""
        result = analytics_service.perform_trend_analysis(
            indicator='life_expectancy',
            country='PRT'
        )
        
        assert 'error' not in result
        assert result['indicator'] == 'life_expectancy'
        assert result['country'] == 'PRT'
        assert result['trend_direction'] in ['increasing', 'decreasing', 'stable']
        assert 0 <= result['trend_strength'] <= 1
        assert isinstance(result['annual_change'], float)
        assert isinstance(result['statistical_significance'], float)
        assert 'confidence_interval' in result
        assert 'data_points' in result
        assert len(result['data_points']) > 0
    
    def test_perform_trend_analysis_no_data(self, analytics_service):
        """Test trend analysis with no data"""
        analytics_service.data_processor.merged_df = pd.DataFrame()
        
        result = analytics_service.perform_trend_analysis(
            indicator='life_expectancy',
            country='PRT'
        )
        
        assert 'error' in result
        assert 'No data available' in result['error']
    
    def test_calculate_correlations_success(self, analytics_service):
        """Test successful correlation analysis"""
        # Add more data for correlation analysis
        additional_data = pd.DataFrame({
            'year': [2020, 2021, 2022, 2023, 2024],
            'country': ['ESP', 'ESP', 'ESP', 'ESP', 'ESP'],
            'life_expectancy': [83.1, 83.3, 83.5, 83.7, 83.9],
            'doctor_density': [2.8, 2.9, 3.0, 3.1, 3.2],
            'nurse_density': [6.1, 6.3, 6.5, 6.7, 6.9],
            'government_spending': [7.2, 7.4, 7.6, 7.8, 8.0]
        })
        
        analytics_service.data_processor.merged_df = pd.concat([
            analytics_service.data_processor.merged_df,
            additional_data
        ])
        
        result = analytics_service.calculate_correlations(
            indicators=['life_expectancy', 'doctor_density'],
            countries=['PRT', 'ESP']
        )
        
        assert 'error' not in result
        assert result['indicators'] == ['life_expectancy', 'doctor_density']
        assert len(result['correlation_matrix']) == 2
        assert len(result['correlation_matrix'][0]) == 2
        assert 'interpretation' in result
        assert isinstance(result['sample_size'], int)
    
    def test_calculate_correlations_insufficient_data(self, analytics_service):
        """Test correlation analysis with insufficient data"""
        result = analytics_service.calculate_correlations(
            indicators=['life_expectancy', 'doctor_density'],
            countries=['PRT']
        )
        
        assert 'error' in result
        assert 'Insufficient data' in result['error']
    
    def test_generate_forecast_success(self, analytics_service):
        """Test successful forecast generation"""
        result = analytics_service.generate_forecast(
            indicator='life_expectancy',
            country='PRT',
            forecast_years=3
        )
        
        assert 'error' not in result
        assert result['indicator'] == 'life_expectancy'
        assert result['country'] == 'PRT'
        assert result['forecast_years'] == 3
        assert 'model_performance' in result
        assert 'historical_data' in result
        assert 'forecast_data' in result
        assert len(result['forecast_data']) == 3
        assert all('confidence_interval' in point for point in result['forecast_data'])
    
    def test_generate_forecast_insufficient_data(self, analytics_service):
        """Test forecast generation with insufficient data"""
        analytics_service.data_processor.merged_df = pd.DataFrame({
            'year': [2020],
            'country': ['PRT'],
            'life_expectancy': [81.2]
        })
        
        result = analytics_service.generate_forecast(
            indicator='life_expectancy',
            country='PRT'
        )
        
        assert 'error' in result
        assert 'Insufficient historical data' in result['error']
    
    def test_statistical_significance_test_success(self, analytics_service):
        """Test successful statistical significance test"""
        # Add data for second country
        additional_data = pd.DataFrame({
            'year': [2020, 2021, 2022, 2023, 2024],
            'country': ['ESP', 'ESP', 'ESP', 'ESP', 'ESP'],
            'life_expectancy': [83.1, 83.3, 83.5, 83.7, 83.9]
        })
        
        analytics_service.data_processor.merged_df = pd.concat([
            analytics_service.data_processor.merged_df,
            additional_data
        ])
        
        result = analytics_service.statistical_significance_test(
            indicator='life_expectancy',
            country1='PRT',
            country2='ESP'
        )
        
        assert 'error' not in result
        assert result['indicator'] == 'life_expectancy'
        assert result['country1'] == 'PRT'
        assert result['country2'] == 'ESP'
        assert 'test_results' in result
        assert 'descriptive_statistics' in result
        assert 'interpretation' in result
        assert isinstance(result['test_results']['p_value'], float)
        assert isinstance(result['test_results']['cohens_d'], float)
    
    def test_statistical_significance_test_insufficient_data(self, analytics_service):
        """Test statistical test with insufficient data"""
        result = analytics_service.statistical_significance_test(
            indicator='life_expectancy',
            country1='PRT',
            country2='ESP'
        )
        
        assert 'error' in result
        assert 'Insufficient data' in result['error']
    
    def test_multi_variable_regression_success(self, analytics_service):
        """Test successful multi-variable regression"""
        result = analytics_service.multi_variable_regression(
            target_indicator='life_expectancy',
            predictor_indicators=['doctor_density', 'nurse_density', 'government_spending']
        )
        
        assert 'error' not in result
        assert result['target_indicator'] == 'life_expectancy'
        assert result['predictor_indicators'] == ['doctor_density', 'nurse_density', 'government_spending']
        assert 'model_performance' in result
        assert 'feature_importance' in result
        assert 'coefficient_significance' in result
        assert 'interpretation' in result
        assert isinstance(result['model_performance']['r_squared'], float)
        assert len(result['feature_importance']) == 3
    
    def test_multi_variable_regression_insufficient_data(self, analytics_service):
        """Test regression with insufficient data"""
        analytics_service.data_processor.merged_df = pd.DataFrame()
        
        result = analytics_service.multi_variable_regression(
            target_indicator='life_expectancy',
            predictor_indicators=['doctor_density']
        )
        
        assert 'error' in result
        assert 'Insufficient data' in result['error']
    
    def test_get_indicator_data_success(self, analytics_service):
        """Test successful data retrieval"""
        df = analytics_service._get_indicator_data('life_expectancy', 'PRT')
        
        assert not df.empty
        assert 'year' in df.columns
        assert 'country' in df.columns
        assert 'value' in df.columns
        assert len(df) > 0
    
    def test_get_indicator_data_no_data(self, analytics_service):
        """Test data retrieval with no matching data"""
        analytics_service.data_processor.merged_df = pd.DataFrame()
        
        df = analytics_service._get_indicator_data('life_expectancy', 'PRT')
        
        assert df.empty
    
    def test_calculate_indicator_correlation(self, analytics_service):
        """Test correlation calculation between indicators"""
        corr, p_value = analytics_service._calculate_indicator_correlation(
            'life_expectancy', 'doctor_density'
        )
        
        assert isinstance(corr, float)
        assert isinstance(p_value, float)
        assert -1 <= corr <= 1
        assert 0 <= p_value <= 1
    
    def test_prepare_regression_data(self, analytics_service):
        """Test regression data preparation"""
        df = analytics_service._prepare_regression_data(
            'life_expectancy',
            ['doctor_density', 'nurse_density'],
            ['PRT']
        )
        
        assert not df.empty
        assert 'life_expectancy' in df.columns
        assert 'doctor_density' in df.columns
        assert 'nurse_density' in df.columns
    
    def test_interpret_correlation_matrix(self, analytics_service):
        """Test correlation matrix interpretation"""
        indicators = ['life_expectancy', 'doctor_density']
        correlation_matrix = np.array([[1.0, 0.8], [0.8, 1.0]])
        significance_matrix = np.array([[0.0, 0.001], [0.001, 0.0]])
        
        interpretation = analytics_service._interpret_correlation_matrix(
            indicators, correlation_matrix, significance_matrix
        )
        
        assert isinstance(interpretation, str)
        assert len(interpretation) > 0
    
    def test_interpret_statistical_test(self, analytics_service):
        """Test statistical test interpretation"""
        interpretation = analytics_service._interpret_statistical_test(
            'PRT', 'ESP', 0.01, 0.6
        )
        
        assert isinstance(interpretation, str)
        assert 'PRT' in interpretation
        assert 'ESP' in interpretation
        assert 'statistically significant' in interpretation
    
    def test_interpret_regression_results(self, analytics_service):
        """Test regression results interpretation"""
        interpretation = analytics_service._interpret_regression_results(
            'life_expectancy',
            ['doctor_density', 'nurse_density'],
            0.85,
            {'doctor_density': 0.6, 'nurse_density': 0.4}
        )
        
        assert isinstance(interpretation, str)
        assert 'life_expectancy' in interpretation
        assert '85%' in interpretation or '0.85' in interpretation
    
    def test_error_handling_in_trend_analysis(self, analytics_service):
        """Test error handling in trend analysis"""
        with patch.object(analytics_service, '_get_indicator_data', side_effect=Exception("Test error")):
            result = analytics_service.perform_trend_analysis('life_expectancy', 'PRT')
            
            assert 'error' in result
            assert 'Trend analysis failed' in result['error']
    
    def test_error_handling_in_correlation_analysis(self, analytics_service):
        """Test error handling in correlation analysis"""
        with patch.object(analytics_service, '_get_indicator_data', side_effect=Exception("Test error")):
            result = analytics_service.calculate_correlations(['life_expectancy', 'doctor_density'])
            
            assert 'error' in result
            assert 'Correlation analysis failed' in result['error']
    
    def test_error_handling_in_forecast_generation(self, analytics_service):
        """Test error handling in forecast generation"""
        with patch.object(analytics_service, '_get_indicator_data', side_effect=Exception("Test error")):
            result = analytics_service.generate_forecast('life_expectancy', 'PRT')
            
            assert 'error' in result
            assert 'Forecast generation failed' in result['error']
    
    def test_error_handling_in_statistical_test(self, analytics_service):
        """Test error handling in statistical test"""
        with patch.object(analytics_service, '_get_indicator_data', side_effect=Exception("Test error")):
            result = analytics_service.statistical_significance_test(
                'life_expectancy', 'PRT', 'ESP'
            )
            
            assert 'error' in result
            assert 'Statistical test failed' in result['error']
    
    def test_error_handling_in_regression_analysis(self, analytics_service):
        """Test error handling in regression analysis"""
        with patch.object(analytics_service, '_prepare_regression_data', side_effect=Exception("Test error")):
            result = analytics_service.multi_variable_regression(
                'life_expectancy', ['doctor_density']
            )
            
            assert 'error' in result
            assert 'Regression analysis failed' in result['error']
