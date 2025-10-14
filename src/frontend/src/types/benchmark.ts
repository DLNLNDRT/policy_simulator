/**
 * TypeScript types for the Health Benchmark Dashboard feature
 */

export enum MetricType {
  LIFE_EXPECTANCY = 'life_expectancy',
  DOCTOR_DENSITY = 'doctor_density',
  NURSE_DENSITY = 'nurse_density',
  HEALTH_SPENDING = 'health_spending'
}

export enum TrendDirection {
  UP = 'up',
  DOWN = 'down',
  STABLE = 'stable'
}

export enum AnomalySeverity {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high'
}

export interface HealthMetric {
  name: string
  value: number
  unit: string
  rank: number
  percentile: number
  trend: TrendDirection
  anomaly: boolean
  baseline_year: number
}

export interface CountryRanking {
  country_code: string
  country_name: string
  overall_rank: number
  metrics: HealthMetric[]
  total_score: number
}

export interface AnomalyAlert {
  country: string
  metric: string
  severity: AnomalySeverity
  description: string
  confidence: number
  recommendation: string
  detected_at: string
}

export interface PeerGroup {
  name: string
  countries: string[]
  criteria: string[]
  average: Record<string, number>
  size: number
}

export interface ComparisonRequest {
  countries: string[]
  metrics?: MetricType[]
  year?: number
  include_anomalies?: boolean
  include_peers?: boolean
}

export interface CountryComparison {
  countries: string[]
  metrics: MetricType[]
  year: number
  rankings: CountryRanking[]
  anomalies: AnomalyAlert[]
  peer_groups: PeerGroup[]
  summary: ComparisonSummary
  generated_at: string
}

export interface ComparisonSummary {
  total_countries: number
  total_anomalies: number
  high_severity_anomalies: number
  peer_groups: number
  best_performer: string | null
  worst_performer: string | null
  average_score: number
  score_range: {
    min: number
    max: number
  }
}

export interface AnomalyDetectionRequest {
  country?: string
  metric?: MetricType
  timeframe?: number
  sensitivity?: number
}

export interface AnomalyDetectionResponse {
  anomalies: AnomalyAlert[]
  total_analyzed: number
  detection_confidence: number
  parameters: AnomalyDetectionRequest
  generated_at: string
}

export interface PeerGroupRequest {
  country: string
  criteria: string[]
  max_peers?: number
  similarity_threshold?: number
}

export interface PeerGroupResponse {
  target_country: string
  peer_groups: PeerGroup[]
  best_match: PeerGroup | null
  similarity_scores: Record<string, number>
  generated_at: string
}

export interface BenchmarkStats {
  total_countries: number
  total_metrics: number
  last_updated: string
  anomaly_alerts: number
  peer_groups: number
  data_quality_score: number
}

export interface ExportRequest {
  format: 'json' | 'csv' | 'pdf'
  countries: string[]
  metrics: MetricType[]
  include_charts?: boolean
  include_anomalies?: boolean
}

export interface ExportResponse {
  download_url: string
  file_size: number
  expires_at: string
  format: string
  generated_at: string
}

export interface Country {
  code: string
  name: string
}

export interface Metric {
  code: string
  name: string
  unit: string
  description: string
}

// Chart data interfaces
export interface ChartDataPoint {
  country: string
  value: number
  rank?: number
  percentile?: number
}

export interface BarChartData {
  country: string
  [key: string]: string | number
}

export interface ScatterDataPoint {
  country: string
  metric: string
  value: number
  rank: number
  percentile: number
}

export interface RankingDataPoint {
  country: string
  overall_rank: number
  total_score: number
}

// UI State interfaces
export interface BenchmarkFilters {
  countries: string[]
  metrics: MetricType[]
  year: number
  showAnomalies: boolean
  showPeers: boolean
  viewMode: 'table' | 'charts'
}

export interface BenchmarkState {
  isLoading: boolean
  error: string | null
  comparison: CountryComparison | null
  filters: BenchmarkFilters
  availableCountries: Country[]
  availableMetrics: Metric[]
}
