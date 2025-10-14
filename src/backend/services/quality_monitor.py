"""
Data Quality Monitoring Service
Provides real-time quality monitoring, validation, and provenance tracking
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import structlog
from dataclasses import dataclass
from enum import Enum

logger = structlog.get_logger()

class QualityAlertType(Enum):
    COMPLETENESS = "completeness"
    VALIDITY = "validity"
    CONSISTENCY = "consistency"
    FRESHNESS = "freshness"

class QualityAlertSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class QualityAlert:
    id: str
    type: QualityAlertType
    severity: QualityAlertSeverity
    message: str
    affected_indicators: List[str]
    created_at: datetime
    resolved: bool = False

@dataclass
class QualityMetrics:
    overall_score: float
    completeness_score: float
    validity_score: float
    consistency_score: float
    freshness_score: float
    last_updated: datetime
    trend: str  # 'up', 'down', 'stable'
    alerts: List[QualityAlert]

@dataclass
class QualityBreakdown:
    by_indicator: Dict[str, float]
    by_country: Dict[str, float]
    by_source: Dict[str, float]
    by_time_period: Dict[str, float]

@dataclass
class ValidationResult:
    dataset_id: str
    validation_timestamp: datetime
    overall_status: str  # 'pass', 'warning', 'fail'
    completeness_check: Dict[str, Any]
    validity_check: Dict[str, Any]
    consistency_check: Dict[str, Any]
    outlier_check: Dict[str, Any]
    issues: List[Dict[str, Any]]

@dataclass
class DataSource:
    name: str
    url: str
    last_updated: datetime
    reliability_score: float
    coverage: List[str]

@dataclass
class ProcessingStep:
    step_id: str
    description: str
    timestamp: datetime
    input_data: str
    output_data: str
    parameters: Dict[str, Any]

@dataclass
class ProvenanceData:
    dataset_id: str
    original_sources: List[DataSource]
    processing_steps: List[ProcessingStep]
    transformations: List[Dict[str, Any]]
    version_history: List[Dict[str, Any]]
    audit_trail: List[Dict[str, Any]]

class DataQualityMonitor:
    """Real-time data quality monitoring and validation service"""
    
    def __init__(self):
        self.quality_threshold = 95.0
        self.freshness_threshold_days = 3
        self.outlier_threshold_sigma = 3.0
        self.quality_history = []
        self.alerts = []
        
    def calculate_quality_score(self, data: pd.DataFrame, metadata: Dict[str, Any]) -> QualityMetrics:
        """Calculate comprehensive quality score for a dataset"""
        logger.info("Calculating quality score", dataset_id=metadata.get('dataset_id'))
        
        # Calculate individual quality components
        completeness_score = self._calculate_completeness_score(data)
        validity_score = self._calculate_validity_score(data, metadata)
        consistency_score = self._calculate_consistency_score(data, metadata)
        freshness_score = self._calculate_freshness_score(metadata)
        
        # Calculate overall weighted score
        overall_score = (
            completeness_score * 0.3 +
            validity_score * 0.3 +
            consistency_score * 0.2 +
            freshness_score * 0.2
        )
        
        # Determine trend
        trend = self._calculate_quality_trend(overall_score)
        
        # Generate alerts
        alerts = self._generate_quality_alerts(
            completeness_score, validity_score, consistency_score, freshness_score, metadata
        )
        
        quality_metrics = QualityMetrics(
            overall_score=overall_score,
            completeness_score=completeness_score,
            validity_score=validity_score,
            consistency_score=consistency_score,
            freshness_score=freshness_score,
            last_updated=datetime.now(),
            trend=trend,
            alerts=alerts
        )
        
        # Store in history
        self.quality_history.append(quality_metrics)
        
        logger.info(
            "Quality score calculated",
            overall_score=overall_score,
            completeness=completeness_score,
            validity=validity_score,
            consistency=consistency_score,
            freshness=freshness_score
        )
        
        return quality_metrics
    
    def _calculate_completeness_score(self, data: pd.DataFrame) -> float:
        """Calculate data completeness score (0-100)"""
        if data.empty:
            return 0.0
        
        total_cells = data.size
        non_null_cells = data.count().sum()
        completeness_ratio = non_null_cells / total_cells
        return completeness_ratio * 100
    
    def _calculate_validity_score(self, data: pd.DataFrame, metadata: Dict[str, Any]) -> float:
        """Calculate data validity score (0-100)"""
        if data.empty:
            return 0.0
        
        validity_issues = 0
        total_checks = 0
        
        # Check numeric columns for valid ranges
        numeric_columns = data.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            if col in metadata.get('valid_ranges', {}):
                min_val, max_val = metadata['valid_ranges'][col]
                invalid_count = ((data[col] < min_val) | (data[col] > max_val)).sum()
                validity_issues += invalid_count
                total_checks += len(data[col])
        
        # Check for negative values where not expected
        for col in numeric_columns:
            if col in ['life_expectancy', 'doctor_density', 'nurse_density', 'health_spending']:
                negative_count = (data[col] < 0).sum()
                validity_issues += negative_count
                total_checks += len(data[col])
        
        if total_checks == 0:
            return 100.0
        
        validity_ratio = 1 - (validity_issues / total_checks)
        return max(0, validity_ratio * 100)
    
    def _calculate_consistency_score(self, data: pd.DataFrame, metadata: Dict[str, Any]) -> float:
        """Calculate data consistency score (0-100)"""
        if data.empty or len(data) < 2:
            return 100.0
        
        consistency_issues = 0
        total_checks = 0
        
        # Check for logical consistency (e.g., life expectancy should be reasonable)
        if 'life_expectancy' in data.columns:
            # Life expectancy should be between 30 and 120 years
            invalid_le = ((data['life_expectancy'] < 30) | (data['life_expectancy'] > 120)).sum()
            consistency_issues += invalid_le
            total_checks += len(data['life_expectancy'])
        
        # Check for country-year consistency (no duplicate entries)
        if 'country' in data.columns and 'year' in data.columns:
            duplicates = data.duplicated(subset=['country', 'year']).sum()
            consistency_issues += duplicates
            total_checks += len(data)
        
        if total_checks == 0:
            return 100.0
        
        consistency_ratio = 1 - (consistency_issues / total_checks)
        return max(0, consistency_ratio * 100)
    
    def _calculate_freshness_score(self, metadata: Dict[str, Any]) -> float:
        """Calculate data freshness score (0-100)"""
        last_updated = metadata.get('last_updated')
        if not last_updated:
            return 0.0
        
        if isinstance(last_updated, str):
            last_updated = datetime.fromisoformat(last_updated.replace('Z', '+00:00'))
        
        days_old = (datetime.now() - last_updated).days
        
        if days_old <= 1:
            return 100.0
        elif days_old <= self.freshness_threshold_days:
            # Linear decay from 100% to 80% over threshold period
            decay_ratio = (self.freshness_threshold_days - days_old) / self.freshness_threshold_days
            return 80 + (20 * decay_ratio)
        else:
            # Exponential decay beyond threshold
            excess_days = days_old - self.freshness_threshold_days
            return max(0, 80 * (0.8 ** excess_days))
    
    def _calculate_quality_trend(self, current_score: float) -> str:
        """Calculate quality trend based on historical data"""
        if len(self.quality_history) < 2:
            return 'stable'
        
        recent_scores = [qm.overall_score for qm in self.quality_history[-5:]]
        if len(recent_scores) < 2:
            return 'stable'
        
        # Calculate trend
        score_change = current_score - recent_scores[-2]
        
        if score_change > 1.0:
            return 'up'
        elif score_change < -1.0:
            return 'down'
        else:
            return 'stable'
    
    def _generate_quality_alerts(
        self, 
        completeness: float, 
        validity: float, 
        consistency: float, 
        freshness: float,
        metadata: Dict[str, Any]
    ) -> List[QualityAlert]:
        """Generate quality alerts based on scores"""
        alerts = []
        
        # Completeness alerts
        if completeness < self.quality_threshold:
            severity = QualityAlertSeverity.CRITICAL if completeness < 80 else QualityAlertSeverity.HIGH
            alerts.append(QualityAlert(
                id=f"completeness_{datetime.now().isoformat()}",
                type=QualityAlertType.COMPLETENESS,
                severity=severity,
                message=f"Data completeness below threshold: {completeness:.1f}%",
                affected_indicators=metadata.get('indicators', []),
                created_at=datetime.now()
            ))
        
        # Validity alerts
        if validity < self.quality_threshold:
            severity = QualityAlertSeverity.HIGH if validity < 85 else QualityAlertSeverity.MEDIUM
            alerts.append(QualityAlert(
                id=f"validity_{datetime.now().isoformat()}",
                type=QualityAlertType.VALIDITY,
                severity=severity,
                message=f"Data validity below threshold: {validity:.1f}%",
                affected_indicators=metadata.get('indicators', []),
                created_at=datetime.now()
            ))
        
        # Freshness alerts
        if freshness < 80:
            severity = QualityAlertSeverity.MEDIUM if freshness > 60 else QualityAlertSeverity.HIGH
            alerts.append(QualityAlert(
                id=f"freshness_{datetime.now().isoformat()}",
                type=QualityAlertType.FRESHNESS,
                severity=severity,
                message=f"Data freshness below threshold: {freshness:.1f}%",
                affected_indicators=metadata.get('indicators', []),
                created_at=datetime.now()
            ))
        
        return alerts
    
    def validate_data(self, data: pd.DataFrame, metadata: Dict[str, Any]) -> ValidationResult:
        """Comprehensive data validation"""
        logger.info("Validating data", dataset_id=metadata.get('dataset_id'))
        
        validation_timestamp = datetime.now()
        
        # Run validation checks
        completeness_check = self._validate_completeness(data)
        validity_check = self._validate_validity(data, metadata)
        consistency_check = self._validate_consistency(data, metadata)
        outlier_check = self._validate_outliers(data, metadata)
        
        # Determine overall status
        all_checks = [completeness_check, validity_check, consistency_check, outlier_check]
        overall_status = self._determine_overall_status(all_checks)
        
        # Collect all issues
        issues = []
        for check in all_checks:
            if check['status'] != 'pass':
                issues.append(check)
        
        validation_result = ValidationResult(
            dataset_id=metadata.get('dataset_id', 'unknown'),
            validation_timestamp=validation_timestamp,
            overall_status=overall_status,
            completeness_check=completeness_check,
            validity_check=validity_check,
            consistency_check=consistency_check,
            outlier_check=outlier_check,
            issues=issues
        )
        
        logger.info("Data validation completed", status=overall_status, issues_count=len(issues))
        return validation_result
    
    def _validate_completeness(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Validate data completeness"""
        if data.empty:
            return {
                'status': 'fail',
                'score': 0,
                'details': 'Dataset is empty',
                'recommendations': ['Check data source and ingestion process']
            }
        
        total_cells = data.size
        non_null_cells = data.count().sum()
        completeness_ratio = non_null_cells / total_cells
        score = completeness_ratio * 100
        
        if score >= 95:
            status = 'pass'
        elif score >= 80:
            status = 'warning'
        else:
            status = 'fail'
        
        return {
            'status': status,
            'score': score,
            'details': f'Completeness: {score:.1f}% ({non_null_cells}/{total_cells} cells)',
            'recommendations': ['Check for missing data in source systems'] if status != 'pass' else []
        }
    
    def _validate_validity(self, data: pd.DataFrame, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data validity"""
        if data.empty:
            return {
                'status': 'pass',
                'score': 100,
                'details': 'No data to validate',
                'recommendations': []
            }
        
        validity_issues = 0
        total_checks = 0
        
        # Check numeric columns
        numeric_columns = data.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            if col in ['life_expectancy', 'doctor_density', 'nurse_density', 'health_spending']:
                # Check for negative values
                negative_count = (data[col] < 0).sum()
                validity_issues += negative_count
                total_checks += len(data[col])
                
                # Check for unreasonably high values
                if col == 'life_expectancy':
                    high_count = (data[col] > 120).sum()
                    validity_issues += high_count
                    total_checks += len(data[col])
        
        if total_checks == 0:
            return {
                'status': 'pass',
                'score': 100,
                'details': 'No numeric data to validate',
                'recommendations': []
            }
        
        validity_ratio = 1 - (validity_issues / total_checks)
        score = validity_ratio * 100
        
        if score >= 95:
            status = 'pass'
        elif score >= 85:
            status = 'warning'
        else:
            status = 'fail'
        
        return {
            'status': status,
            'score': score,
            'details': f'Validity: {score:.1f}% ({validity_issues} issues found)',
            'recommendations': ['Review data source for invalid values'] if status != 'pass' else []
        }
    
    def _validate_consistency(self, data: pd.DataFrame, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data consistency"""
        if data.empty or len(data) < 2:
            return {
                'status': 'pass',
                'score': 100,
                'details': 'Insufficient data for consistency check',
                'recommendations': []
            }
        
        consistency_issues = 0
        total_checks = 0
        
        # Check for duplicate entries
        if 'country' in data.columns and 'year' in data.columns:
            duplicates = data.duplicated(subset=['country', 'year']).sum()
            consistency_issues += duplicates
            total_checks += len(data)
        
        # Check for logical consistency
        if 'life_expectancy' in data.columns:
            # Life expectancy should be reasonable
            invalid_le = ((data['life_expectancy'] < 30) | (data['life_expectancy'] > 120)).sum()
            consistency_issues += invalid_le
            total_checks += len(data['life_expectancy'])
        
        if total_checks == 0:
            return {
                'status': 'pass',
                'score': 100,
                'details': 'No consistency checks applicable',
                'recommendations': []
            }
        
        consistency_ratio = 1 - (consistency_issues / total_checks)
        score = consistency_ratio * 100
        
        if score >= 95:
            status = 'pass'
        elif score >= 85:
            status = 'warning'
        else:
            status = 'fail'
        
        return {
            'status': status,
            'score': score,
            'details': f'Consistency: {score:.1f}% ({consistency_issues} issues found)',
            'recommendations': ['Check for duplicate entries and logical inconsistencies'] if status != 'pass' else []
        }
    
    def _validate_outliers(self, data: pd.DataFrame, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Validate for statistical outliers"""
        if data.empty or len(data) < 10:
            return {
                'status': 'pass',
                'score': 100,
                'details': 'Insufficient data for outlier detection',
                'recommendations': []
            }
        
        outlier_issues = 0
        total_checks = 0
        
        # Check numeric columns for outliers
        numeric_columns = data.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            if col in ['life_expectancy', 'doctor_density', 'nurse_density', 'health_spending']:
                # Use z-score method for outlier detection
                z_scores = np.abs((data[col] - data[col].mean()) / data[col].std())
                outliers = (z_scores > self.outlier_threshold_sigma).sum()
                outlier_issues += outliers
                total_checks += len(data[col])
        
        if total_checks == 0:
            return {
                'status': 'pass',
                'score': 100,
                'details': 'No numeric data for outlier detection',
                'recommendations': []
            }
        
        outlier_ratio = 1 - (outlier_issues / total_checks)
        score = outlier_ratio * 100
        
        if score >= 95:
            status = 'pass'
        elif score >= 85:
            status = 'warning'
        else:
            status = 'fail'
        
        return {
            'status': status,
            'score': score,
            'details': f'Outlier check: {score:.1f}% ({outlier_issues} outliers found)',
            'recommendations': ['Review outliers for data quality issues'] if status != 'pass' else []
        }
    
    def _determine_overall_status(self, checks: List[Dict[str, Any]]) -> str:
        """Determine overall validation status"""
        if any(check['status'] == 'fail' for check in checks):
            return 'fail'
        elif any(check['status'] == 'warning' for check in checks):
            return 'warning'
        else:
            return 'pass'
    
    def get_quality_breakdown(self, data: pd.DataFrame, metadata: Dict[str, Any]) -> QualityBreakdown:
        """Get detailed quality breakdown by various dimensions"""
        logger.info("Generating quality breakdown")
        
        # Calculate quality by indicator
        by_indicator = {}
        if 'indicator' in data.columns:
            for indicator in data['indicator'].unique():
                indicator_data = data[data['indicator'] == indicator]
                quality_metrics = self.calculate_quality_score(indicator_data, metadata)
                by_indicator[indicator] = quality_metrics.overall_score
        
        # Calculate quality by country
        by_country = {}
        if 'country' in data.columns:
            for country in data['country'].unique():
                country_data = data[data['country'] == country]
                quality_metrics = self.calculate_quality_score(country_data, metadata)
                by_country[country] = quality_metrics.overall_score
        
        # Calculate quality by source
        by_source = {}
        if 'source' in data.columns:
            for source in data['source'].unique():
                source_data = data[data['source'] == source]
                quality_metrics = self.calculate_quality_score(source_data, metadata)
                by_source[source] = quality_metrics.overall_score
        
        # Calculate quality by time period
        by_time_period = {}
        if 'year' in data.columns:
            for year in data['year'].unique():
                year_data = data[data['year'] == year]
                quality_metrics = self.calculate_quality_score(year_data, metadata)
                by_time_period[str(year)] = quality_metrics.overall_score
        
        return QualityBreakdown(
            by_indicator=by_indicator,
            by_country=by_country,
            by_source=by_source,
            by_time_period=by_time_period
        )
    
    def get_quality_trends(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get quality trends over specified period"""
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_metrics = [qm for qm in self.quality_history if qm.last_updated >= cutoff_date]
        
        trends = []
        for metrics in recent_metrics:
            trends.append({
                'timestamp': metrics.last_updated.isoformat(),
                'overall_score': metrics.overall_score,
                'completeness_score': metrics.completeness_score,
                'validity_score': metrics.validity_score,
                'consistency_score': metrics.consistency_score,
                'freshness_score': metrics.freshness_score,
                'alert_count': len(metrics.alerts)
            })
        
        return trends
