"""
Tests for the Policy Simulation Engine.
"""

import pytest
import numpy as np
import pandas as pd
from unittest.mock import Mock, patch
from ..services.simulation_engine import PolicySimulationEngine
from ..services.data_processor import HealthDataProcessor


class TestPolicySimulationEngine:
    """Test cases for PolicySimulationEngine."""
    
    @pytest.fixture
    def engine(self):
        """Create a simulation engine instance."""
        return PolicySimulationEngine()
    
    @pytest.fixture
    def sample_data(self):
        """Create sample health data for testing."""
        data = {
            'country': ['PRT', 'PRT', 'PRT', 'ESP', 'ESP', 'ESP'],
            'year': [2020, 2021, 2022, 2020, 2021, 2022],
            'life_expectancy': [81.2, 81.5, 81.8, 83.1, 83.4, 83.7],
            'doctor_density': [2.1, 2.2, 2.3, 2.8, 2.9, 3.0],
            'nurse_density': [5.2, 5.3, 5.4, 6.1, 6.2, 6.3],
            'health_spending': [5.8, 6.0, 6.2, 7.2, 7.4, 7.6]
        }
        return pd.DataFrame(data)
    
    def test_engine_initialization(self, engine):
        """Test engine initialization."""
        assert engine.model is not None
        assert engine.is_trained == False
        assert engine.feature_importance == {}
        assert engine.model_metrics == {}
    
    def test_prepare_training_data(self, engine, sample_data):
        """Test training data preparation."""
        X, y = engine.prepare_training_data(sample_data)
        
        assert X.shape[0] == 6  # 6 samples
        assert X.shape[1] == 3  # 3 features
        assert y.shape[0] == 6  # 6 targets
        assert not np.isnan(X).any()
        assert not np.isnan(y).any()
    
    def test_prepare_training_data_insufficient_data(self, engine):
        """Test training data preparation with insufficient data."""
        insufficient_data = pd.DataFrame({
            'life_expectancy': [80.0],
            'doctor_density': [2.0],
            'nurse_density': [5.0],
            'health_spending': [6.0]
        })
        
        with pytest.raises(ValueError, match="Insufficient data for training"):
            engine.prepare_training_data(insufficient_data)
    
    def test_train_model(self, engine, sample_data):
        """Test model training."""
        metrics = engine.train_model(sample_data)
        
        assert engine.is_trained == True
        assert 'r2_score' in metrics
        assert 'mse' in metrics
        assert 'rmse' in metrics
        assert 'training_samples' in metrics
        assert 'test_samples' in metrics
        assert metrics['training_samples'] > 0
        assert metrics['test_samples'] > 0
        assert len(engine.feature_importance) == 3
    
    def test_predict_life_expectancy_not_trained(self, engine):
        """Test prediction without trained model."""
        with pytest.raises(ValueError, match="Model must be trained"):
            engine.predict_life_expectancy(2.5, 5.8, 6.2)
    
    def test_predict_life_expectancy(self, engine, sample_data):
        """Test life expectancy prediction."""
        # Train the model first
        engine.train_model(sample_data)
        
        prediction, details = engine.predict_life_expectancy(2.5, 5.8, 6.2)
        
        assert isinstance(prediction, float)
        assert prediction > 0
        assert 'confidence_interval' in details
        assert 'feature_contributions' in details
        assert 'model_metrics' in details
        
        # Check confidence interval
        ci = details['confidence_interval']
        assert 'lower' in ci
        assert 'upper' in ci
        assert 'margin_of_error' in ci
        assert ci['lower'] < ci['upper']
        
        # Check feature contributions
        contributions = details['feature_contributions']
        assert 'doctor_density' in contributions
        assert 'nurse_density' in contributions
        assert 'health_spending' in contributions
        assert 'intercept' in contributions
    
    def test_calculate_confidence_interval(self, engine, sample_data):
        """Test confidence interval calculation."""
        engine.train_model(sample_data)
        
        X = np.array([[2.5, 5.8, 6.2]])
        ci = engine._calculate_confidence_interval(X)
        
        assert 'lower' in ci
        assert 'upper' in ci
        assert 'margin_of_error' in ci
        assert ci['lower'] >= 0
        assert ci['upper'] > ci['lower']
        assert ci['margin_of_error'] > 0
    
    def test_calculate_feature_contributions(self, engine, sample_data):
        """Test feature contributions calculation."""
        engine.train_model(sample_data)
        
        contributions = engine._calculate_feature_contributions(2.5, 5.8, 6.2)
        
        assert 'doctor_density' in contributions
        assert 'nurse_density' in contributions
        assert 'health_spending' in contributions
        assert 'intercept' in contributions
        
        # All contributions should be numeric
        for key, value in contributions.items():
            assert isinstance(value, (int, float))
    
    def test_run_simulation_not_trained(self, engine):
        """Test running simulation without trained model."""
        baseline_data = {
            'life_expectancy': 81.2,
            'doctor_density': 2.1,
            'nurse_density': 5.2,
            'health_spending': 5.8,
            'year': 2022
        }
        parameters = {
            'doctor_density': 2.5,
            'nurse_density': 5.8,
            'health_spending': 6.2
        }
        
        with pytest.raises(ValueError, match="Model must be trained"):
            engine.run_simulation('PRT', baseline_data, parameters)
    
    def test_run_simulation(self, engine, sample_data):
        """Test complete simulation run."""
        # Train the model first
        engine.train_model(sample_data)
        
        baseline_data = {
            'life_expectancy': 81.2,
            'doctor_density': 2.1,
            'nurse_density': 5.2,
            'health_spending': 5.8,
            'year': 2022
        }
        parameters = {
            'doctor_density': 2.5,
            'nurse_density': 5.8,
            'health_spending': 6.2
        }
        
        result = engine.run_simulation('PRT', baseline_data, parameters)
        
        # Check result structure
        assert 'simulation_id' in result
        assert 'country' in result
        assert 'timestamp' in result
        assert 'baseline' in result
        assert 'parameters' in result
        assert 'prediction' in result
        assert 'model_metrics' in result
        assert 'metadata' in result
        
        # Check specific values
        assert result['country'] == 'PRT'
        assert result['baseline'] == baseline_data
        assert result['parameters'] == parameters
        
        # Check prediction structure
        prediction = result['prediction']
        assert 'life_expectancy' in prediction
        assert 'change' in prediction
        assert 'change_percentage' in prediction
        assert 'confidence_interval' in prediction
        assert 'feature_contributions' in prediction
        
        # Check metadata
        metadata = result['metadata']
        assert 'model_version' in metadata
        assert 'execution_time' in metadata
        assert 'data_quality' in metadata
    
    def test_get_model_info_not_trained(self, engine):
        """Test getting model info when not trained."""
        info = engine.get_model_info()
        assert info['status'] == 'not_trained'
    
    def test_get_model_info_trained(self, engine, sample_data):
        """Test getting model info when trained."""
        engine.train_model(sample_data)
        info = engine.get_model_info()
        
        assert info['status'] == 'trained'
        assert 'feature_importance' in info
        assert 'metrics' in info
        assert 'model_type' in info
        assert 'features' in info
        assert 'target' in info
        
        assert info['model_type'] == 'LinearRegression'
        assert info['features'] == ['doctor_density', 'nurse_density', 'health_spending']
        assert info['target'] == 'life_expectancy'


class TestHealthDataProcessor:
    """Test cases for HealthDataProcessor."""
    
    @pytest.fixture
    def processor(self):
        """Create a data processor instance."""
        return HealthDataProcessor()
    
    def test_processor_initialization(self, processor):
        """Test processor initialization."""
        assert processor.country_mapping is not None
        assert processor.metric_mapping is not None
        assert len(processor.country_mapping) > 0
        assert len(processor.metric_mapping) > 0
    
    def test_get_baseline_data(self, processor):
        """Test baseline data extraction."""
        sample_df = pd.DataFrame({
            'country': ['PRT', 'PRT', 'ESP', 'ESP'],
            'year': [2020, 2022, 2020, 2022],
            'life_expectancy': [81.0, 81.5, 83.0, 83.5],
            'doctor_density': [2.0, 2.2, 2.5, 2.7],
            'nurse_density': [5.0, 5.2, 6.0, 6.2],
            'health_spending': [5.5, 6.0, 7.0, 7.5]
        })
        
        baseline_data = processor.get_baseline_data(sample_df)
        
        assert 'PRT' in baseline_data
        assert 'ESP' in baseline_data
        
        # Check Portugal baseline (most recent year 2022)
        prt_baseline = baseline_data['PRT']
        assert prt_baseline['life_expectancy'] == 81.5
        assert prt_baseline['doctor_density'] == 2.2
        assert prt_baseline['nurse_density'] == 5.2
        assert prt_baseline['health_spending'] == 6.0
        assert prt_baseline['year'] == 2022
        
        # Check Spain baseline (most recent year 2022)
        esp_baseline = baseline_data['ESP']
        assert esp_baseline['life_expectancy'] == 83.5
        assert esp_baseline['doctor_density'] == 2.7
        assert esp_baseline['nurse_density'] == 6.2
        assert esp_baseline['health_spending'] == 7.5
        assert esp_baseline['year'] == 2022
    
    def test_validate_data_quality(self, processor):
        """Test data quality validation."""
        # Good quality data
        good_data = pd.DataFrame({
            'life_expectancy': [80.0, 81.0, 82.0],
            'doctor_density': [2.0, 2.5, 3.0],
            'nurse_density': [5.0, 6.0, 7.0],
            'health_spending': [6.0, 7.0, 8.0]
        })
        
        quality_metrics = processor.validate_data_quality(good_data)
        
        assert 'completeness' in quality_metrics
        assert 'validity' in quality_metrics
        assert 'consistency' in quality_metrics
        assert 'overall_quality' in quality_metrics
        
        # All metrics should be high for good data
        assert quality_metrics['completeness'] > 90
        assert quality_metrics['validity'] > 90
        assert quality_metrics['consistency'] > 90
        assert quality_metrics['overall_quality'] > 90
    
    def test_validate_data_quality_with_issues(self, processor):
        """Test data quality validation with data issues."""
        # Data with issues
        bad_data = pd.DataFrame({
            'life_expectancy': [80.0, np.nan, 200.0],  # Missing and invalid values
            'doctor_density': [2.0, 2.5, 50.0],  # Invalid value
            'nurse_density': [5.0, 6.0, 7.0],
            'health_spending': [6.0, 7.0, 8.0]
        })
        
        quality_metrics = processor.validate_data_quality(bad_data)
        
        # Quality should be lower due to issues
        assert quality_metrics['completeness'] < 100
        assert quality_metrics['validity'] < 100
        assert quality_metrics['overall_quality'] < 100


@pytest.mark.integration
class TestSimulationIntegration:
    """Integration tests for the complete simulation workflow."""
    
    def test_end_to_end_simulation(self):
        """Test complete end-to-end simulation workflow."""
        # Create sample data
        sample_data = pd.DataFrame({
            'country': ['PRT', 'PRT', 'PRT', 'ESP', 'ESP', 'ESP', 'SWE', 'SWE', 'SWE'],
            'year': [2020, 2021, 2022, 2020, 2021, 2022, 2020, 2021, 2022],
            'life_expectancy': [81.0, 81.3, 81.6, 83.0, 83.3, 83.6, 82.5, 82.8, 83.1],
            'doctor_density': [2.0, 2.1, 2.2, 2.5, 2.6, 2.7, 3.0, 3.1, 3.2],
            'nurse_density': [5.0, 5.1, 5.2, 6.0, 6.1, 6.2, 7.0, 7.1, 7.2],
            'health_spending': [5.5, 5.7, 5.9, 7.0, 7.2, 7.4, 8.0, 8.2, 8.4]
        })
        
        # Initialize services
        processor = HealthDataProcessor()
        engine = PolicySimulationEngine()
        
        # Train model
        metrics = engine.train_model(sample_data)
        assert engine.is_trained == True
        assert metrics['r2_score'] > 0
        
        # Get baseline data
        baseline_data = processor.get_baseline_data(sample_data)
        assert len(baseline_data) == 3  # PRT, ESP, SWE
        
        # Run simulation for Portugal
        prt_baseline = baseline_data['PRT']
        parameters = {
            'doctor_density': prt_baseline['doctor_density'] + 0.5,
            'nurse_density': prt_baseline['nurse_density'] + 1.0,
            'health_spending': prt_baseline['health_spending'] + 1.0
        }
        
        result = engine.run_simulation('PRT', prt_baseline, parameters)
        
        # Verify results
        assert result['country'] == 'PRT'
        assert result['prediction']['life_expectancy'] > prt_baseline['life_expectancy']
        assert result['prediction']['change'] > 0  # Should be positive with increased parameters
        
        # Check model performance
        assert result['model_metrics']['r2_score'] > 0.5  # Reasonable R² score
        assert result['metadata']['data_quality'] > 90  # High data quality


if __name__ == '__main__':
    pytest.main([__file__])
