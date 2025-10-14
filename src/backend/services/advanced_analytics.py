"""
Advanced Analytics Service for Policy Simulation Assistant
Provides comprehensive data analysis capabilities including trend analysis,
correlations, forecasting, and statistical significance testing.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import structlog

logger = structlog.get_logger()

class AdvancedAnalyticsService:
    """Advanced analytics service for comprehensive data analysis"""
    
    def __init__(self, data_processor):
        self.data_processor = data_processor
        self.analytics_cache = {}
        
    def perform_trend_analysis(
        self, 
        indicator: str, 
        country: str, 
        time_period: Optional[Tuple[int, int]] = None
    ) -> Dict[str, Any]:
        """
        Perform trend analysis on health indicators over time
        
        Args:
            indicator: Health indicator to analyze (e.g., 'life_expectancy')
            country: Country code to analyze
            time_period: Optional tuple of (start_year, end_year)
            
        Returns:
            Dictionary containing trend analysis results
        """
        logger.info("Performing trend analysis", indicator=indicator, country=country)
        
        try:
            # Get data for the indicator and country
            df = self._get_indicator_data(indicator, country, time_period)
            
            if df.empty:
                return {"error": "No data available for the specified parameters"}
            
            # Calculate trend statistics
            years = df['year'].values
            values = df['value'].values
            
            # Linear regression for trend
            slope, intercept, r_value, p_value, std_err = stats.linregress(years, values)
            
            # Calculate trend direction and strength
            trend_direction = "increasing" if slope > 0 else "decreasing" if slope < 0 else "stable"
            trend_strength = abs(r_value)
            
            # Calculate confidence interval for trend
            n = len(years)
            t_critical = stats.t.ppf(0.975, n - 2)  # 95% confidence
            margin_error = t_critical * std_err
            confidence_interval = {
                "lower": slope - margin_error,
                "upper": slope + margin_error
            }
            
            # Calculate annual change
            annual_change = slope
            total_change = slope * (years[-1] - years[0])
            change_percentage = (total_change / values[0]) * 100 if values[0] != 0 else 0
            
            result = {
                "indicator": indicator,
                "country": country,
                "time_period": {
                    "start": int(years[0]),
                    "end": int(years[-1])
                },
                "trend_direction": trend_direction,
                "trend_strength": float(trend_strength),
                "annual_change": float(annual_change),
                "total_change": float(total_change),
                "change_percentage": float(change_percentage),
                "statistical_significance": float(p_value),
                "confidence_interval": confidence_interval,
                "r_squared": float(r_value ** 2),
                "sample_size": n,
                "data_points": [
                    {"year": int(year), "value": float(value)} 
                    for year, value in zip(years, values)
                ]
            }
            
            logger.info("Trend analysis completed", 
                       trend_direction=trend_direction, 
                       significance=p_value)
            
            return result
            
        except Exception as e:
            logger.error("Error in trend analysis", error=str(e))
            return {"error": f"Trend analysis failed: {str(e)}"}
    
    def calculate_correlations(
        self, 
        indicators: List[str], 
        countries: Optional[List[str]] = None,
        time_period: Optional[Tuple[int, int]] = None
    ) -> Dict[str, Any]:
        """
        Calculate correlation matrix between health indicators
        
        Args:
            indicators: List of indicators to correlate
            countries: Optional list of countries to include
            time_period: Optional tuple of (start_year, end_year)
            
        Returns:
            Dictionary containing correlation matrix and analysis
        """
        logger.info("Calculating correlations", indicators=indicators, countries=countries)
        
        try:
            # Get data for all indicators
            correlation_data = {}
            
            for indicator in indicators:
                if countries:
                    for country in countries:
                        df = self._get_indicator_data(indicator, country, time_period)
                        if not df.empty:
                            key = f"{indicator}_{country}"
                            correlation_data[key] = df
                else:
                    # Get data for all countries
                    df = self._get_indicator_data(indicator, None, time_period)
                    if not df.empty:
                        correlation_data[indicator] = df
            
            if len(correlation_data) < 2:
                return {"error": "Insufficient data for correlation analysis"}
            
            # Create correlation matrix
            correlation_matrix = np.zeros((len(indicators), len(indicators)))
            significance_matrix = np.zeros((len(indicators), len(indicators)))
            
            for i, indicator1 in enumerate(indicators):
                for j, indicator2 in enumerate(indicators):
                    if i == j:
                        correlation_matrix[i][j] = 1.0
                        significance_matrix[i][j] = 0.0
                    else:
                        # Calculate correlation between indicators
                        corr, p_value = self._calculate_indicator_correlation(
                            indicator1, indicator2, countries, time_period
                        )
                        correlation_matrix[i][j] = corr
                        significance_matrix[i][j] = p_value
            
            # Generate interpretation
            interpretation = self._interpret_correlation_matrix(
                indicators, correlation_matrix, significance_matrix
            )
            
            result = {
                "indicators": indicators,
                "countries": countries,
                "time_period": time_period,
                "correlation_matrix": correlation_matrix.tolist(),
                "significance_matrix": significance_matrix.tolist(),
                "interpretation": interpretation,
                "sample_size": len(correlation_data),
                "generated_at": datetime.utcnow().isoformat()
            }
            
            logger.info("Correlation analysis completed", 
                       indicators_count=len(indicators))
            
            return result
            
        except Exception as e:
            logger.error("Error in correlation analysis", error=str(e))
            return {"error": f"Correlation analysis failed: {str(e)}"}
    
    def generate_forecast(
        self, 
        indicator: str, 
        country: str, 
        forecast_years: int = 5,
        confidence_level: float = 0.95
    ) -> Dict[str, Any]:
        """
        Generate forecast for health indicators
        
        Args:
            indicator: Health indicator to forecast
            country: Country code
            forecast_years: Number of years to forecast
            confidence_level: Confidence level for prediction intervals
            
        Returns:
            Dictionary containing forecast results
        """
        logger.info("Generating forecast", 
                   indicator=indicator, 
                   country=country, 
                   years=forecast_years)
        
        try:
            # Get historical data
            df = self._get_indicator_data(indicator, country)
            
            if df.empty or len(df) < 3:
                return {"error": "Insufficient historical data for forecasting"}
            
            # Prepare data for forecasting
            years = df['year'].values
            values = df['value'].values
            
            # Fit linear regression model
            X = years.reshape(-1, 1)
            y = values
            
            model = LinearRegression()
            model.fit(X, y)
            
            # Generate forecast
            last_year = int(years[-1])
            forecast_years_list = list(range(last_year + 1, last_year + forecast_years + 1))
            X_forecast = np.array(forecast_years_list).reshape(-1, 1)
            
            # Predictions
            predictions = model.predict(X_forecast)
            
            # Calculate prediction intervals
            residuals = y - model.predict(X)
            mse = np.mean(residuals ** 2)
            std_error = np.sqrt(mse)
            
            # T-distribution critical value
            t_critical = stats.t.ppf((1 + confidence_level) / 2, len(y) - 2)
            margin_error = t_critical * std_error * np.sqrt(1 + 1/len(y))
            
            # Create forecast data points
            forecast_points = []
            for year, pred in zip(forecast_years_list, predictions):
                forecast_points.append({
                    "year": int(year),
                    "predicted_value": float(pred),
                    "confidence_interval": {
                        "lower": float(pred - margin_error),
                        "upper": float(pred + margin_error)
                    }
                })
            
            # Model performance metrics
            r2 = r2_score(y, model.predict(X))
            rmse = np.sqrt(mean_squared_error(y, model.predict(X)))
            
            result = {
                "indicator": indicator,
                "country": country,
                "forecast_years": forecast_years,
                "confidence_level": confidence_level,
                "model_performance": {
                    "r_squared": float(r2),
                    "rmse": float(rmse),
                    "trend_slope": float(model.coef_[0]),
                    "intercept": float(model.intercept_)
                },
                "historical_data": [
                    {"year": int(year), "value": float(value)} 
                    for year, value in zip(years, values)
                ],
                "forecast_data": forecast_points,
                "generated_at": datetime.utcnow().isoformat()
            }
            
            logger.info("Forecast generated successfully", 
                       r_squared=r2, 
                       rmse=rmse)
            
            return result
            
        except Exception as e:
            logger.error("Error in forecast generation", error=str(e))
            return {"error": f"Forecast generation failed: {str(e)}"}
    
    def statistical_significance_test(
        self, 
        indicator: str, 
        country1: str, 
        country2: str,
        time_period: Optional[Tuple[int, int]] = None
    ) -> Dict[str, Any]:
        """
        Perform statistical significance test between two countries
        
        Args:
            indicator: Health indicator to compare
            country1: First country code
            country2: Second country code
            time_period: Optional tuple of (start_year, end_year)
            
        Returns:
            Dictionary containing statistical test results
        """
        logger.info("Performing statistical significance test", 
                   indicator=indicator, 
                   country1=country1, 
                   country2=country2)
        
        try:
            # Get data for both countries
            df1 = self._get_indicator_data(indicator, country1, time_period)
            df2 = self._get_indicator_data(indicator, country2, time_period)
            
            if df1.empty or df2.empty:
                return {"error": "Insufficient data for statistical test"}
            
            # Extract values
            values1 = df1['value'].values
            values2 = df2['value'].values
            
            # Perform t-test
            t_stat, p_value = stats.ttest_ind(values1, values2)
            
            # Calculate effect size (Cohen's d)
            pooled_std = np.sqrt(((len(values1) - 1) * np.var(values1, ddof=1) + 
                                 (len(values2) - 1) * np.var(values2, ddof=1)) / 
                                (len(values1) + len(values2) - 2))
            cohens_d = (np.mean(values1) - np.mean(values2)) / pooled_std
            
            # Determine significance level
            if p_value < 0.001:
                significance_level = "highly significant (p < 0.001)"
            elif p_value < 0.01:
                significance_level = "very significant (p < 0.01)"
            elif p_value < 0.05:
                significance_level = "significant (p < 0.05)"
            elif p_value < 0.1:
                significance_level = "marginally significant (p < 0.1)"
            else:
                significance_level = "not significant (p >= 0.1)"
            
            # Effect size interpretation
            if abs(cohens_d) < 0.2:
                effect_size_interpretation = "negligible"
            elif abs(cohens_d) < 0.5:
                effect_size_interpretation = "small"
            elif abs(cohens_d) < 0.8:
                effect_size_interpretation = "medium"
            else:
                effect_size_interpretation = "large"
            
            result = {
                "indicator": indicator,
                "country1": country1,
                "country2": country2,
                "time_period": time_period,
                "test_results": {
                    "t_statistic": float(t_stat),
                    "p_value": float(p_value),
                    "significance_level": significance_level,
                    "cohens_d": float(cohens_d),
                    "effect_size_interpretation": effect_size_interpretation
                },
                "descriptive_statistics": {
                    "country1": {
                        "mean": float(np.mean(values1)),
                        "std": float(np.std(values1)),
                        "n": len(values1)
                    },
                    "country2": {
                        "mean": float(np.mean(values2)),
                        "std": float(np.std(values2)),
                        "n": len(values2)
                    }
                },
                "interpretation": self._interpret_statistical_test(
                    country1, country2, p_value, cohens_d
                ),
                "generated_at": datetime.utcnow().isoformat()
            }
            
            logger.info("Statistical test completed", 
                       p_value=p_value, 
                       significance=significance_level)
            
            return result
            
        except Exception as e:
            logger.error("Error in statistical significance test", error=str(e))
            return {"error": f"Statistical test failed: {str(e)}"}
    
    def multi_variable_regression(
        self, 
        target_indicator: str, 
        predictor_indicators: List[str],
        countries: Optional[List[str]] = None,
        time_period: Optional[Tuple[int, int]] = None
    ) -> Dict[str, Any]:
        """
        Perform multi-variable regression analysis
        
        Args:
            target_indicator: Target variable for regression
            predictor_indicators: List of predictor variables
            countries: Optional list of countries to include
            time_period: Optional tuple of (start_year, end_year)
            
        Returns:
            Dictionary containing regression analysis results
        """
        logger.info("Performing multi-variable regression", 
                   target=target_indicator, 
                   predictors=predictor_indicators)
        
        try:
            # Prepare data for regression
            regression_data = self._prepare_regression_data(
                target_indicator, predictor_indicators, countries, time_period
            )
            
            if regression_data.empty:
                return {"error": "Insufficient data for regression analysis"}
            
            # Separate target and predictors
            target = regression_data[target_indicator].values
            predictors = regression_data[predictor_indicators].values
            
            # Fit regression model
            model = LinearRegression()
            model.fit(predictors, target)
            
            # Calculate predictions
            predictions = model.predict(predictors)
            
            # Model performance metrics
            r2 = r2_score(target, predictions)
            mse = mean_squared_error(target, predictions)
            rmse = np.sqrt(mse)
            
            # Feature importance (coefficients)
            feature_importance = dict(zip(predictor_indicators, model.coef_))
            
            # Calculate residuals
            residuals = target - predictions
            
            # Statistical significance of coefficients
            n = len(target)
            k = len(predictor_indicators)
            df_residual = n - k - 1
            
            # Standard errors of coefficients
            mse_residual = np.sum(residuals ** 2) / df_residual
            X_with_intercept = np.column_stack([np.ones(len(predictors)), predictors])
            try:
                cov_matrix = mse_residual * np.linalg.inv(X_with_intercept.T @ X_with_intercept)
                std_errors = np.sqrt(np.diag(cov_matrix))[1:]  # Exclude intercept
            except np.linalg.LinAlgError:
                std_errors = np.full(len(predictor_indicators), np.nan)
            
            # T-statistics and p-values
            t_stats = model.coef_ / std_errors
            p_values = 2 * (1 - stats.t.cdf(np.abs(t_stats), df_residual))
            
            # Coefficient significance
            coefficient_significance = {}
            for i, indicator in enumerate(predictor_indicators):
                coefficient_significance[indicator] = {
                    "coefficient": float(model.coef_[i]),
                    "std_error": float(std_errors[i]) if not np.isnan(std_errors[i]) else None,
                    "t_statistic": float(t_stats[i]) if not np.isnan(t_stats[i]) else None,
                    "p_value": float(p_values[i]) if not np.isnan(p_values[i]) else None,
                    "significant": p_values[i] < 0.05 if not np.isnan(p_values[i]) else False
                }
            
            result = {
                "target_indicator": target_indicator,
                "predictor_indicators": predictor_indicators,
                "countries": countries,
                "time_period": time_period,
                "model_performance": {
                    "r_squared": float(r2),
                    "adjusted_r_squared": float(1 - (1 - r2) * (n - 1) / df_residual),
                    "mse": float(mse),
                    "rmse": float(rmse),
                    "intercept": float(model.intercept_)
                },
                "feature_importance": {k: float(v) for k, v in feature_importance.items()},
                "coefficient_significance": coefficient_significance,
                "sample_size": n,
                "degrees_of_freedom": df_residual,
                "interpretation": self._interpret_regression_results(
                    target_indicator, predictor_indicators, r2, feature_importance
                ),
                "generated_at": datetime.utcnow().isoformat()
            }
            
            logger.info("Multi-variable regression completed", 
                       r_squared=r2, 
                       predictors_count=len(predictor_indicators))
            
            return result
            
        except Exception as e:
            logger.error("Error in multi-variable regression", error=str(e))
            return {"error": f"Regression analysis failed: {str(e)}"}
    
    def _get_indicator_data(
        self, 
        indicator: str, 
        country: Optional[str] = None,
        time_period: Optional[Tuple[int, int]] = None
    ) -> pd.DataFrame:
        """Get data for a specific indicator and country"""
        try:
            # This would integrate with the actual data processor
            # For now, return mock data structure
            if hasattr(self.data_processor, 'merged_df') and self.data_processor.merged_df is not None:
                df = self.data_processor.merged_df.copy()
                
                # Filter by indicator
                if indicator in df.columns:
                    df = df[['year', 'country', indicator]].dropna()
                    df = df.rename(columns={indicator: 'value'})
                    
                    # Filter by country if specified
                    if country:
                        df = df[df['country'] == country]
                    
                    # Filter by time period if specified
                    if time_period:
                        start_year, end_year = time_period
                        df = df[(df['year'] >= start_year) & (df['year'] <= end_year)]
                    
                    return df.sort_values('year')
            
            # Return empty DataFrame if no data available
            return pd.DataFrame(columns=['year', 'country', 'value'])
            
        except Exception as e:
            logger.error("Error getting indicator data", error=str(e))
            return pd.DataFrame(columns=['year', 'country', 'value'])
    
    def _calculate_indicator_correlation(
        self, 
        indicator1: str, 
        indicator2: str, 
        countries: Optional[List[str]] = None,
        time_period: Optional[Tuple[int, int]] = None
    ) -> Tuple[float, float]:
        """Calculate correlation between two indicators"""
        try:
            df1 = self._get_indicator_data(indicator1, None, time_period)
            df2 = self._get_indicator_data(indicator2, None, time_period)
            
            if df1.empty or df2.empty:
                return 0.0, 1.0
            
            # Merge data on year and country
            merged = pd.merge(df1, df2, on=['year', 'country'], suffixes=('_1', '_2'))
            
            if merged.empty:
                return 0.0, 1.0
            
            # Calculate correlation
            corr, p_value = stats.pearsonr(merged['value_1'], merged['value_2'])
            
            return float(corr), float(p_value)
            
        except Exception as e:
            logger.error("Error calculating correlation", error=str(e))
            return 0.0, 1.0
    
    def _prepare_regression_data(
        self, 
        target_indicator: str, 
        predictor_indicators: List[str],
        countries: Optional[List[str]] = None,
        time_period: Optional[Tuple[int, int]] = None
    ) -> pd.DataFrame:
        """Prepare data for regression analysis"""
        try:
            # Get data for target indicator
            target_df = self._get_indicator_data(target_indicator, None, time_period)
            
            if target_df.empty:
                return pd.DataFrame()
            
            # Get data for predictor indicators
            predictor_dfs = []
            for indicator in predictor_indicators:
                df = self._get_indicator_data(indicator, None, time_period)
                if not df.empty:
                    predictor_dfs.append(df)
            
            if not predictor_dfs:
                return pd.DataFrame()
            
            # Merge all data
            merged = target_df.copy()
            for df in predictor_dfs:
                merged = pd.merge(merged, df, on=['year', 'country'], how='inner')
            
            # Filter by countries if specified
            if countries:
                merged = merged[merged['country'].isin(countries)]
            
            # Remove rows with missing values
            merged = merged.dropna()
            
            return merged
            
        except Exception as e:
            logger.error("Error preparing regression data", error=str(e))
            return pd.DataFrame()
    
    def _interpret_correlation_matrix(
        self, 
        indicators: List[str], 
        correlation_matrix: np.ndarray, 
        significance_matrix: np.ndarray
    ) -> str:
        """Generate interpretation of correlation matrix"""
        interpretations = []
        
        for i in range(len(indicators)):
            for j in range(i + 1, len(indicators)):
                corr = correlation_matrix[i][j]
                p_value = significance_matrix[i][j]
                
                if p_value < 0.05:
                    if abs(corr) > 0.7:
                        strength = "strong"
                    elif abs(corr) > 0.5:
                        strength = "moderate"
                    else:
                        strength = "weak"
                    
                    direction = "positive" if corr > 0 else "negative"
                    
                    interpretations.append(
                        f"{indicators[i]} and {indicators[j]} show a {strength} "
                        f"{direction} correlation (r = {corr:.3f}, p = {p_value:.3f})"
                    )
        
        return "; ".join(interpretations) if interpretations else "No significant correlations found"
    
    def _interpret_statistical_test(
        self, 
        country1: str, 
        country2: str, 
        p_value: float, 
        cohens_d: float
    ) -> str:
        """Generate interpretation of statistical test results"""
        if p_value < 0.05:
            significance = "statistically significant"
        else:
            significance = "not statistically significant"
        
        if abs(cohens_d) < 0.2:
            effect_size = "negligible"
        elif abs(cohens_d) < 0.5:
            effect_size = "small"
        elif abs(cohens_d) < 0.8:
            effect_size = "medium"
        else:
            effect_size = "large"
        
        return (f"The difference between {country1} and {country2} is {significance} "
                f"(p = {p_value:.3f}) with a {effect_size} effect size (Cohen's d = {cohens_d:.3f})")
    
    def _interpret_regression_results(
        self, 
        target: str, 
        predictors: List[str], 
        r2: float, 
        feature_importance: Dict[str, float]
    ) -> str:
        """Generate interpretation of regression results"""
        interpretation = f"The regression model explains {r2:.1%} of the variance in {target}. "
        
        # Find most important predictors
        sorted_predictors = sorted(feature_importance.items(), key=lambda x: abs(x[1]), reverse=True)
        
        if sorted_predictors:
            top_predictor = sorted_predictors[0]
            interpretation += f"The most important predictor is {top_predictor[0]} "
            
            if top_predictor[1] > 0:
                interpretation += f"(positive effect: {top_predictor[1]:.3f})."
            else:
                interpretation += f"(negative effect: {top_predictor[1]:.3f})."
        
        return interpretation
