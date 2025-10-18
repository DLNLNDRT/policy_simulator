import React, { useState, useEffect, useCallback } from 'react'
import { BarChart3, AlertTriangle, Users, TrendingUp, Play, RefreshCw, Settings, Download, FileText, Image, Table } from 'lucide-react'
import CountrySelector from './CountrySelector'
import MetricComparison from './MetricComparison'
import AnomalyAlerts from './AnomalyAlerts'

interface Country {
  code: string
  name: string
}

interface HealthMetric {
  name: string
  value: number
  unit: string
  rank: number
  percentile: number
  trend: string
  anomaly: boolean
  baseline_year: number
}

interface CountryRanking {
  country_code: string
  country_name: string
  overall_rank: number
  metrics: HealthMetric[]
  total_score: number
}

interface AnomalyAlert {
  country: string
  metric: string
  severity: string
  description: string
  confidence: number
  recommendation: string
  detected_at: string
}

interface ComparisonResult {
  countries: string[]
  metrics: string[]
  year: number
  rankings: CountryRanking[]
  anomalies: AnomalyAlert[]
  peer_groups: any[]
  summary: {
    total_countries: number
    total_anomalies: number
    high_severity_anomalies: number
    peer_groups: number
    best_performer: string
    worst_performer: string
    average_score: number
  }
  generated_at: string
}

const BenchmarkDashboard: React.FC = () => {
  const [countries, setCountries] = useState<Country[]>([])
  const [selectedCountries, setSelectedCountries] = useState<string[]>([])
  const [selectedMetrics, setSelectedMetrics] = useState<string[]>([
    'life_expectancy',
    'doctor_density',
    'nurse_density',
    'health_spending'
  ])
  const [comparisonResult, setComparisonResult] = useState<ComparisonResult | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || ''

  // Fetch available countries
  useEffect(() => {
    const fetchCountries = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/benchmarks/countries`)
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        const data: Country[] = await response.json()
        setCountries(data)
        // Auto-select first 3 countries for demo
        if (data.length >= 3) {
          setSelectedCountries(data.slice(0, 3).map(c => c.code))
        }
      } catch (err) {
        console.error('Failed to fetch countries:', err)
        setError('Failed to load available countries.')
      }
    }
    fetchCountries()
  }, [API_BASE_URL])

  const runComparison = useCallback(async () => {
    if (selectedCountries.length < 2) {
      setError('Please select at least 2 countries for comparison.')
      return
    }

    setIsLoading(true)
    setError(null)
    setComparisonResult(null)

    try {
      const response = await fetch(`${API_BASE_URL}/api/benchmarks/compare`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          countries: selectedCountries,
          metrics: selectedMetrics,
          year: 2022,
          include_anomalies: true,
          include_peers: true
        }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
      }

      const data: ComparisonResult = await response.json()
      setComparisonResult(data)
    } catch (err: any) {
      console.error('Comparison failed:', err)
      setError(err.message || 'An unknown error occurred during comparison.')
    } finally {
      setIsLoading(false)
    }
  }, [selectedCountries, selectedMetrics, API_BASE_URL])

  const handleCountrySelectionChange = (countries: string[]) => {
    setSelectedCountries(countries)
  }

  const handleMetricToggle = (metric: string) => {
    setSelectedMetrics(prev => 
      prev.includes(metric) 
        ? prev.filter(m => m !== metric)
        : [...prev, metric]
    )
  }

  const handleExport = useCallback(async (format: 'csv' | 'pdf' | 'png') => {
    if (!comparisonResult) {
      setError('No comparison data available for export')
      return
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/benchmarks/export/${format}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          comparison_data: comparisonResult,
          format: format,
          include_charts: true,
          include_tables: true,
          include_anomalies: true
        }),
      })

      if (!response.ok) {
        throw new Error(`Export failed: ${response.status}`)
      }

      if (format === 'csv') {
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `benchmark_comparison.${format}`
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
        window.URL.revokeObjectURL(url)
      } else if (format === 'pdf') {
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `benchmark_comparison.html`
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
        window.URL.revokeObjectURL(url)
      } else if (format === 'png') {
        const data = await response.json()
        // For PNG, we'd typically handle the base64 image data
        console.log('PNG export data:', data)
        alert('PNG export feature - chart data prepared for visualization')
      }
    } catch (err: any) {
      console.error('Export failed:', err)
      setError(err.message || 'Export failed')
    }
  }, [comparisonResult, API_BASE_URL])

  const availableMetrics = [
    { key: 'life_expectancy', label: 'Life Expectancy' },
    { key: 'doctor_density', label: 'Doctor Density' },
    { key: 'nurse_density', label: 'Nurse Density' },
    { key: 'health_spending', label: 'Health Spending' }
  ]

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4 flex items-center justify-center">
          <BarChart3 className="w-8 h-8 mr-3 text-blue-600" />
          Health Benchmark Dashboard
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          Compare countries across health indicators, detect anomalies, and analyze peer group performance
        </p>
      </div>

      {/* Configuration Panel */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Country Selection */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <CountrySelector
              countries={countries}
              selectedCountries={selectedCountries}
              onSelectionChange={handleCountrySelectionChange}
              maxSelection={5}
            />
          </div>
        </div>

        {/* Metrics Selection */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <Settings className="w-5 h-5 mr-2 text-green-600" />
              Select Metrics
            </h3>
            <div className="space-y-3">
              {availableMetrics.map((metric) => (
                <label key={metric.key} className="flex items-center">
                  <input
                    type="checkbox"
                    checked={selectedMetrics.includes(metric.key)}
                    onChange={() => handleMetricToggle(metric.key)}
                    className="rounded border-gray-300 text-green-600 focus:ring-green-500"
                  />
                  <span className="ml-2 text-sm text-gray-700">{metric.label}</span>
                </label>
              ))}
            </div>
          </div>
        </div>

        {/* Run Comparison */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <Play className="w-5 h-5 mr-2 text-purple-600" />
              Run Comparison
            </h3>
            <div className="space-y-4">
              <div className="text-sm text-gray-600">
                <p>Selected: {selectedCountries.length} countries</p>
                <p>Metrics: {selectedMetrics.length} indicators</p>
              </div>
              <button
                onClick={runComparison}
                disabled={isLoading || selectedCountries.length < 2}
                className="w-full btn-primary inline-flex items-center justify-center space-x-2"
              >
                {isLoading ? (
                  <>
                    <RefreshCw className="w-4 h-4 animate-spin" />
                    <span>Analyzing...</span>
                  </>
                ) : (
                  <>
                    <Play className="w-4 h-4" />
                    <span>Run Comparison</span>
                  </>
                )}
              </button>
              {selectedCountries.length < 2 && (
                <p className="text-sm text-gray-500 text-center">
                  Select at least 2 countries to run comparison
                </p>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-center space-x-3">
          <AlertTriangle className="w-5 h-5 text-red-600" />
          <span className="text-red-800">{error}</span>
        </div>
      )}

      {/* Results */}
      {comparisonResult && (
        <div className="space-y-6">
          {/* Summary Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="bg-white rounded-lg border border-gray-200 p-4">
              <div className="flex items-center space-x-2 mb-2">
                <Users className="w-5 h-5 text-blue-600" />
                <span className="text-sm font-medium text-gray-900">Countries</span>
              </div>
              <div className="text-2xl font-bold text-gray-900">{comparisonResult.summary.total_countries}</div>
            </div>
            <div className="bg-white rounded-lg border border-gray-200 p-4">
              <div className="flex items-center space-x-2 mb-2">
                <AlertTriangle className="w-5 h-5 text-orange-600" />
                <span className="text-sm font-medium text-gray-900">Anomalies</span>
              </div>
              <div className="text-2xl font-bold text-gray-900">{comparisonResult.summary.total_anomalies}</div>
            </div>
            <div className="bg-white rounded-lg border border-gray-200 p-4">
              <div className="flex items-center space-x-2 mb-2">
                <TrendingUp className="w-5 h-5 text-green-600" />
                <span className="text-sm font-medium text-gray-900">Best Performer</span>
              </div>
              <div className="text-lg font-semibold text-gray-900">{comparisonResult.summary.best_performer}</div>
            </div>
            <div className="bg-white rounded-lg border border-gray-200 p-4">
              <div className="flex items-center space-x-2 mb-2">
                <BarChart3 className="w-5 h-5 text-purple-600" />
                <span className="text-sm font-medium text-gray-900">Avg Score</span>
              </div>
              <div className="text-2xl font-bold text-gray-900">
                {(comparisonResult.summary.average_score * 100).toFixed(0)}%
              </div>
            </div>
          </div>

          {/* Metric Comparison */}
          <MetricComparison
            rankings={comparisonResult.rankings}
            selectedMetrics={selectedMetrics}
          />

          {/* Anomaly Alerts */}
          <AnomalyAlerts anomalies={comparisonResult.anomalies} />

          {/* Export Section */}
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <Download className="w-5 h-5 mr-2 text-green-600" />
              Export Results
            </h3>
            <p className="text-gray-600 mb-4">
              Download your benchmark comparison in various formats for sharing and analysis.
            </p>
            <div className="flex flex-wrap gap-3">
              <button
                onClick={() => handleExport('csv')}
                className="btn-outline inline-flex items-center space-x-2"
              >
                <Table className="w-4 h-4" />
                <span>CSV Data</span>
              </button>
              <button
                onClick={() => handleExport('pdf')}
                className="btn-outline inline-flex items-center space-x-2"
              >
                <FileText className="w-4 h-4" />
                <span>PDF Report</span>
              </button>
              <button
                onClick={() => handleExport('png')}
                className="btn-outline inline-flex items-center space-x-2"
              >
                <Image className="w-4 h-4" />
                <span>PNG Chart</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Loading State */}
      {isLoading && (
        <div className="bg-white rounded-lg border border-gray-200 p-8 text-center">
          <RefreshCw className="w-16 h-16 text-blue-600 animate-spin mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            Analyzing Health Data...
          </h3>
          <p className="text-gray-600">
            Comparing countries and detecting anomalies. This may take a few moments.
          </p>
        </div>
      )}

      {/* Info Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="flex items-center space-x-3 mb-4">
            <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
              <BarChart3 className="w-5 h-5 text-blue-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900">Benchmark Analysis</h3>
          </div>
          <p className="text-gray-600 text-sm">
            Compare countries across multiple health indicators with statistical ranking and percentile analysis.
          </p>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="flex items-center space-x-3 mb-4">
            <div className="w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center">
              <AlertTriangle className="w-5 h-5 text-orange-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900">Anomaly Detection</h3>
          </div>
          <p className="text-gray-600 text-sm">
            Automatically detect statistical anomalies in health data with confidence scoring and recommendations.
          </p>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="flex items-center space-x-3 mb-4">
            <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
              <Users className="w-5 h-5 text-green-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900">Peer Group Analysis</h3>
          </div>
          <p className="text-gray-600 text-sm">
            Identify similar countries and analyze performance patterns within peer groups for better insights.
          </p>
        </div>
      </div>
    </div>
  )
}

export default BenchmarkDashboard