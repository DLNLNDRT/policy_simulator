"""
Benchmark dashboard service
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import structlog
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from scipy import stats

from src.backend.models.benchmark_models import (
    CountryComparison, CountryRanking, HealthMetric, AnomalyAlert, 
    PeerGroup, ComparisonRequest, AnomalyDetectionRequest, 
    AnomalyDetectionResponse, PeerGroupRequest, PeerGroupResponse,
    MetricType, TrendDirection, AnomalySeverity
)
from src.backend.core.exceptions import DataNotFoundError, ValidationError

logger = structlog.get_logger()


class BenchmarkService:
    """Service for health benchmark analysis and comparison"""
    
    def __init__(self, data_processor):
        self.data_processor = data_processor
        self.metric_weights = {
            MetricType.LIFE_EXPECTANCY: 0.4,
            MetricType.DOCTOR_DENSITY: 0.2,
            MetricType.NURSE_DENSITY: 0.2,
            MetricType.HEALTH_SPENDING: 0.2
        }
        
    def compare_countries(self, request: ComparisonRequest) -> CountryComparison:
        """Compare multiple countries across health metrics"""
        logger.info("Starting country comparison", countries=request.countries, metrics=request.metrics)
        
        try:
            # Get data for all countries
            country_data = {}
            for country in request.countries:
                data = self.data_processor.get_country_data(country, request.year)
                if not data:
                    raise DataNotFoundError(f"Data not found for country {country} in year {request.year}")
                country_data[country] = data
            
            # Determine metrics to compare
            metrics = request.metrics or list(MetricType)
            
            # Calculate rankings and percentiles
            rankings = self._calculate_rankings(country_data, metrics, request.year)
            
            # Detect anomalies if requested
            anomalies = []
            if request.include_anomalies:
                anomalies = self._detect_anomalies(country_data, metrics)
            
            # Find peer groups if requested
            peer_groups = []
            if request.include_peers:
                peer_groups = self._identify_peer_groups(request.countries)
            
            # Generate summary
            summary = self._generate_comparison_summary(rankings, anomalies, peer_groups)
            
            return CountryComparison(
                countries=request.countries,
                metrics=metrics,
                year=request.year,
                rankings=rankings,
                anomalies=anomalies,
                peer_groups=peer_groups,
                summary=summary
            )
            
        except Exception as e:
            logger.error("Error in country comparison", error=str(e), countries=request.countries)
            raise
    
    def detect_anomalies(self, request: AnomalyDetectionRequest) -> AnomalyDetectionResponse:
        """Detect anomalies in health data"""
        logger.info("Starting anomaly detection", country=request.country, metric=request.metric)
        
        try:
            anomalies = []
            total_analyzed = 0
            
            # Get available countries and metrics
            countries = [request.country] if request.country else self.data_processor.get_available_countries()
            metrics = [request.metric] if request.metric else list(MetricType)
            
            for country in countries:
                for metric in metrics:
                    # Get historical data for trend analysis
                    historical_data = self._get_historical_data(country, metric, request.timeframe)
                    if not historical_data:
                        continue
                    
                    total_analyzed += len(historical_data)
                    
                    # Detect anomalies using statistical methods
                    country_anomalies = self._detect_metric_anomalies(
                        country, metric, historical_data, request.sensitivity
                    )
                    anomalies.extend(country_anomalies)
            
            # Calculate overall confidence
            detection_confidence = self._calculate_detection_confidence(anomalies, total_analyzed)
            
            return AnomalyDetectionResponse(
                anomalies=anomalies,
                total_analyzed=total_analyzed,
                detection_confidence=detection_confidence,
                parameters=request
            )
            
        except Exception as e:
            logger.error("Error in anomaly detection", error=str(e))
            raise
    
    def find_peer_groups(self, request: PeerGroupRequest) -> PeerGroupResponse:
        """Find peer groups for a target country"""
        logger.info("Finding peer groups", country=request.country, criteria=request.criteria)
        
        try:
            # Get all available countries
            all_countries = self.data_processor.get_available_countries()
            
            # Calculate similarity scores
            similarity_scores = self._calculate_similarity_scores(
                request.country, all_countries, request.criteria
            )
            
            # Filter by similarity threshold
            qualified_peers = {
                country: score for country, score in similarity_scores.items()
                if score >= request.similarity_threshold and country != request.country
            }
            
            # Sort by similarity and limit to max_peers
            sorted_peers = sorted(qualified_peers.items(), key=lambda x: x[1], reverse=True)
            top_peers = [country for country, _ in sorted_peers[:request.max_peers]]
            
            # Create peer groups
            peer_groups = []
            if top_peers:
                # Create main peer group
                main_group = self._create_peer_group(
                    f"Similar to {request.country}",
                    [request.country] + top_peers,
                    request.criteria
                )
                peer_groups.append(main_group)
                
                # Create additional groups based on criteria
                additional_groups = self._create_criteria_groups(
                    request.country, top_peers, request.criteria
                )
                peer_groups.extend(additional_groups)
            
            # Find best match
            best_match = peer_groups[0] if peer_groups else None
            
            return PeerGroupResponse(
                target_country=request.country,
                peer_groups=peer_groups,
                best_match=best_match,
                similarity_scores=similarity_scores
            )
            
        except Exception as e:
            logger.error("Error finding peer groups", error=str(e), country=request.country)
            raise
    
    def _calculate_rankings(self, country_data: Dict, metrics: List[MetricType], year: int) -> List[CountryRanking]:
        """Calculate rankings for countries across metrics"""
        rankings = []
        
        # Extract metric values for ranking
        metric_values = {}
        for metric in metrics:
            metric_values[metric] = []
            for country, data in country_data.items():
                value = self._get_metric_value(data, metric)
                if value is not None:
                    metric_values[metric].append((country, value))
        
        # Calculate percentiles and ranks
        country_metrics = {}
        for country in country_data.keys():
            country_metrics[country] = []
        
        for metric, values in metric_values.items():
            if not values:
                continue
                
            # Sort by value (higher is better for most health metrics)
            sorted_values = sorted(values, key=lambda x: x[1], reverse=True)
            
            for rank, (country, value) in enumerate(sorted_values, 1):
                percentile = (len(sorted_values) - rank + 1) / len(sorted_values) * 100
                
                health_metric = HealthMetric(
                    name=metric.value,
                    value=value,
                    unit=self._get_metric_unit(metric),
                    rank=rank,
                    percentile=percentile,
                    trend=self._calculate_trend(country, metric),
                    anomaly=False,  # Will be updated by anomaly detection
                    baseline_year=year
                )
                country_metrics[country].append(health_metric)
        
        # Calculate overall rankings
        for country, metrics_list in country_metrics.items():
            if not metrics_list:
                continue
                
            # Calculate weighted score
            total_score = 0
            total_weight = 0
            
            for metric in metrics_list:
                weight = self.metric_weights.get(MetricType(metric.name), 0.25)
                # Normalize percentile to 0-1 scale
                normalized_score = metric.percentile / 100
                total_score += normalized_score * weight
                total_weight += weight
            
            overall_score = total_score / total_weight if total_weight > 0 else 0
            
            ranking = CountryRanking(
                country_code=country,
                country_name=self._get_country_name(country),
                overall_rank=0,  # Will be calculated after all countries
                metrics=metrics_list,
                total_score=overall_score
            )
            rankings.append(ranking)
        
        # Calculate overall ranks
        rankings.sort(key=lambda x: x.total_score, reverse=True)
        for rank, ranking in enumerate(rankings, 1):
            ranking.overall_rank = rank
        
        return rankings
    
    def _detect_anomalies(self, country_data: Dict, metrics: List[MetricType]) -> List[AnomalyAlert]:
        """Detect anomalies in country data"""
        anomalies = []
        
        for country, data in country_data.items():
            for metric in metrics:
                value = self._get_metric_value(data, metric)
                if value is None:
                    continue
                
                # Get historical data for comparison
                historical_values = self._get_historical_values(country, metric, 5)
                if len(historical_values) < 3:
                    continue
                
                # Calculate z-score
                mean_val = np.mean(historical_values)
                std_val = np.std(historical_values)
                
                if std_val == 0:
                    continue
                
                z_score = abs(value - mean_val) / std_val
                
                # Determine severity
                if z_score > 3:
                    severity = AnomalySeverity.HIGH
                elif z_score > 2:
                    severity = AnomalySeverity.MEDIUM
                elif z_score > 1.5:
                    severity = AnomalySeverity.LOW
                else:
                    continue
                
                # Create anomaly alert
                anomaly = AnomalyAlert(
                    country=country,
                    metric=metric.value,
                    severity=severity,
                    description=f"{metric.value} is {z_score:.1f} standard deviations from historical average",
                    confidence=min(z_score / 3, 1.0),
                    recommendation=self._get_anomaly_recommendation(metric, severity, value, mean_val)
                )
                anomalies.append(anomaly)
        
        return anomalies
    
    def _identify_peer_groups(self, countries: List[str]) -> List[PeerGroup]:
        """Identify peer groups for countries"""
        peer_groups = []
        
        # Create regional groups
        regional_groups = {
            "Southern Europe": ["PRT", "ESP", "GRC"],
            "Northern Europe": ["SWE"],
            "All Countries": countries
        }
        
        for group_name, group_countries in regional_groups.items():
            if any(country in group_countries for country in countries):
                # Calculate group averages
                group_data = []
                for country in group_countries:
                    data = self.data_processor.get_country_data(country, 2022)
                    if data:
                        group_data.append(data)
                
                if group_data:
                    averages = self._calculate_group_averages(group_data)
                    peer_group = PeerGroup(
                        name=group_name,
                        countries=group_countries,
                        criteria=["region"],
                        average=averages,
                        size=len(group_countries)
                    )
                    peer_groups.append(peer_group)
        
        return peer_groups
    
    def _generate_comparison_summary(self, rankings: List[CountryRanking], 
                                   anomalies: List[AnomalyAlert], 
                                   peer_groups: List[PeerGroup]) -> Dict[str, Any]:
        """Generate summary of comparison results"""
        summary = {
            "total_countries": len(rankings),
            "total_anomalies": len(anomalies),
            "high_severity_anomalies": len([a for a in anomalies if a.severity == AnomalySeverity.HIGH]),
            "peer_groups": len(peer_groups),
            "best_performer": rankings[0].country_name if rankings else None,
            "worst_performer": rankings[-1].country_name if rankings else None,
            "average_score": np.mean([r.total_score for r in rankings]) if rankings else 0,
            "score_range": {
                "min": min([r.total_score for r in rankings]) if rankings else 0,
                "max": max([r.total_score for r in rankings]) if rankings else 0
            }
        }
        
        return summary
    
    def _get_metric_value(self, data: Dict, metric: MetricType) -> Optional[float]:
        """Extract metric value from country data"""
        metric_mapping = {
            MetricType.LIFE_EXPECTANCY: "life_expectancy",
            MetricType.DOCTOR_DENSITY: "doctor_density",
            MetricType.NURSE_DENSITY: "nurse_density",
            MetricType.HEALTH_SPENDING: "government_spending"
        }
        
        key = metric_mapping.get(metric)
        return data.get(key) if key else None
    
    def _get_metric_unit(self, metric: MetricType) -> str:
        """Get unit for metric"""
        units = {
            MetricType.LIFE_EXPECTANCY: "years",
            MetricType.DOCTOR_DENSITY: "per 1,000 population",
            MetricType.NURSE_DENSITY: "per 1,000 population",
            MetricType.HEALTH_SPENDING: "% of GDP"
        }
        return units.get(metric, "")
    
    def _calculate_trend(self, country: str, metric: MetricType) -> TrendDirection:
        """Calculate trend direction for metric"""
        # Simplified trend calculation - in real implementation, would use historical data
        return TrendDirection.STABLE
    
    def _get_country_name(self, country_code: str) -> str:
        """Get country name from code"""
        names = {
            "PRT": "Portugal",
            "ESP": "Spain", 
            "SWE": "Sweden",
            "GRC": "Greece"
        }
        return names.get(country_code, country_code)
    
    def _get_historical_data(self, country: str, metric: MetricType, years: int) -> List[float]:
        """Get historical data for trend analysis"""
        # Simplified - in real implementation, would query historical data
        return []
    
    def _detect_metric_anomalies(self, country: str, metric: MetricType, 
                                historical_data: List[float], sensitivity: float) -> List[AnomalyAlert]:
        """Detect anomalies for specific metric"""
        # Simplified anomaly detection
        return []
    
    def _calculate_detection_confidence(self, anomalies: List[AnomalyAlert], total_analyzed: int) -> float:
        """Calculate overall detection confidence"""
        if total_analyzed == 0:
            return 0.0
        
        # Simple confidence calculation based on data coverage
        coverage = min(total_analyzed / 100, 1.0)  # Assume 100 is good coverage
        return coverage
    
    def _calculate_similarity_scores(self, target_country: str, all_countries: List[str], 
                                   criteria: List[str]) -> Dict[str, float]:
        """Calculate similarity scores between countries"""
        scores = {}
        
        # Get target country data
        target_data = self.data_processor.get_country_data(target_country, 2022)
        if not target_data:
            return scores
        
        for country in all_countries:
            if country == target_country:
                continue
                
            country_data = self.data_processor.get_country_data(country, 2022)
            if not country_data:
                continue
            
            # Calculate similarity based on criteria
            similarity = self._calculate_country_similarity(target_data, country_data, criteria)
            scores[country] = similarity
        
        return scores
    
    def _calculate_country_similarity(self, data1: Dict, data2: Dict, criteria: List[str]) -> float:
        """Calculate similarity between two countries"""
        # Simplified similarity calculation
        # In real implementation, would use proper distance metrics
        
        similarities = []
        
        # Compare life expectancy (normalized)
        le1, le2 = data1.get("life_expectancy", 0), data2.get("life_expectancy", 0)
        if le1 > 0 and le2 > 0:
            le_sim = 1 - abs(le1 - le2) / max(le1, le2)
            similarities.append(le_sim)
        
        # Compare spending (normalized)
        sp1, sp2 = data1.get("government_spending", 0), data2.get("government_spending", 0)
        if sp1 > 0 and sp2 > 0:
            sp_sim = 1 - abs(sp1 - sp2) / max(sp1, sp2)
            similarities.append(sp_sim)
        
        return np.mean(similarities) if similarities else 0.0
    
    def _create_peer_group(self, name: str, countries: List[str], criteria: List[str]) -> PeerGroup:
        """Create a peer group"""
        # Calculate group averages
        group_data = []
        for country in countries:
            data = self.data_processor.get_country_data(country, 2022)
            if data:
                group_data.append(data)
        
        averages = self._calculate_group_averages(group_data) if group_data else {}
        
        return PeerGroup(
            name=name,
            countries=countries,
            criteria=criteria,
            average=averages,
            size=len(countries)
        )
    
    def _create_criteria_groups(self, target_country: str, peers: List[str], 
                               criteria: List[str]) -> List[PeerGroup]:
        """Create additional peer groups based on criteria"""
        # Simplified - in real implementation, would create more sophisticated groups
        return []
    
    def _calculate_group_averages(self, group_data: List[Dict]) -> Dict[str, float]:
        """Calculate average values for a group of countries"""
        if not group_data:
            return {}
        
        averages = {}
        metrics = ["life_expectancy", "doctor_density", "nurse_density", "government_spending"]
        
        for metric in metrics:
            values = [data.get(metric, 0) for data in group_data if data.get(metric) is not None]
            if values:
                averages[metric] = np.mean(values)
        
        return averages
    
    def _get_historical_values(self, country: str, metric: MetricType, years: int) -> List[float]:
        """Get historical values for a country and metric"""
        # Simplified - in real implementation, would query historical data
        return []
    
    def _get_anomaly_recommendation(self, metric: MetricType, severity: AnomalySeverity, 
                                  current_value: float, historical_avg: float) -> str:
        """Generate recommendation for anomaly"""
        if current_value > historical_avg:
            direction = "higher than"
            action = "investigate the improvement"
        else:
            direction = "lower than"
            action = "address the decline"
        
        return f"Current {metric.value} is {direction} historical average. Consider {action}."
