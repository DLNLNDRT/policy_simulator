import React, { useState, useEffect } from 'react'
import { 
  TrendingUp, 
  Calendar,
  Download,
  Settings,
  Eye,
  AlertTriangle
} from 'lucide-react'
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  ReferenceLine,
  Legend
} from 'recharts'

interface ForecastData {
  period: string
  actual?: number
  forecast: number
  confidence_lower: number
  confidence_upper: number
  trend: 'increasing' | 'decreasing' | 'stable'
}

interface ForecastChartProps {
  data?: ForecastData[]
  indicator?: string
  onExport?: (format: string) => void
}

const ForecastChart: React.FC<ForecastChartProps> = ({ 
  data, 
  indicator = 'Life Expectancy',
  onExport 
}) => {
  const [forecastPeriod, setForecastPeriod] = useState(5)
  const [showConfidence, setShowConfidence] = useState(true)
  const [selectedModel, setSelectedModel] = useState('linear')

  // Sample forecast data
  const sampleData: ForecastData[] = [
    { period: '2020', actual: 81.2, forecast: 81.2, confidence_lower: 80.5, confidence_upper: 81.9, trend: 'stable' },
    { period: '2021', actual: 81.5, forecast: 81.5, confidence_lower: 80.8, confidence_upper: 82.2, trend: 'increasing' },
    { period: '2022', actual: 81.8, forecast: 81.8, confidence_lower: 81.1, confidence_upper: 82.5, trend: 'increasing' },
    { period: '2023', actual: 82.1, forecast: 82.1, confidence_lower: 81.4, confidence_upper: 82.8, trend: 'increasing' },
    { period: '2024', actual: 82.4, forecast: 82.4, confidence_lower: 81.7, confidence_upper: 83.1, trend: 'increasing' },
    { period: '2025', forecast: 82.7, confidence_lower: 81.8, confidence_upper: 83.6, trend: 'increasing' },
    { period: '2026', forecast: 83.0, confidence_lower: 81.9, confidence_upper: 84.1, trend: 'increasing' },
    { period: '2027', forecast: 83.3, confidence_lower: 82.0, confidence_upper: 84.6, trend: 'increasing' },
    { period: '2028', forecast: 83.6, confidence_lower: 82.1, confidence_upper: 85.1, trend: 'increasing' },
    { period: '2029', forecast: 83.9, confidence_lower: 82.2, confidence_upper: 85.6, trend: 'increasing' }
  ]

  const forecastData = data || sampleData

  const models = [
    { id: 'linear', name: 'Linear Regression', description: 'Simple trend continuation' },
    { id: 'exponential', name: 'Exponential Smoothing', description: 'Weighted historical data' },
    { id: 'arima', name: 'ARIMA', description: 'Advanced time series analysis' },
    { id: 'prophet', name: 'Prophet', description: 'Facebook\'s forecasting tool' }
  ]

  const getTrendColor = (trend: string) => {
    switch (trend) {
      case 'increasing': return '#2ecc71'
      case 'decreasing': return '#e74c3c'
      default: return '#95a5a6'
    }
  }

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'increasing': return '↗'
      case 'decreasing': return '↘'
      default: return '→'
    }
  }

  const calculateAccuracy = () => {
    const actualData = forecastData.filter(d => d.actual !== undefined)
    if (actualData.length < 2) return null

    const errors = actualData.map(d => Math.abs((d.actual! - d.forecast) / d.actual!))
    const mape = errors.reduce((sum, error) => sum + error, 0) / errors.length
    return (1 - mape) * 100
  }

  const accuracy = calculateAccuracy()

  return (
    <div className="forecast-chart">
      <div className="forecast-header">
        <div className="header-content">
          <h3>Forecast Analysis</h3>
          <p>Predictive modeling for {indicator}</p>
        </div>
        <div className="header-actions">
          <button
            onClick={() => setShowConfidence(!showConfidence)}
            className="btn-outline inline-flex items-center space-x-2"
          >
            <Eye className="w-4 h-4" />
            <span>{showConfidence ? 'Hide' : 'Show'} Confidence</span>
          </button>
          {onExport && (
            <button
              onClick={() => onExport('csv')}
              className="btn-outline inline-flex items-center space-x-2"
            >
              <Download className="w-4 h-4" />
              <span>Export</span>
            </button>
          )}
        </div>
      </div>

      <div className="forecast-content">
        {/* Model Selection */}
        <div className="model-selection">
          <h4>Forecasting Model</h4>
          <div className="model-grid">
            {models.map(model => (
              <button
                key={model.id}
                onClick={() => setSelectedModel(model.id)}
                className={`model-card ${selectedModel === model.id ? 'selected' : ''}`}
              >
                <h5>{model.name}</h5>
                <p>{model.description}</p>
              </button>
            ))}
          </div>
        </div>

        {/* Forecast Chart */}
        <div className="forecast-visualization">
          <div className="chart-header">
            <h4>Forecast Visualization</h4>
            <div className="chart-controls">
              <div className="control-group">
                <label>Forecast Period:</label>
                <select 
                  value={forecastPeriod} 
                  onChange={(e) => setForecastPeriod(Number(e.target.value))}
                  className="form-select"
                >
                  <option value={3}>3 years</option>
                  <option value={5}>5 years</option>
                  <option value={10}>10 years</option>
                </select>
              </div>
            </div>
          </div>

          <div className="chart-container">
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={forecastData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="period"
                  label={{ value: 'Year', position: 'insideBottom', offset: -5 }}
                />
                <YAxis 
                  label={{ value: indicator, angle: -90, position: 'insideLeft' }}
                />
                <Tooltip 
                  formatter={(value, name) => [
                    `${Number(value).toFixed(2)}`,
                    name === 'actual' ? 'Actual' : 
                    name === 'forecast' ? 'Forecast' :
                    name === 'confidence_lower' ? 'Lower Bound' :
                    name === 'confidence_upper' ? 'Upper Bound' : name
                  ]}
                />
                <Legend />
                
                {/* Actual data line */}
                <Line 
                  type="monotone" 
                  dataKey="actual" 
                  stroke="#3498db" 
                  strokeWidth={3}
                  dot={{ fill: '#3498db', strokeWidth: 2, r: 4 }}
                  name="Actual"
                />
                
                {/* Forecast line */}
                <Line 
                  type="monotone" 
                  dataKey="forecast" 
                  stroke="#e74c3c" 
                  strokeWidth={3}
                  strokeDasharray="5 5"
                  dot={{ fill: '#e74c3c', strokeWidth: 2, r: 4 }}
                  name="Forecast"
                />
                
                {/* Confidence intervals */}
                {showConfidence && (
                  <>
                    <Line 
                      type="monotone" 
                      dataKey="confidence_lower" 
                      stroke="#95a5a6" 
                      strokeWidth={1}
                      strokeDasharray="2 2"
                      dot={false}
                      name="Lower Bound"
                    />
                    <Line 
                      type="monotone" 
                      dataKey="confidence_upper" 
                      stroke="#95a5a6" 
                      strokeWidth={1}
                      strokeDasharray="2 2"
                      dot={false}
                      name="Upper Bound"
                    />
                  </>
                )}
                
                {/* Reference line for current year */}
                <ReferenceLine 
                  x="2024" 
                  stroke="#f39c12" 
                  strokeDasharray="3 3"
                  label={{ value: "Current Year", position: "top" }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Forecast Summary */}
        <div className="forecast-summary">
          <h4>Forecast Summary</h4>
          <div className="summary-grid">
            <div className="summary-card">
              <h5>Model Performance</h5>
              <div className="performance-metrics">
                <div className="metric">
                  <span className="metric-label">Accuracy:</span>
                  <span className="metric-value">
                    {accuracy ? `${accuracy.toFixed(1)}%` : 'N/A'}
                  </span>
                </div>
                <div className="metric">
                  <span className="metric-label">Model:</span>
                  <span className="metric-value">
                    {models.find(m => m.id === selectedModel)?.name}
                  </span>
                </div>
                <div className="metric">
                  <span className="metric-label">Data Points:</span>
                  <span className="metric-value">{forecastData.length}</span>
                </div>
              </div>
            </div>

            <div className="summary-card">
              <h5>Trend Analysis</h5>
              <div className="trend-analysis">
                {forecastData.slice(-3).map((data, index) => (
                  <div key={index} className="trend-item">
                    <span className="trend-period">{data.period}</span>
                    <span 
                      className="trend-value"
                      style={{ color: getTrendColor(data.trend) }}
                    >
                      {data.forecast.toFixed(1)} {getTrendIcon(data.trend)}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            <div className="summary-card">
              <h5>Confidence Intervals</h5>
              <div className="confidence-info">
                <div className="confidence-item">
                  <span>95% Confidence Level</span>
                </div>
                <div className="confidence-item">
                  <span>Lower Bound: {forecastData[forecastData.length - 1]?.confidence_lower.toFixed(1)}</span>
                </div>
                <div className="confidence-item">
                  <span>Upper Bound: {forecastData[forecastData.length - 1]?.confidence_upper.toFixed(1)}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Forecast Warnings */}
        <div className="forecast-warnings">
          <div className="warning-header">
            <AlertTriangle className="w-5 h-5 text-yellow-500" />
            <h5>Forecast Limitations</h5>
          </div>
          <ul className="warning-list">
            <li>Forecasts are based on historical trends and may not account for future policy changes</li>
            <li>Confidence intervals represent statistical uncertainty, not real-world variability</li>
            <li>Long-term forecasts become less reliable as the time horizon increases</li>
            <li>External factors (pandemics, economic crises) can significantly impact outcomes</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

export default ForecastChart
