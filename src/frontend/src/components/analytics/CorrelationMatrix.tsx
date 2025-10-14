import React, { useState, useEffect } from 'react'
import { 
  BarChart3, 
  TrendingUp, 
  Activity, 
  Download,
  Eye,
  Settings
} from 'lucide-react'
import { 
  ScatterChart, 
  Scatter, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  Cell
} from 'recharts'

interface CorrelationData {
  x: number
  y: number
  country: string
  correlation: number
}

interface CorrelationMatrixProps {
  data?: CorrelationData[]
  onExport?: (format: string) => void
}

const CorrelationMatrix: React.FC<CorrelationMatrixProps> = ({ 
  data, 
  onExport 
}) => {
  const [selectedPair, setSelectedPair] = useState<string | null>(null)
  const [showDetails, setShowDetails] = useState(false)

  // Sample correlation data
  const sampleData: CorrelationData[] = [
    { x: 2.1, y: 81.2, country: 'Portugal', correlation: 0.85 },
    { x: 2.8, y: 83.1, country: 'Spain', correlation: 0.78 },
    { x: 3.0, y: 82.5, country: 'Sweden', correlation: 0.92 },
    { x: 2.4, y: 81.5, country: 'Greece', correlation: 0.67 },
    { x: 2.6, y: 80.8, country: 'Italy', correlation: 0.73 },
    { x: 2.9, y: 84.2, country: 'Norway', correlation: 0.88 }
  ]

  const correlationData = data || sampleData

  const correlationPairs = [
    { pair: 'Life Expectancy vs Doctor Density', correlation: 0.85, color: '#3498db' },
    { pair: 'Life Expectancy vs Health Spending', correlation: 0.78, color: '#e74c3c' },
    { pair: 'Doctor Density vs Health Spending', correlation: 0.92, color: '#2ecc71' },
    { pair: 'Nurse Density vs Life Expectancy', correlation: 0.67, color: '#f39c12' },
    { pair: 'Health Spending vs GDP per Capita', correlation: 0.73, color: '#9b59b6' }
  ]

  const getCorrelationColor = (correlation: number) => {
    const abs = Math.abs(correlation)
    if (abs >= 0.8) return '#2ecc71' // Strong positive
    if (abs >= 0.6) return '#f39c12' // Moderate
    if (abs >= 0.4) return '#e67e22' // Weak
    return '#95a5a6' // Very weak
  }

  const getCorrelationStrength = (correlation: number) => {
    const abs = Math.abs(correlation)
    if (abs >= 0.8) return 'Strong'
    if (abs >= 0.6) return 'Moderate'
    if (abs >= 0.4) return 'Weak'
    return 'Very Weak'
  }

  return (
    <div className="correlation-matrix">
      <div className="matrix-header">
        <div className="header-content">
          <h3>Correlation Matrix</h3>
          <p>Explore relationships between health indicators</p>
        </div>
        <div className="header-actions">
          <button
            onClick={() => setShowDetails(!showDetails)}
            className="btn-outline inline-flex items-center space-x-2"
          >
            <Eye className="w-4 h-4" />
            <span>{showDetails ? 'Hide' : 'Show'} Details</span>
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

      <div className="matrix-content">
        {/* Correlation Pairs Grid */}
        <div className="correlation-pairs">
          <h4>Correlation Pairs</h4>
          <div className="pairs-grid">
            {correlationPairs.map((pair, index) => (
              <div
                key={index}
                className={`correlation-card ${selectedPair === pair.pair ? 'selected' : ''}`}
                onClick={() => setSelectedPair(pair.pair)}
              >
                <div className="correlation-info">
                  <h5>{pair.pair}</h5>
                  <div className="correlation-value">
                    <span 
                      className="correlation-number"
                      style={{ color: getCorrelationColor(pair.correlation) }}
                    >
                      {pair.correlation.toFixed(2)}
                    </span>
                    <span className="correlation-strength">
                      {getCorrelationStrength(pair.correlation)}
                    </span>
                  </div>
                </div>
                <div 
                  className="correlation-bar"
                  style={{ 
                    backgroundColor: getCorrelationColor(pair.correlation),
                    width: `${Math.abs(pair.correlation) * 100}%`
                  }}
                />
              </div>
            ))}
          </div>
        </div>

        {/* Scatter Plot Visualization */}
        <div className="scatter-plot">
          <h4>Scatter Plot Visualization</h4>
          <div className="plot-container">
            <ResponsiveContainer width="100%" height={400}>
              <ScatterChart data={correlationData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="x" 
                  name="X Value"
                  label={{ value: 'Health Indicator X', position: 'insideBottom', offset: -5 }}
                />
                <YAxis 
                  dataKey="y" 
                  name="Y Value"
                  label={{ value: 'Health Indicator Y', angle: -90, position: 'insideLeft' }}
                />
                <Tooltip 
                  cursor={{ strokeDasharray: '3 3' }}
                  formatter={(value, name, props) => [
                    `${value}`,
                    `${props.payload.country}`
                  ]}
                />
                <Scatter 
                  dataKey="y" 
                  fill="#3498db"
                  stroke="#2980b9"
                  strokeWidth={2}
                />
              </ScatterChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Detailed Analysis */}
        {showDetails && (
          <div className="detailed-analysis">
            <h4>Detailed Analysis</h4>
            <div className="analysis-grid">
              <div className="analysis-card">
                <h5>Correlation Strength</h5>
                <div className="strength-indicators">
                  <div className="strength-item">
                    <span className="strength-label">Strong (≥0.8):</span>
                    <span className="strength-count">
                      {correlationPairs.filter(p => Math.abs(p.correlation) >= 0.8).length}
                    </span>
                  </div>
                  <div className="strength-item">
                    <span className="strength-label">Moderate (0.6-0.8):</span>
                    <span className="strength-count">
                      {correlationPairs.filter(p => Math.abs(p.correlation) >= 0.6 && Math.abs(p.correlation) < 0.8).length}
                    </span>
                  </div>
                  <div className="strength-item">
                    <span className="strength-label">Weak (<0.6):</span>
                    <span className="strength-count">
                      {correlationPairs.filter(p => Math.abs(p.correlation) < 0.6).length}
                    </span>
                  </div>
                </div>
              </div>

              <div className="analysis-card">
                <h5>Key Insights</h5>
                <ul className="insights-list">
                  <li>Strongest correlation: Doctor Density vs Health Spending (0.92)</li>
                  <li>Life Expectancy shows strong correlation with healthcare indicators</li>
                  <li>Economic factors have moderate impact on health outcomes</li>
                  <li>Geographic clustering visible in correlation patterns</li>
                </ul>
              </div>

              <div className="analysis-card">
                <h5>Statistical Significance</h5>
                <div className="significance-info">
                  <div className="significance-item">
                    <span>P-value: <strong>&lt; 0.001</strong></span>
                  </div>
                  <div className="significance-item">
                    <span>Sample Size: <strong>{correlationData.length}</strong></span>
                  </div>
                  <div className="significance-item">
                    <span>Confidence Level: <strong>95%</strong></span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default CorrelationMatrix
