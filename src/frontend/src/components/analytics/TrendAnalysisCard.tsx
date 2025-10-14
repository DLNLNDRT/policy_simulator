import React, { useState } from 'react'
import { TrendingUp, TrendingDown, Minus, Play, Download, Info } from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

interface TrendAnalysisData {
  indicator: string
  country: string
  time_period: {
    start: number
    end: number
  }
  trend_direction: 'increasing' | 'decreasing' | 'stable'
  trend_strength: number
  annual_change: number
  total_change: number
  change_percentage: number
  statistical_significance: number
  confidence_interval: {
    lower: number
    upper: number
  }
  r_squared: number
  sample_size: number
  data_points: Array<{
    year: number
    value: number
  }>
}

interface TrendAnalysisCardProps {
  data?: TrendAnalysisData
  onAnalyze?: (config: any) => void
}

const TrendAnalysisCard: React.FC<TrendAnalysisCardProps> = ({ data, onAnalyze }) => {
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysisConfig, setAnalysisConfig] = useState({
    indicator: 'life_expectancy',
    country: 'PRT',
    timePeriod: { start: 2020, end: 2024 }
  })

  const handleAnalyze = async () => {
    if (!onAnalyze) return

    setIsAnalyzing(true)
    try {
      await onAnalyze(analysisConfig)
    } finally {
      setIsAnalyzing(false)
    }
  }

  const getTrendIcon = (direction: string) => {
    switch (direction) {
      case 'increasing':
        return <TrendingUp className="w-5 h-5 text-green-600" />
      case 'decreasing':
        return <TrendingDown className="w-5 h-5 text-red-600" />
      default:
        return <Minus className="w-5 h-5 text-gray-600" />
    }
  }

  const getTrendColor = (direction: string) => {
    switch (direction) {
      case 'increasing':
        return 'text-green-600'
      case 'decreasing':
        return 'text-red-600'
      default:
        return 'text-gray-600'
    }
  }

  const formatTrendStrength = (strength: number) => {
    if (strength >= 0.8) return 'Very Strong'
    if (strength >= 0.6) return 'Strong'
    if (strength >= 0.4) return 'Moderate'
    if (strength >= 0.2) return 'Weak'
    return 'Very Weak'
  }

  const formatSignificance = (pValue: number) => {
    if (pValue < 0.001) return 'Highly Significant (p < 0.001)'
    if (pValue < 0.01) return 'Very Significant (p < 0.01)'
    if (pValue < 0.05) return 'Significant (p < 0.05)'
    if (pValue < 0.1) return 'Marginally Significant (p < 0.1)'
    return 'Not Significant (p >= 0.1)'
  }

  return (
    <div className="trend-analysis-card">
      <div className="card-header">
        <div className="header-content">
          <h3 className="card-title">Trend Analysis</h3>
          <p className="card-description">
            Analyze trends in health indicators over time
          </p>
        </div>
        <div className="header-actions">
          <button
            onClick={handleAnalyze}
            disabled={isAnalyzing}
            className="btn-primary inline-flex items-center space-x-2"
          >
            <Play className="w-4 h-4" />
            <span>{isAnalyzing ? 'Analyzing...' : 'Analyze'}</span>
          </button>
        </div>
      </div>

      <div className="card-content">
        {/* Analysis Configuration */}
        <div className="analysis-config">
          <div className="config-row">
            <div className="config-item">
              <label>Indicator</label>
              <select
                value={analysisConfig.indicator}
                onChange={(e) => setAnalysisConfig({
                  ...analysisConfig,
                  indicator: e.target.value
                })}
                className="config-select"
              >
                <option value="life_expectancy">Life Expectancy</option>
                <option value="doctor_density">Doctor Density</option>
                <option value="nurse_density">Nurse Density</option>
                <option value="government_spending">Government Spending</option>
              </select>
            </div>
            <div className="config-item">
              <label>Country</label>
              <select
                value={analysisConfig.country}
                onChange={(e) => setAnalysisConfig({
                  ...analysisConfig,
                  country: e.target.value
                })}
                className="config-select"
              >
                <option value="PRT">Portugal</option>
                <option value="ESP">Spain</option>
                <option value="SWE">Sweden</option>
                <option value="GRC">Greece</option>
              </select>
            </div>
            <div className="config-item">
              <label>Time Period</label>
              <div className="time-inputs">
                <input
                  type="number"
                  value={analysisConfig.timePeriod.start}
                  onChange={(e) => setAnalysisConfig({
                    ...analysisConfig,
                    timePeriod: {
                      ...analysisConfig.timePeriod,
                      start: parseInt(e.target.value)
                    }
                  })}
                  className="config-input"
                  placeholder="Start Year"
                />
                <span>to</span>
                <input
                  type="number"
                  value={analysisConfig.timePeriod.end}
                  onChange={(e) => setAnalysisConfig({
                    ...analysisConfig,
                    timePeriod: {
                      ...analysisConfig.timePeriod,
                      end: parseInt(e.target.value)
                    }
                  })}
                  className="config-input"
                  placeholder="End Year"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Results */}
        {data && (
          <div className="analysis-results">
            {/* Trend Summary */}
            <div className="trend-summary">
              <div className="trend-header">
                <div className="trend-icon">
                  {getTrendIcon(data.trend_direction)}
                </div>
                <div className="trend-info">
                  <h4 className={`trend-direction ${getTrendColor(data.trend_direction)}`}>
                    {data.trend_direction.charAt(0).toUpperCase() + data.trend_direction.slice(1)} Trend
                  </h4>
                  <p className="trend-description">
                    {data.indicator.replace('_', ' ')} in {data.country} ({data.time_period.start}-{data.time_period.end})
                  </p>
                </div>
              </div>
              
              <div className="trend-metrics">
                <div className="metric">
                  <div className="metric-label">Annual Change</div>
                  <div className={`metric-value ${getTrendColor(data.trend_direction)}`}>
                    {data.annual_change > 0 ? '+' : ''}{data.annual_change.toFixed(3)}
                  </div>
                </div>
                <div className="metric">
                  <div className="metric-label">Total Change</div>
                  <div className={`metric-value ${getTrendColor(data.trend_direction)}`}>
                    {data.total_change > 0 ? '+' : ''}{data.total_change.toFixed(3)}
                  </div>
                </div>
                <div className="metric">
                  <div className="metric-label">Change %</div>
                  <div className={`metric-value ${getTrendColor(data.trend_direction)}`}>
                    {data.change_percentage > 0 ? '+' : ''}{data.change_percentage.toFixed(2)}%
                  </div>
                </div>
              </div>
            </div>

            {/* Statistical Information */}
            <div className="statistical-info">
              <div className="stat-row">
                <div className="stat-item">
                  <div className="stat-label">Trend Strength</div>
                  <div className="stat-value">
                    {formatTrendStrength(data.trend_strength)} ({data.trend_strength.toFixed(3)})
                  </div>
                </div>
                <div className="stat-item">
                  <div className="stat-label">Statistical Significance</div>
                  <div className="stat-value">
                    {formatSignificance(data.statistical_significance)}
                  </div>
                </div>
                <div className="stat-item">
                  <div className="stat-label">R-squared</div>
                  <div className="stat-value">
                    {data.r_squared.toFixed(3)}
                  </div>
                </div>
                <div className="stat-item">
                  <div className="stat-label">Sample Size</div>
                  <div className="stat-value">
                    {data.sample_size} data points
                  </div>
                </div>
              </div>
            </div>

            {/* Confidence Interval */}
            <div className="confidence-interval">
              <div className="ci-header">
                <Info className="w-4 h-4" />
                <span>95% Confidence Interval for Trend</span>
              </div>
              <div className="ci-range">
                <span className="ci-value">{data.confidence_interval.lower.toFixed(3)}</span>
                <span className="ci-separator">to</span>
                <span className="ci-value">{data.confidence_interval.upper.toFixed(3)}</span>
              </div>
            </div>

            {/* Trend Chart */}
            {data.data_points && data.data_points.length > 0 && (
              <div className="trend-chart">
                <h4>Trend Visualization</h4>
                <div className="chart-container">
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={data.data_points}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis 
                        dataKey="year" 
                        tick={{ fontSize: 12 }}
                        tickFormatter={(value) => value.toString()}
                      />
                      <YAxis 
                        tick={{ fontSize: 12 }}
                        tickFormatter={(value) => value.toFixed(1)}
                      />
                      <Tooltip 
                        formatter={(value: number) => [value.toFixed(3), 'Value']}
                        labelFormatter={(label) => `Year: ${label}`}
                      />
                      <Line 
                        type="monotone" 
                        dataKey="value" 
                        stroke="#3498db" 
                        strokeWidth={2}
                        dot={{ fill: '#3498db', strokeWidth: 2, r: 4 }}
                        activeDot={{ r: 6, stroke: '#3498db', strokeWidth: 2 }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </div>
            )}

            {/* Interpretation */}
            <div className="interpretation">
              <h4>Interpretation</h4>
              <div className="interpretation-content">
                <p>
                  The analysis shows a <strong>{data.trend_direction}</strong> trend in {data.indicator.replace('_', ' ')} 
                  for {data.country} over the period {data.time_period.start}-{data.time_period.end}. 
                  The trend has a <strong>{formatTrendStrength(data.trend_strength).toLowerCase()}</strong> strength 
                  (R² = {data.r_squared.toFixed(3)}) and is <strong>{formatSignificance(data.statistical_significance).toLowerCase()}</strong>.
                </p>
                <p>
                  On average, the indicator {data.annual_change > 0 ? 'increased' : 'decreased'} by {Math.abs(data.annual_change).toFixed(3)} 
                  units per year, resulting in a total {data.total_change > 0 ? 'increase' : 'decrease'} of {Math.abs(data.total_change).toFixed(3)} 
                  units ({Math.abs(data.change_percentage).toFixed(2)}%) over the entire period.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* No Data State */}
        {!data && (
          <div className="no-data-state">
            <div className="no-data-content">
              <TrendingUp className="w-16 h-16 text-gray-400" />
              <h4>No Trend Analysis Data</h4>
              <p>Configure the analysis parameters and click "Analyze" to generate trend analysis results.</p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default TrendAnalysisCard
