import React, { useState } from 'react'
import { 
  GitCompare, 
  TrendingUp, 
  BarChart3, 
  Users, 
  Calendar,
  Play,
  Download,
  Settings,
  Eye
} from 'lucide-react'
import { 
  LineChart, 
  Line, 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  Legend
} from 'recharts'

interface ComparisonToolsProps {
  onCompare?: (config: any) => void
}

const ComparisonTools: React.FC<ComparisonToolsProps> = ({ onCompare }) => {
  const [comparisonConfig, setComparisonConfig] = useState({
    type: 'countries', // 'countries', 'time_periods', 'scenarios'
    countries: ['PRT', 'ESP'],
    indicators: ['life_expectancy'],
    timePeriod: { start: 2020, end: 2024 },
    scenarios: ['baseline', 'optimistic', 'pessimistic']
  })

  const [isComparing, setIsComparing] = useState(false)
  const [showResults, setShowResults] = useState(false)
  const [comparisonResults, setComparisonResults] = useState<any>(null)

  const countries = [
    { code: 'PRT', name: 'Portugal' },
    { code: 'ESP', name: 'Spain' },
    { code: 'SWE', name: 'Sweden' },
    { code: 'GRC', name: 'Greece' }
  ]

  const indicators = [
    { code: 'life_expectancy', name: 'Life Expectancy' },
    { code: 'doctor_density', name: 'Doctor Density' },
    { code: 'nurse_density', name: 'Nurse Density' },
    { code: 'government_spending', name: 'Government Spending' }
  ]

  const comparisonTypes = [
    { 
      id: 'countries', 
      label: 'Country Comparison', 
      icon: Users, 
      description: 'Compare health indicators across different countries' 
    },
    { 
      id: 'time_periods', 
      label: 'Time Period Comparison', 
      icon: Calendar, 
      description: 'Compare indicators across different time periods' 
    },
    { 
      id: 'scenarios', 
      label: 'Scenario Comparison', 
      icon: TrendingUp, 
      description: 'Compare different policy scenarios' 
    }
  ]

  const handleCompare = async () => {
    if (!onCompare) return

    setIsComparing(true)
    try {
      // Mock comparison data
      const mockResults = {
        type: comparisonConfig.type,
        countries: comparisonConfig.countries,
        indicators: comparisonConfig.indicators,
        timePeriod: comparisonConfig.timePeriod,
        results: {
          statistical_significance: 0.023,
          effect_size: 0.45,
          interpretation: 'Significant differences found between selected countries',
          data: generateMockComparisonData()
        }
      }

      setComparisonResults(mockResults)
      setShowResults(true)
      
      await onCompare(comparisonConfig)
    } finally {
      setIsComparing(false)
    }
  }

  const generateMockComparisonData = () => {
    if (comparisonConfig.type === 'countries') {
      return comparisonConfig.countries.map(country => ({
        country: country,
        life_expectancy: 80 + Math.random() * 5,
        doctor_density: 2 + Math.random() * 2,
        nurse_density: 5 + Math.random() * 3,
        government_spending: 6 + Math.random() * 3
      }))
    } else if (comparisonConfig.type === 'time_periods') {
      return Array.from({ length: 5 }, (_, i) => ({
        year: 2020 + i,
        life_expectancy: 80 + i * 0.5 + Math.random() * 0.5,
        doctor_density: 2 + i * 0.1 + Math.random() * 0.1,
        nurse_density: 5 + i * 0.2 + Math.random() * 0.2,
        government_spending: 6 + i * 0.3 + Math.random() * 0.3
      }))
    }
    return []
  }

  const renderComparisonChart = () => {
    if (!comparisonResults?.results?.data) return null

    const data = comparisonResults.results.data

    if (comparisonConfig.type === 'countries') {
      return (
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="country" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="life_expectancy" fill="#3498db" name="Life Expectancy" />
            <Bar dataKey="doctor_density" fill="#e74c3c" name="Doctor Density" />
            <Bar dataKey="nurse_density" fill="#2ecc71" name="Nurse Density" />
            <Bar dataKey="government_spending" fill="#f39c12" name="Government Spending" />
          </BarChart>
        </ResponsiveContainer>
      )
    } else if (comparisonConfig.type === 'time_periods') {
      return (
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="year" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line 
              type="monotone" 
              dataKey="life_expectancy" 
              stroke="#3498db" 
              strokeWidth={2}
              name="Life Expectancy"
            />
            <Line 
              type="monotone" 
              dataKey="doctor_density" 
              stroke="#e74c3c" 
              strokeWidth={2}
              name="Doctor Density"
            />
            <Line 
              type="monotone" 
              dataKey="nurse_density" 
              stroke="#2ecc71" 
              strokeWidth={2}
              name="Nurse Density"
            />
            <Line 
              type="monotone" 
              dataKey="government_spending" 
              stroke="#f39c12" 
              strokeWidth={2}
              name="Government Spending"
            />
          </LineChart>
        </ResponsiveContainer>
      )
    }

    return null
  }

  return (
    <div className="comparison-tools">
      <div className="tools-header">
        <div className="header-content">
          <h2 className="tools-title">Comparison Tools</h2>
          <p className="tools-description">
            Compare countries, time periods, and scenarios for comprehensive analysis
          </p>
        </div>
        <div className="header-actions">
          <button
            onClick={() => setShowResults(!showResults)}
            className="btn-outline inline-flex items-center space-x-2"
            disabled={!comparisonResults}
          >
            <Eye className="w-4 h-4" />
            <span>{showResults ? 'Hide' : 'Show'} Results</span>
          </button>
          <button
            onClick={handleCompare}
            disabled={isComparing}
            className="btn-primary inline-flex items-center space-x-2"
          >
            <Play className="w-4 h-4" />
            <span>{isComparing ? 'Comparing...' : 'Run Comparison'}</span>
          </button>
        </div>
      </div>

      <div className="tools-content">
        <div className="tools-main">
          {/* Comparison Type Selection */}
          <div className="comparison-type-section">
            <h3>Comparison Type</h3>
            <div className="comparison-type-grid">
              {comparisonTypes.map(compType => {
                const Icon = compType.icon
                return (
                  <button
                    key={compType.id}
                    onClick={() => setComparisonConfig({ ...comparisonConfig, type: compType.id })}
                    className={`comparison-type-card ${comparisonConfig.type === compType.id ? 'selected' : ''}`}
                  >
                    <Icon className="w-8 h-8" />
                    <h4>{compType.label}</h4>
                    <p>{compType.description}</p>
                  </button>
                )
              })}
            </div>
          </div>

          {/* Configuration Panel */}
          <div className="config-panel">
            <h3>Comparison Configuration</h3>
            
            {comparisonConfig.type === 'countries' && (
              <div className="config-section">
                <h4>Select Countries</h4>
                <div className="country-selection">
                  {countries.map(country => (
                    <label key={country.code} className="selection-item">
                      <input
                        type="checkbox"
                        checked={comparisonConfig.countries.includes(country.code)}
                        onChange={(e) => {
                          if (e.target.checked) {
                            setComparisonConfig({
                              ...comparisonConfig,
                              countries: [...comparisonConfig.countries, country.code]
                            })
                          } else {
                            setComparisonConfig({
                              ...comparisonConfig,
                              countries: comparisonConfig.countries.filter(c => c !== country.code)
                            })
                          }
                        }}
                      />
                      <span>{country.name} ({country.code})</span>
                    </label>
                  ))}
                </div>
              </div>
            )}

            {comparisonConfig.type === 'time_periods' && (
              <div className="config-section">
                <h4>Time Periods</h4>
                <div className="time-period-config">
                  <div className="form-group">
                    <label>Start Year</label>
                    <input
                      type="number"
                      value={comparisonConfig.timePeriod.start}
                      onChange={(e) => setComparisonConfig({
                        ...comparisonConfig,
                        timePeriod: { ...comparisonConfig.timePeriod, start: parseInt(e.target.value) }
                      })}
                      className="form-input"
                      min="1990"
                      max="2024"
                    />
                  </div>
                  <div className="form-group">
                    <label>End Year</label>
                    <input
                      type="number"
                      value={comparisonConfig.timePeriod.end}
                      onChange={(e) => setComparisonConfig({
                        ...comparisonConfig,
                        timePeriod: { ...comparisonConfig.timePeriod, end: parseInt(e.target.value) }
                      })}
                      className="form-input"
                      min="1990"
                      max="2024"
                    />
                  </div>
                </div>
              </div>
            )}

            {comparisonConfig.type === 'scenarios' && (
              <div className="config-section">
                <h4>Policy Scenarios</h4>
                <div className="scenario-selection">
                  <label className="selection-item">
                    <input
                      type="checkbox"
                      checked={comparisonConfig.scenarios.includes('baseline')}
                      onChange={(e) => {
                        if (e.target.checked) {
                          setComparisonConfig({
                            ...comparisonConfig,
                            scenarios: [...comparisonConfig.scenarios, 'baseline']
                          })
                        } else {
                          setComparisonConfig({
                            ...comparisonConfig,
                            scenarios: comparisonConfig.scenarios.filter(s => s !== 'baseline')
                          })
                        }
                      }}
                    />
                    <span>Baseline Scenario</span>
                  </label>
                  <label className="selection-item">
                    <input
                      type="checkbox"
                      checked={comparisonConfig.scenarios.includes('optimistic')}
                      onChange={(e) => {
                        if (e.target.checked) {
                          setComparisonConfig({
                            ...comparisonConfig,
                            scenarios: [...comparisonConfig.scenarios, 'optimistic']
                          })
                        } else {
                          setComparisonConfig({
                            ...comparisonConfig,
                            scenarios: comparisonConfig.scenarios.filter(s => s !== 'optimistic')
                          })
                        }
                      }}
                    />
                    <span>Optimistic Scenario</span>
                  </label>
                  <label className="selection-item">
                    <input
                      type="checkbox"
                      checked={comparisonConfig.scenarios.includes('pessimistic')}
                      onChange={(e) => {
                        if (e.target.checked) {
                          setComparisonConfig({
                            ...comparisonConfig,
                            scenarios: [...comparisonConfig.scenarios, 'pessimistic']
                          })
                        } else {
                          setComparisonConfig({
                            ...comparisonConfig,
                            scenarios: comparisonConfig.scenarios.filter(s => s !== 'pessimistic')
                          })
                        }
                      }}
                    />
                    <span>Pessimistic Scenario</span>
                  </label>
                </div>
              </div>
            )}

            {/* Indicators Selection */}
            <div className="config-section">
              <h4>Select Indicators</h4>
              <div className="indicator-selection">
                {indicators.map(indicator => (
                  <label key={indicator.code} className="selection-item">
                    <input
                      type="checkbox"
                      checked={comparisonConfig.indicators.includes(indicator.code)}
                      onChange={(e) => {
                        if (e.target.checked) {
                          setComparisonConfig({
                            ...comparisonConfig,
                            indicators: [...comparisonConfig.indicators, indicator.code]
                          })
                        } else {
                          setComparisonConfig({
                            ...comparisonConfig,
                            indicators: comparisonConfig.indicators.filter(i => i !== indicator.code)
                          })
                        }
                      }}
                    />
                    <span>{indicator.name}</span>
                  </label>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Results Panel */}
        {showResults && comparisonResults && (
          <div className="results-panel">
            <div className="results-header">
              <h3>Comparison Results</h3>
              <button
                onClick={() => setShowResults(false)}
                className="btn-icon"
              >
                ×
              </button>
            </div>
            
            <div className="results-content">
              {/* Statistical Summary */}
              <div className="statistical-summary">
                <h4>Statistical Summary</h4>
                <div className="stat-grid">
                  <div className="stat-item">
                    <div className="stat-label">Statistical Significance</div>
                    <div className="stat-value">
                      {comparisonResults.results.statistical_significance < 0.05 ? 'Significant' : 'Not Significant'}
                      <span className="stat-detail">
                        (p = {comparisonResults.results.statistical_significance.toFixed(3)})
                      </span>
                    </div>
                  </div>
                  <div className="stat-item">
                    <div className="stat-label">Effect Size</div>
                    <div className="stat-value">
                      {comparisonResults.results.effect_size > 0.5 ? 'Large' : 
                       comparisonResults.results.effect_size > 0.2 ? 'Medium' : 'Small'}
                      <span className="stat-detail">
                        (d = {comparisonResults.results.effect_size.toFixed(3)})
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Interpretation */}
              <div className="interpretation">
                <h4>Interpretation</h4>
                <p>{comparisonResults.results.interpretation}</p>
              </div>

              {/* Comparison Chart */}
              <div className="comparison-chart">
                <h4>Visualization</h4>
                <div className="chart-container">
                  {renderComparisonChart()}
                </div>
              </div>

              {/* Export Options */}
              <div className="export-options">
                <h4>Export Results</h4>
                <div className="export-buttons">
                  <button className="btn-outline">
                    <Download className="w-4 h-4" />
                    Export as CSV
                  </button>
                  <button className="btn-outline">
                    <Download className="w-4 h-4" />
                    Export as PDF
                  </button>
                  <button className="btn-outline">
                    <Download className="w-4 h-4" />
                    Export Chart
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default ComparisonTools
