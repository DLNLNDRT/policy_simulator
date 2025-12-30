/**
 * Data Quality Assurance TypeScript types
 */

export enum QualityAlertType {
  COMPLETENESS = 'completeness',
  VALIDITY = 'validity',
  CONSISTENCY = 'consistency',
  FRESHNESS = 'freshness'
}

export enum QualityAlertSeverity {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  CRITICAL = 'critical'
}

export enum ValidationStatus {
  PASS = 'pass',
  WARNING = 'warning',
  FAIL = 'fail'
}

export enum ProcessingStepType {
  DATA_INGESTION = 'data_ingestion',
  DATA_CLEANING = 'data_cleaning',
  DATA_TRANSFORMATION = 'data_transformation',
  DATA_VALIDATION = 'data_validation',
  DATA_AGGREGATION = 'data_aggregation',
  MODEL_TRAINING = 'model_training',
  SIMULATION_EXECUTION = 'simulation_execution'
}

export enum DataSourceType {
  WHO_GLOBAL_HEALTH = 'who_global_health',
  INTERNAL_PROCESSING = 'internal_processing'
}

export interface QualityAlert {
  id: string
  type: QualityAlertType
  severity: QualityAlertSeverity
  message: string
  affected_indicators: string[]
  affected_countries?: string[]
  created_at: string
  resolved: boolean
  resolved_at?: string
  recommendations: string[]
}

export interface QualityMetrics {
  overall_score: number
  completeness_score: number
  validity_score: number
  consistency_score: number
  freshness_score: number
  last_updated: string
  trend: 'up' | 'down' | 'stable'
  alerts: QualityAlert[]
}

export interface QualityBreakdown {
  by_indicator: Record<string, number>
  by_country: Record<string, number>
  by_source: Record<string, number>
  by_time_period: Record<string, number>
}

export interface ValidationCheck {
  status: ValidationStatus
  score: number
  details: string
  recommendations: string[]
}

export interface ValidationIssue {
  type: string
  severity: QualityAlertSeverity
  description: string
  affected_records: string[]
  recommendation: string
}

export interface ValidationResult {
  dataset_id: string
  validation_timestamp: string
  overall_status: ValidationStatus
  completeness_check: ValidationCheck
  validity_check: ValidationCheck
  consistency_check: ValidationCheck
  outlier_check: ValidationCheck
  issues: ValidationIssue[]
  quality_score: number
  validation_duration_ms: number
}

export interface DataSource {
  source_id: string
  name: string
  url: string
  description: string
  quality_score: number
  coverage: string
  last_updated: string
  version?: string
}

export interface ProcessingStep {
  step_id: string
  type: ProcessingStepType
  description: string
  timestamp: string
  input_data: string
  output_data: string
  parameters: Record<string, any>
  duration_ms: number
  success: boolean
  error_message?: string
}

export interface DataTransformation {
  transformation_id: string
  name: string
  description: string
  input_schema: Record<string, any>
  output_schema: Record<string, any>
  transformation_logic: string
  timestamp: string
  parameters: Record<string, any>
}

export interface DatasetVersion {
  version_id: string
  dataset_id: string
  version_number: string
  created_at: string
  created_by: string
  changes: string[]
  data_hash: string
  size_bytes: number
  record_count: number
}

export interface AuditEntry {
  entry_id: string
  timestamp: string
  action: string
  user_id?: string
  resource_type: string
  resource_id: string
  details: Record<string, any>
  ip_address?: string
}

export interface ProvenanceData {
  dataset_id: string
  original_sources: DataSource[]
  processing_steps: ProcessingStep[]
  transformations: DataTransformation[]
  version_history: DatasetVersion[]
  audit_trail: AuditEntry[]
  created_at: string
  last_updated: string
}

export interface QualityOverview {
  overall_score: number
  completeness_score: number
  validity_score: number
  consistency_score: number
  freshness_score: number
  last_updated: string
  trend: 'up' | 'down' | 'stable'
  alerts: QualityAlert[]
  data_sources: Record<string, Record<string, any>>
}

export interface QualityTrend {
  timestamp: string
  overall_score: number
  completeness_score: number
  validity_score: number
  consistency_score: number
  freshness_score: number
  alert_count: number
}

export interface IndicatorQuality {
  indicator_id: string
  overall_score: number
  completeness_score: number
  validity_score: number
  consistency_score: number
  freshness_score: number
  last_updated: string
  trend: 'up' | 'down' | 'stable'
  coverage: Record<string, any>
  issues: ValidationIssue[]
  recommendations: string[]
}

export interface CountryQuality {
  country_code: string
  country_name: string
  overall_score: number
  completeness_score: number
  validity_score: number
  consistency_score: number
  freshness_score: number
  last_updated: string
  trend: 'up' | 'down' | 'stable'
  indicators: Record<string, Record<string, any>>
  alerts: QualityAlert[]
  data_sources: DataSource[]
}

export interface ValidationRequest {
  dataset_id: string
  validation_type: string
  parameters: Record<string, any>
}

export interface AlertResolutionRequest {
  resolution_notes: string
}

export interface AlertResolutionResponse {
  alert_id: string
  resolved: boolean
  resolved_at: string
  resolution_notes: string
  resolved_by: string
  status: string
}

export interface ProvenanceExportRequest {
  format: 'json' | 'csv'
}

export interface ProvenanceExportResponse {
  dataset_id: string
  format: string
  exported_data: string
  export_timestamp: string
  size_bytes: number
}

export interface DataSourcesResponse {
  summary: Record<string, any>
  sources: DataSource[]
}

export interface QualityTrendsResponse {
  trends: QualityTrend[]
  period_days: number
  generated_at: string
}

// API Response types
export interface QualityOverviewResponse extends QualityOverview {}

export interface QualityTrendsResponseData extends QualityTrendsResponse {}

export interface IndicatorQualityResponse extends IndicatorQuality {}

export interface CountryQualityResponse extends CountryQuality {}

export interface ValidationResultResponse extends ValidationResult {}

export interface ProvenanceDataResponse extends ProvenanceData {}

export interface DataSourcesResponseData extends DataSourcesResponse {}

export interface QualityAlertsResponse {
  alerts: QualityAlert[]
  total_count: number
  unresolved_count: number
}

// Component Props types
export interface QualityDashboardProps {
  onRefresh?: () => void
  onExport?: () => void
}

export interface QualityScoreCardProps {
  title: string
  score: number
  icon: React.ReactElement
  color: 'green' | 'blue' | 'purple' | 'orange' | 'red'
  trend?: 'up' | 'down' | 'stable'
  subtitle?: string
}

export interface QualityAlertsProps {
  alerts: QualityAlert[]
  onResolveAlert?: (alertId: string) => void
  onDismissAlert?: (alertId: string) => void
}

export interface QualityTrendsProps {
  days?: number
}

export interface DataSourcesProps {
  sources?: Record<string, any>
  onViewProvenance?: (sourceId: string) => void
  onExportProvenance?: (sourceId: string) => void
}

export interface ProvenanceViewerProps {
  datasetId: string
  provenanceData: ProvenanceData
  onExport: () => void
}

export interface ValidationStatusProps {
  validationResults: ValidationResult[]
  onViewDetails: (result: ValidationResult) => void
}
