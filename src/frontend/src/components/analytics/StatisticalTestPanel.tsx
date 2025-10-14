import React, { useState, useEffect } from 'react'
import { 
  Calculator, 
  TrendingUp, 
  AlertTriangle,
  CheckCircle,
  XCircle,
  Download,
  Settings,
  BarChart3
} from 'lucide-react'

interface StatisticalTest {
  id: string
  name: string
  description: string
  p_value: number
  significance: boolean
  test_statistic: number
  critical_value: number
  confidence_level: number
  result: 'significant' | 'not_significant'
}

interface StatisticalTestPanelProps {
  tests?: StatisticalTest[]
  onExport?: (format: string) => void
}

const StatisticalTestPanel: React.FC<StatisticalTestPanelProps> = ({ 
  tests, 
  onExport 
}) => {
  const [selectedTest, setSelectedTest] = useState<string | null>(null)
  const [showDetails, setShowDetails] = useState(false)
  const [confidenceLevel, setConfidenceLevel] = useState(0.05)

  // Sample statistical tests
  const sampleTests: StatisticalTest[] = [
    {
      id: 't_test_1',
      name: 'T-Test: Life Expectancy vs Doctor Density',
      description: 'Testing if there is a significant difference in life expectancy between countries with high and low doctor density',
      p_value: 0.0023,
      significance: true,
      test_statistic: 3.45,
      critical_value: 2.101,
      confidence_level: 0.95,
      result: 'significant'
    },
    {
      id: 'correlation_test',
      name: 'Correlation Test: Health Spending vs Life Expectancy',
      description: 'Testing the strength and significance of correlation between health spending and life expectancy',
      p_value: 0.0001,
      significance: true,
      test_statistic: 0.78,
      critical_value: 0.632,
      confidence_level: 0.95,
      result: 'significant'
    },
    {
      id: 'anova_test',
      name: 'ANOVA: Regional Health Outcomes',
      description: 'Testing if there are significant differences in health outcomes across different regions',
      p_value: 0.0234,
      significance: true,
      test_statistic: 4.12,
      critical_value: 3.89,
      confidence_level: 0.95,
      result: 'significant'
    },
    {
      id: 'chi_square',
      name: 'Chi-Square: Healthcare Access',
      description: 'Testing independence between healthcare access and demographic factors',
      p_value: 0.156,
      significance: false,
      test_statistic: 2.34,
      critical_value: 3.84,
      confidence_level: 0.95,
      result: 'not_significant'
    },
    {
      id: 'regression_test',
      name: 'Regression: Multiple Variables',
      description: 'Testing the overall significance of a multiple regression model',
      p_value: 0.0001,
      significance: true,
      test_statistic: 12.45,
      critical_value: 2.58,
      confidence_level: 0.95,
      result: 'significant'
    }
  ]

  const statisticalTests = tests || sampleTests

  const getSignificanceColor = (significant: boolean) => {
    return significant ? '#2ecc71' : '#e74c3c'
  }

  const getSignificanceIcon = (significant: boolean) => {
    return significant ? CheckCircle : XCircle
  }

  const getSignificanceText = (significant: boolean) => {
    return significant ? 'Significant' : 'Not Significant'
  }

  const getPValueInterpretation = (pValue: number) => {
    if (pValue < 0.001) return 'Highly Significant (p < 0.001)'
    if (pValue < 0.01) return 'Very Significant (p < 0.01)'
    if (pValue < 0.05) return 'Significant (p < 0.05)'
    if (pValue < 0.1) return 'Marginally Significant (p < 0.1)'
    return 'Not Significant (p ≥ 0.1)'
  }

  const getEffectSize = (testStatistic: number, testType: string) => {
    if (testType.includes('correlation')) {
      const absValue = Math.abs(testStatistic)
      if (absValue >= 0.7) return 'Large Effect'
      if (absValue >= 0.5) return 'Medium Effect'
      if (absValue >= 0.3) return 'Small Effect'
      return 'Negligible Effect'
    }
    
    // For other tests, use Cohen's conventions
    if (Math.abs(testStatistic) >= 0.8) return 'Large Effect'
    if (Math.abs(testStatistic) >= 0.5) return 'Medium Effect'
    if (Math.abs(testStatistic) >= 0.2) return 'Small Effect'
    return 'Negligible Effect'
  }

  return (
    <div className="statistical-test-panel">
      <div className="test-header">
        <div className="header-content">
          <h3>Statistical Tests</h3>
          <p>Comprehensive statistical analysis of health indicators</p>
        </div>
        <div className="header-actions">
          <div className="control-group">
            <label>Confidence Level:</label>
            <select 
              value={confidenceLevel} 
              onChange={(e) => setConfidenceLevel(Number(e.target.value))}
              className="form-select"
            >
              <option value={0.01}>99% (α = 0.01)</option>
              <option value={0.05}>95% (α = 0.05)</option>
              <option value={0.1}>90% (α = 0.1)</option>
            </select>
          </div>
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

      <div className="test-content">
        {/* Test Results Grid */}
        <div className="test-results">
          <h4>Test Results</h4>
          <div className="results-grid">
            {statisticalTests.map((test) => {
              const SignificanceIcon = getSignificanceIcon(test.significance)
              return (
                <div
                  key={test.id}
                  className={`test-card ${selectedTest === test.id ? 'selected' : ''}`}
                  onClick={() => setSelectedTest(test.id)}
                >
                  <div className="test-header-card">
                    <h5>{test.name}</h5>
                    <div className="test-status">
                      <SignificanceIcon 
                        className="w-5 h-5" 
                        style={{ color: getSignificanceColor(test.significance) }}
                      />
                      <span 
                        className="significance-text"
                        style={{ color: getSignificanceColor(test.significance) }}
                      >
                        {getSignificanceText(test.significance)}
                      </span>
                    </div>
                  </div>
                  
                  <div className="test-metrics">
                    <div className="metric">
                      <span className="metric-label">P-value:</span>
                      <span className="metric-value">{test.p_value.toFixed(4)}</span>
                    </div>
                    <div className="metric">
                      <span className="metric-label">Test Statistic:</span>
                      <span className="metric-value">{test.test_statistic.toFixed(3)}</span>
                    </div>
                    <div className="metric">
                      <span className="metric-label">Critical Value:</span>
                      <span className="metric-value">{test.critical_value.toFixed(3)}</span>
                    </div>
                  </div>

                  <div className="test-interpretation">
                    <p>{getPValueInterpretation(test.p_value)}</p>
                    <p>Effect Size: {getEffectSize(test.test_statistic, test.name)}</p>
                  </div>
                </div>
              )
            })}
          </div>
        </div>

        {/* Detailed Test Analysis */}
        {selectedTest && (
          <div className="detailed-analysis">
            <h4>Detailed Analysis</h4>
            {(() => {
              const test = statisticalTests.find(t => t.id === selectedTest)
              if (!test) return null

              return (
                <div className="analysis-content">
                  <div className="analysis-header">
                    <h5>{test.name}</h5>
                    <button
                      onClick={() => setShowDetails(!showDetails)}
                      className="btn-outline"
                    >
                      {showDetails ? 'Hide' : 'Show'} Details
                    </button>
                  </div>

                  <div className="analysis-description">
                    <p>{test.description}</p>
                  </div>

                  <div className="analysis-metrics">
                    <div className="metrics-grid">
                      <div className="metric-card">
                        <h6>Test Statistics</h6>
                        <div className="metric-details">
                          <div className="detail-item">
                            <span>Test Statistic:</span>
                            <span className="value">{test.test_statistic.toFixed(4)}</span>
                          </div>
                          <div className="detail-item">
                            <span>Critical Value:</span>
                            <span className="value">{test.critical_value.toFixed(4)}</span>
                          </div>
                          <div className="detail-item">
                            <span>P-value:</span>
                            <span className="value">{test.p_value.toFixed(6)}</span>
                          </div>
                        </div>
                      </div>

                      <div className="metric-card">
                        <h6>Significance</h6>
                        <div className="significance-details">
                          <div className="significance-item">
                            <span>Result:</span>
                            <span 
                              className="significance-value"
                              style={{ color: getSignificanceColor(test.significance) }}
                            >
                              {getSignificanceText(test.significance)}
                            </span>
                          </div>
                          <div className="significance-item">
                            <span>Confidence Level:</span>
                            <span className="value">{(test.confidence_level * 100).toFixed(0)}%</span>
                          </div>
                          <div className="significance-item">
                            <span>Effect Size:</span>
                            <span className="value">{getEffectSize(test.test_statistic, test.name)}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  {showDetails && (
                    <div className="technical-details">
                      <h6>Technical Details</h6>
                      <div className="technical-content">
                        <div className="detail-section">
                          <h7>Hypothesis Testing</h7>
                          <ul>
                            <li>Null Hypothesis (H₀): No significant relationship exists</li>
                            <li>Alternative Hypothesis (H₁): Significant relationship exists</li>
                            <li>Significance Level (α): {(confidenceLevel * 100).toFixed(0)}%</li>
                          </ul>
                        </div>
                        
                        <div className="detail-section">
                          <h7>Decision Rule</h7>
                          <p>
                            {test.p_value < confidenceLevel 
                              ? `Since p-value (${test.p_value.toFixed(4)}) < α (${confidenceLevel}), we reject the null hypothesis.`
                              : `Since p-value (${test.p_value.toFixed(4)}) ≥ α (${confidenceLevel}), we fail to reject the null hypothesis.`
                            }
                          </p>
                        </div>

                        <div className="detail-section">
                          <h7>Interpretation</h7>
                          <p>
                            {test.significance 
                              ? 'The test indicates a statistically significant relationship between the variables.'
                              : 'The test does not provide sufficient evidence of a significant relationship.'
                            }
                          </p>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )
            })()}
          </div>
        )}

        {/* Summary Statistics */}
        <div className="summary-statistics">
          <h4>Summary Statistics</h4>
          <div className="summary-grid">
            <div className="summary-card">
              <h5>Test Overview</h5>
              <div className="summary-metrics">
                <div className="summary-metric">
                  <span>Total Tests:</span>
                  <span>{statisticalTests.length}</span>
                </div>
                <div className="summary-metric">
                  <span>Significant:</span>
                  <span style={{ color: '#2ecc71' }}>
                    {statisticalTests.filter(t => t.significance).length}
                  </span>
                </div>
                <div className="summary-metric">
                  <span>Not Significant:</span>
                  <span style={{ color: '#e74c3c' }}>
                    {statisticalTests.filter(t => !t.significance).length}
                  </span>
                </div>
              </div>
            </div>

            <div className="summary-card">
              <h5>Effect Sizes</h5>
              <div className="effect-sizes">
                <div className="effect-item">
                  <span>Large Effect:</span>
                  <span>
                    {statisticalTests.filter(t => getEffectSize(t.test_statistic, t.name) === 'Large Effect').length}
                  </span>
                </div>
                <div className="effect-item">
                  <span>Medium Effect:</span>
                  <span>
                    {statisticalTests.filter(t => getEffectSize(t.test_statistic, t.name) === 'Medium Effect').length}
                  </span>
                </div>
                <div className="effect-item">
                  <span>Small Effect:</span>
                  <span>
                    {statisticalTests.filter(t => getEffectSize(t.test_statistic, t.name) === 'Small Effect').length}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default StatisticalTestPanel
