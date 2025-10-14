/**
 * TypeScript types for Advanced Analytics & Reporting features
 */

// Enums
export enum TrendDirection {
  INCREASING = 'increasing',
  DECREASING = 'decreasing',
  STABLE = 'stable'
}

export enum ChartType {
  LINE = 'line',
  BAR = 'bar',
  SCATTER = 'scatter',
  HEATMAP = 'heatmap',
  BOX = 'box',
  HISTOGRAM = 'histogram',
  PIE = 'pie',
  AREA = 'area',
  RADAR = 'radar',
  BUBBLE = 'bubble'
}

export enum ReportTemplate {
  EXECUTIVE_SUMMARY = 'executive_summary',
  DETAILED_ANALYSIS = 'detailed_analysis',
  POLICY_BRIEF = 'policy_brief',
  RESEARCH_REPORT = 'research_report'
}

export enum ExportFormat {
  PDF = 'pdf',
  DOCX = 'docx',
  PPTX = 'pptx',
  PNG = 'png',
  SVG = 'svg',
  HTML = 'html'
}

// Base Types
export interface TimePeriod {
  start: number
  end: number
}

export interface ConfidenceInterval {
  lower: number
  upper: number
}

export interface DataPoint {
  year: number
  value: number
}

// Trend Analysis Types
export interface TrendAnalysisRequest {
  indicator: string
  country: string
  time_period?: TimePeriod
}

export interface TrendAnalysisResponse {
  indicator: string
  country: string
  time_period: TimePeriod
  trend_direction: TrendDirection
  trend_strength: number
  annual_change: number
  total_change: number
  change_percentage: number
  statistical_significance: number
  confidence_interval: ConfidenceInterval
  r_squared: number
  sample_size: number
  data_points: DataPoint[]
  response_time_ms: number
  generated_at: number
}

// Correlation Analysis Types
export interface CorrelationAnalysisRequest {
  indicators: string[]
  countries?: string[]
  time_period?: TimePeriod
}

export interface CorrelationAnalysisResponse {
  indicators: string[]
  countries?: string[]
  time_period?: TimePeriod
  correlation_matrix: number[][]
  significance_matrix: number[][]
  interpretation: string
  sample_size: number
  response_time_ms: number
  generated_at: string
}

// Forecast Types
export interface ForecastRequest {
  indicator: string
  country: string
  forecast_years: number
  confidence_level: number
}

export interface ModelPerformance {
  r_squared: number
  rmse: number
  trend_slope: number
  intercept: number
}

export interface ForecastDataPoint {
  year: number
  predicted_value: number
  confidence_interval: ConfidenceInterval
}

export interface ForecastResponse {
  indicator: string
  country: string
  forecast_years: number
  confidence_level: number
  model_performance: ModelPerformance
  historical_data: DataPoint[]
  forecast_data: ForecastDataPoint[]
  response_time_ms: number
  generated_at: string
}

// Statistical Test Types
export interface StatisticalTestRequest {
  indicator: string
  country1: string
  country2: string
  time_period?: TimePeriod
}

export interface TestResults {
  t_statistic: number
  p_value: number
  significance_level: string
  cohens_d: number
  effect_size_interpretation: string
}

export interface DescriptiveStatistics {
  mean: number
  std: number
  n: number
}

export interface CountryStatistics {
  country1: DescriptiveStatistics
  country2: DescriptiveStatistics
}

export interface StatisticalTestResponse {
  indicator: string
  country1: string
  country2: string
  time_period?: TimePeriod
  test_results: TestResults
  descriptive_statistics: CountryStatistics
  interpretation: string
  response_time_ms: number
  generated_at: string
}

// Regression Analysis Types
export interface RegressionAnalysisRequest {
  target_indicator: string
  predictor_indicators: string[]
  countries?: string[]
  time_period?: TimePeriod
}

export interface RegressionModelPerformance {
  r_squared: number
  adjusted_r_squared: number
  mse: number
  rmse: number
  intercept: number
}

export interface CoefficientSignificance {
  coefficient: number
  std_error?: number
  t_statistic?: number
  p_value?: number
  significant: boolean
}

export interface RegressionAnalysisResponse {
  target_indicator: string
  predictor_indicators: string[]
  countries?: string[]
  time_period?: TimePeriod
  model_performance: RegressionModelPerformance
  feature_importance: Record<string, number>
  coefficient_significance: Record<string, CoefficientSignificance>
  sample_size: number
  degrees_of_freedom: number
  interpretation: string
  response_time_ms: number
  generated_at: string
}

// Report Generation Types
export interface ReportGenerationRequest {
  template: ReportTemplate
  title: string
  simulation_data?: Record<string, any>
  analytics_data?: Record<string, any>
  data_sources?: string[]
  config: Record<string, any>
}

export interface ReportMetadata {
  generated_at: string
  template: string
  sections_count: number
}

export interface ReportGenerationResponse {
  report_id: string
  title: string
  format: string
  content: string
  metadata: ReportMetadata
  response_time_ms: number
  generated_at: number
}

// Visualization Types
export interface VisualizationRequest {
  chart_type: ChartType
  title: string
  data: Record<string, any>
  config: Record<string, any>
  chart_spec?: Record<string, any>
}

export interface VisualizationResponse {
  chart_id: string
  chart_type: ChartType
  data: Record<string, any>
  config: Record<string, any>
  analysis: Record<string, any>
  metadata: Record<string, any>
  response_time_ms: number
  generated_at: number
}

// Dashboard Types
export interface DashboardComponent {
  type: string
  title: string
  data_source: string
  position: Record<string, number>
  size: Record<string, number>
  styling: Record<string, any>
  filters: string[]
}

export interface DashboardRequest {
  title: string
  components: DashboardComponent[]
  dashboard_config: Record<string, any>
  data_sources: Record<string, any>
}

export interface DashboardResponse {
  dashboard_id: string
  dashboard: Record<string, any>
  export_options: Record<string, any>
  metadata: Record<string, any>
  response_time_ms: number
  generated_at: number
}

// Analytics Data Types
export interface AnalyticsData {
  dashboard_id: string
  title: string
  layout: string
  components: DashboardComponentData[]
  filters: AnalyticsFilter[]
  refresh_interval: number
  metadata: {
    created_at: string
    version: string
  }
}

export interface DashboardComponentData {
  component_id: string
  type: string
  title: string
  data_source: string
  data: Record<string, any>
  position: Record<string, number>
  size: Record<string, number>
  styling: Record<string, any>
  filters: string[]
}

export interface AnalyticsFilter {
  type: string
  name: string
  options: string[]
  value: any
}

// Dashboard Configuration Types
export interface DashboardConfig {
  layout: 'grid' | 'list' | 'custom'
  refreshInterval: number
  showMetrics: boolean
  showCharts: boolean
  showReports: boolean
}

// Chart Data Types
export interface ChartData {
  labels: string[]
  datasets: ChartDataset[]
  metadata?: Record<string, any>
}

export interface ChartDataset {
  label: string
  data: number[]
  backgroundColor?: string | string[]
  borderColor?: string | string[]
  borderWidth?: number
  fill?: boolean
}

export interface ChartOptions {
  responsive: boolean
  maintainAspectRatio: boolean
  plugins: Record<string, any>
  scales?: Record<string, any>
  animation?: Record<string, any>
}

// Heatmap Types
export interface HeatmapData {
  type: 'heatmap'
  title: string
  x_axis: {
    title: string
    categories: string[]
  }
  y_axis: {
    title: string
    categories: string[]
  }
  data: number[][]
  color_scale: string
  show_values: boolean
  annotations: HeatmapAnnotation[]
}

export interface HeatmapAnnotation {
  row: number
  col: number
  text: string
  color: string
}

// Scatter Plot Types
export interface ScatterPlotData {
  type: 'scatter'
  title: string
  x_axis: {
    title: string
    values: number[]
  }
  y_axis: {
    title: string
    values: number[]
  }
  labels: string[]
  correlation: {
    value: number
    strength: string
    direction: string
  }
  trend_line: {
    slope: number
    intercept: number
    points: Array<{ x: number; y: number }>
  }
}

// Report Section Types
export interface ReportSection {
  id: string
  title: string
  type: 'text' | 'chart' | 'table' | 'analysis'
  content: any
  enabled: boolean
}

export interface ReportTemplateConfig {
  id: string
  name: string
  description: string
  sections: string[]
}

// Analytics Summary Types
export interface AnalyticsSummary {
  total_analyses: number
  trend_analyses: number
  correlation_analyses: number
  forecasts: number
  statistical_tests: number
  regression_analyses: number
  reports_generated: number
  visualizations_created: number
  dashboards_built: number
  avg_response_time_ms: number
  last_updated: string
}

export interface AnalyticsHealth {
  status: string
  uptime_percentage: number
  error_rate: number
  active_connections: number
  memory_usage: number
  cpu_usage: number
  last_health_check: string
}

// API Response Types
export interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
  message?: string
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

// Filter Types
export interface AnalyticsFilters {
  countries: string[]
  indicators: string[]
  timePeriod: TimePeriod
}

// Export Types
export interface ExportOptions {
  formats: ExportFormat[]
  include_data: boolean
  filename?: string
  quality?: number
}

export interface ExportResult {
  success: boolean
  filename: string
  format: string
  size_bytes: number
  download_url: string
  generated_at: string
}

// Component Props Types
export interface AnalyticsDashboardProps {
  initialData?: AnalyticsData
  onDataUpdate?: (data: AnalyticsData) => void
  onExport?: (format: string) => void
}

export interface TrendAnalysisCardProps {
  data?: TrendAnalysisResponse
  onAnalyze?: (config: TrendAnalysisRequest) => void
}

export interface CorrelationMatrixProps {
  data?: CorrelationAnalysisResponse
  onAnalyze?: (config: CorrelationAnalysisRequest) => void
}

export interface ForecastChartProps {
  data?: ForecastResponse
  onForecast?: (config: ForecastRequest) => void
}

export interface StatisticalTestPanelProps {
  data?: StatisticalTestResponse
  onTest?: (config: StatisticalTestRequest) => void
}

export interface ReportBuilderProps {
  onGenerate?: (config: ReportGenerationRequest) => void
}

export interface AdvancedChartsProps {
  onCreate?: (config: VisualizationRequest) => void
}

export interface ComparisonToolsProps {
  onCompare?: (config: any) => void
}
