/**
 * TypeScript types for the Narrative Insight Generator feature
 */

export enum NarrativeType {
  SIMULATION_IMPACT = 'simulation_impact',
  BENCHMARK_COMPARISON = 'benchmark_comparison',
  ANOMALY_ALERT = 'anomaly_alert',
  TREND_ANALYSIS = 'trend_analysis',
  EXECUTIVE_SUMMARY = 'executive_summary'
}

export enum AudienceType {
  MINISTERS = 'ministers',
  NGOS = 'ngos',
  RESEARCHERS = 'researchers',
  PUBLIC = 'public',
  POLICY_MAKERS = 'policy_makers'
}

export enum ToneType {
  FORMAL = 'formal',
  CONVERSATIONAL = 'conversational',
  TECHNICAL = 'technical',
  PERSUASIVE = 'persuasive'
}

export enum LengthType {
  BRIEF = 'brief',
  STANDARD = 'standard',
  DETAILED = 'detailed'
}

export enum FocusArea {
  ECONOMIC_IMPACT = 'economic_impact',
  HEALTH_OUTCOMES = 'health_outcomes',
  IMPLEMENTATION = 'implementation',
  POLICY_RECOMMENDATIONS = 'policy_recommendations',
  RISK_ASSESSMENT = 'risk_assessment'
}

export interface NarrativeRequest {
  narrative_type: NarrativeType
  data_source: Record<string, any>
  audience: AudienceType
  tone: ToneType
  length: LengthType
  focus_areas: FocusArea[]
  custom_instructions?: string
  include_citations: boolean
  include_recommendations: boolean
}

export interface NarrativeSection {
  title: string
  content: string
  order: number
  word_count: number
  key_points: string[]
}

export interface Citation {
  source: string
  url?: string
  date?: string
  type: string
  relevance: string
}

export interface Recommendation {
  title: string
  description: string
  priority: 'low' | 'medium' | 'high'
  timeline?: string
  resources_needed?: string
  expected_impact?: string
}

export interface QualityMetrics {
  coherence_score: number
  accuracy_score: number
  actionability_score: number
  readability_score: number
  overall_score: number
  word_count: number
  reading_time_minutes: number
}

export interface NarrativeResponse {
  narrative_id: string
  title: string
  narrative_type: NarrativeType
  sections: NarrativeSection[]
  executive_summary: string
  key_insights: string[]
  recommendations: Recommendation[]
  citations: Citation[]
  quality_metrics: QualityMetrics
  metadata: Record<string, any>
  generated_at: string
  cost_usd: number
  generation_time_ms: number
}

export interface TemplateInfo {
  template_id: string
  name: string
  description: string
  narrative_type: NarrativeType
  audience: AudienceType
  tone: ToneType
  length: LengthType
  focus_areas: FocusArea[]
  sections: string[]
  word_count_range: {
    min: number
    max: number
  }
}

export interface NarrativeHistory {
  narrative_id: string
  title: string
  narrative_type: NarrativeType
  audience: AudienceType
  quality_score: number
  word_count: number
  cost_usd: number
  generated_at: string
  user_feedback?: Record<string, any>
}

export interface NarrativeStats {
  total_narratives: number
  narratives_by_type: Record<string, number>
  narratives_by_audience: Record<string, number>
  average_quality_score: number
  average_cost_usd: number
  total_cost_usd: number
  most_used_template?: string
  last_24h_narratives: number
}

export interface ExportRequest {
  narrative_id: string
  format: 'pdf' | 'docx' | 'html' | 'markdown'
  include_citations: boolean
  include_recommendations: boolean
  include_quality_metrics: boolean
}

export interface ExportResponse {
  download_url: string
  file_size: number
  format: string
  expires_at: string
  generated_at: string
}

export interface FeedbackRequest {
  narrative_id: string
  overall_rating: number
  coherence_rating: number
  accuracy_rating: number
  actionability_rating: number
  comments?: string
  suggestions?: string
}

export interface FeedbackResponse {
  feedback_id: string
  narrative_id: string
  overall_rating: number
  submitted_at: string
  thank_you_message: string
}

// UI State interfaces
export interface NarrativeBuilderState {
  request: NarrativeRequest
  response: NarrativeResponse | null
  isGenerating: boolean
  error: string | null
  activeTab: 'builder' | 'preview' | 'metrics'
}

export interface NarrativeOptions {
  narrative_types: Array<{
    value: string
    label: string
  }>
  audiences: Array<{
    value: string
    label: string
  }>
  tones: Array<{
    value: string
    label: string
  }>
  lengths: Array<{
    value: string
    label: string
  }>
  focus_areas: Array<{
    value: string
    label: string
  }>
}

// Chart data interfaces for quality metrics visualization
export interface QualityScoreData {
  metric: string
  score: number
  maxScore: number
  color: string
}

export interface TokenUsageData {
  type: string
  tokens: number
  cost: number
}

// Template selection interfaces
export interface TemplateSelection {
  template_id: string
  customizations: {
    audience: AudienceType
    tone: ToneType
    length: LengthType
    focus_areas: FocusArea[]
  }
}

// Data source interfaces for different narrative types
export interface SimulationDataSource {
  country: string
  baseline_life_expectancy: number
  predicted_change: number
  new_life_expectancy: number
  confidence_interval: {
    lower: number
    upper: number
  }
  doctor_density_change: number
  nurse_density_change: number
  spending_change: number
}

export interface BenchmarkDataSource {
  countries: string[]
  best_performer: string
  worst_performer: string
  total_anomalies: number
  high_severity_anomalies: number
  peer_groups: number
  average_score: number
}

export interface AnomalyDataSource {
  total_anomalies: number
  high_severity: number
  medium_severity: number
  low_severity: number
  detection_confidence: number
}

export interface TrendDataSource {
  time_period: string
  countries: string[]
  key_trends: string[]
  significant_changes: string[]
}
