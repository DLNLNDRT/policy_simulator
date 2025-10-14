import React, { useState, useEffect } from 'react'
import { 
  BarChart3, 
  TrendingUp, 
  Activity, 
  FileText, 
  Download,
  RefreshCw,
  Filter,
  Settings,
  Eye,
  Share2
} from 'lucide-react'
import TrendAnalysisCard from './TrendAnalysisCard'
import CorrelationMatrix from './CorrelationMatrix'
import ForecastChart from './ForecastChart'
import StatisticalTestPanel from './StatisticalTestPanel'
import ReportBuilder from './ReportBuilder'
import AdvancedCharts from './AdvancedCharts'
import ComparisonTools from './ComparisonTools'
import { AnalyticsData, DashboardConfig } from '@/types/analytics'

interface AnalyticsDashboardProps {
  initialData?: AnalyticsData
  onDataUpdate?: (data: AnalyticsData) => void
  onExport?: (format: string) => void
}

const AnalyticsDashboard: React.FC<AnalyticsDashboardProps> = ({
  initialData,
  onDataUpdate,
  onExport
}) => {
  const [dashboardData, setDashboardData] = useState<AnalyticsData | null>(initialData || null)
  const [isLoading, setIsLoading] = useState(false)
  const [activeTab, setActiveTab] = useState('overview')
  const [filters, setFilters] = useState({
    countries: [] as string[],
    indicators: [] as string[],
    timePeriod: { start: 2020, end: 2024 }
  })
  const [dashboardConfig, setDashboardConfig] = useState<DashboardConfig>({
    layout: 'grid',
    refreshInterval: 300,
    showMetrics: true,
    showCharts: true,
    showReports: true
  })

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

  // Fetch dashboard data
  const fetchDashboardData = async () => {
    setIsLoading(true)
    try {
      const response = await fetch(`${API_BASE_URL}/api/analytics/dashboard`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: 'Analytics Dashboard',
          components: [
            {
              type: 'trend_analysis',
              title: 'Trend Analysis',
              data_source: 'trends'
            },
            {
              type: 'correlation_matrix',
              title: 'Correlation Matrix',
              data_source: 'correlations'
            },
            {
              type: 'forecast_chart',
              title: 'Forecast Chart',
              data_source: 'forecasts'
            }
          ],
          dashboard_config: dashboardConfig,
          data_sources: {
            trends: { indicators: filters.indicators, countries: filters.countries },
            correlations: { indicators: filters.indicators, countries: filters.countries },
            forecasts: { indicators: filters.indicators, countries: filters.countries }
          }
        })
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      setDashboardData(data.dashboard)
      
      if (onDataUpdate) {
        onDataUpdate(data.dashboard)
      }
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error)
    } finally {
      setIsLoading(false)
    }
  }

  // Load initial data
  useEffect(() => {
    if (!initialData) {
      fetchDashboardData()
    }
  }, [])

  // Auto-refresh dashboard
  useEffect(() => {
    if (dashboardConfig.refreshInterval > 0) {
      const interval = setInterval(fetchDashboardData, dashboardConfig.refreshInterval * 1000)
      return () => clearInterval(interval)
    }
  }, [dashboardConfig.refreshInterval])

  const handleFilterChange = (newFilters: typeof filters) => {
    setFilters(newFilters)
    // Debounce filter updates
    setTimeout(() => {
      fetchDashboardData()
    }, 500)
  }

  const handleExport = async (format: string) => {
    if (!dashboardData) return

    try {
      const response = await fetch(`${API_BASE_URL}/api/analytics/visualizations/export/dashboard/${format}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(dashboardData)
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const blob = await response.blob()
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `analytics-dashboard-${Date.now()}.${format}`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)

      if (onExport) {
        onExport(format)
      }
    } catch (error) {
      console.error('Export failed:', error)
    }
  }

  const tabs = [
    { id: 'overview', label: 'Overview', icon: BarChart3 },
    { id: 'trends', label: 'Trends', icon: TrendingUp },
    { id: 'correlations', label: 'Correlations', icon: Activity },
    { id: 'forecasts', label: 'Forecasts', icon: TrendingUp },
    { id: 'reports', label: 'Reports', icon: FileText },
    { id: 'charts', label: 'Charts', icon: BarChart3 },
    { id: 'comparisons', label: 'Comparisons', icon: Activity }
  ]

  return (
    <div className="analytics-dashboard">
      {/* Header */}
      <div className="dashboard-header">
        <div className="header-content">
          <div className="header-left">
            <h1 className="dashboard-title">Advanced Analytics Dashboard</h1>
            <p className="dashboard-subtitle">
              Comprehensive health policy analytics and insights
            </p>
          </div>
          <div className="header-actions">
            <button
              onClick={() => fetchDashboardData()}
              disabled={isLoading}
              className="btn-outline inline-flex items-center space-x-2"
            >
              <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
              <span>Refresh</span>
            </button>
            <button
              onClick={() => setActiveTab('settings')}
              className="btn-outline inline-flex items-center space-x-2"
            >
              <Settings className="w-4 h-4" />
              <span>Settings</span>
            </button>
            <div className="export-dropdown">
              <button className="btn-primary inline-flex items-center space-x-2">
                <Download className="w-4 h-4" />
                <span>Export</span>
              </button>
              <div className="dropdown-menu">
                <button onClick={() => handleExport('png')}>Export as PNG</button>
                <button onClick={() => handleExport('pdf')}>Export as PDF</button>
                <button onClick={() => handleExport('html')}>Export as HTML</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="dashboard-filters">
        <div className="filter-section">
          <label className="filter-label">
            <Filter className="w-4 h-4" />
            Countries
          </label>
          <select
            multiple
            value={filters.countries}
            onChange={(e) => {
              const selected = Array.from(e.target.selectedOptions, option => option.value)
              handleFilterChange({ ...filters, countries: selected })
            }}
            className="filter-select"
          >
            <option value="PRT">Portugal</option>
            <option value="ESP">Spain</option>
            <option value="SWE">Sweden</option>
            <option value="GRC">Greece</option>
          </select>
        </div>
        <div className="filter-section">
          <label className="filter-label">
            <Filter className="w-4 h-4" />
            Indicators
          </label>
          <select
            multiple
            value={filters.indicators}
            onChange={(e) => {
              const selected = Array.from(e.target.selectedOptions, option => option.value)
              handleFilterChange({ ...filters, indicators: selected })
            }}
            className="filter-select"
          >
            <option value="life_expectancy">Life Expectancy</option>
            <option value="doctor_density">Doctor Density</option>
            <option value="nurse_density">Nurse Density</option>
            <option value="government_spending">Government Spending</option>
          </select>
        </div>
        <div className="filter-section">
          <label className="filter-label">
            <Filter className="w-4 h-4" />
            Time Period
          </label>
          <div className="time-period-inputs">
            <input
              type="number"
              value={filters.timePeriod.start}
              onChange={(e) => handleFilterChange({
                ...filters,
                timePeriod: { ...filters.timePeriod, start: parseInt(e.target.value) }
              })}
              className="filter-input"
              placeholder="Start Year"
            />
            <span>to</span>
            <input
              type="number"
              value={filters.timePeriod.end}
              onChange={(e) => handleFilterChange({
                ...filters,
                timePeriod: { ...filters.timePeriod, end: parseInt(e.target.value) }
              })}
              className="filter-input"
              placeholder="End Year"
            />
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="dashboard-tabs">
        {tabs.map((tab) => {
          const Icon = tab.icon
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`tab-button ${activeTab === tab.id ? 'active' : ''}`}
            >
              <Icon className="w-4 h-4" />
              <span>{tab.label}</span>
            </button>
          )
        })}
      </div>

      {/* Content */}
      <div className="dashboard-content">
        {isLoading && (
          <div className="loading-overlay">
            <div className="loading-spinner" />
            <p>Loading analytics data...</p>
          </div>
        )}

        {activeTab === 'overview' && (
          <div className="overview-grid">
            <div className="metrics-row">
              <div className="metric-card">
                <div className="metric-value">87.3%</div>
                <div className="metric-label">Simulation Accuracy</div>
              </div>
              <div className="metric-card">
                <div className="metric-value">92.1%</div>
                <div className="metric-label">User Adoption</div>
              </div>
              <div className="metric-card">
                <div className="metric-value">$0.08</div>
                <div className="metric-label">Cost per Simulation</div>
              </div>
              <div className="metric-card">
                <div className="metric-value">2.3s</div>
                <div className="metric-label">Avg Response Time</div>
              </div>
            </div>
            <div className="charts-row">
              <div className="chart-container">
                <h3>Trend Analysis</h3>
                <TrendAnalysisCard data={dashboardData?.components?.[0]?.data as any} />
              </div>
              <div className="chart-container">
                <h3>Correlation Matrix</h3>
                <CorrelationMatrix data={dashboardData?.components?.[1]?.data as any} />
              </div>
            </div>
          </div>
        )}

        {activeTab === 'trends' && (
          <div className="trends-section">
            <TrendAnalysisCard 
              data={dashboardData?.components?.[0]?.data as any}
              onAnalyze={(config: any) => {
                // Handle trend analysis
                console.log('Trend analysis requested:', config)
              }}
            />
          </div>
        )}

        {activeTab === 'correlations' && (
          <div className="correlations-section">
            <CorrelationMatrix 
              data={dashboardData?.components?.[1]?.data as any}
              onExport={(format: string) => {
                // Handle correlation export
                console.log('Correlation export requested:', format)
              }}
            />
          </div>
        )}

        {activeTab === 'forecasts' && (
          <div className="forecasts-section">
            <ForecastChart 
              data={dashboardData?.components?.[2]?.data as any}
              onForecast={(config: any) => {
                // Handle forecast generation
                console.log('Forecast requested:', config)
              }}
            />
          </div>
        )}

        {activeTab === 'reports' && (
          <div className="reports-section">
            <ReportBuilder 
              onGenerate={(config) => {
                // Handle report generation
                console.log('Report generation requested:', config)
              }}
            />
          </div>
        )}

        {activeTab === 'charts' && (
          <div className="charts-section">
            <AdvancedCharts 
              onCreate={(config) => {
                // Handle chart creation
                console.log('Chart creation requested:', config)
              }}
            />
          </div>
        )}

        {activeTab === 'comparisons' && (
          <div className="comparisons-section">
            <ComparisonTools 
              onCompare={(config) => {
                // Handle comparison analysis
                console.log('Comparison requested:', config)
              }}
            />
          </div>
        )}

        {activeTab === 'settings' && (
          <div className="settings-section">
            <div className="settings-card">
              <h3>Dashboard Settings</h3>
              <div className="setting-item">
                <label>Refresh Interval (seconds)</label>
                <input
                  type="number"
                  value={dashboardConfig.refreshInterval}
                  onChange={(e) => setDashboardConfig({
                    ...dashboardConfig,
                    refreshInterval: parseInt(e.target.value)
                  })}
                  min="0"
                  max="3600"
                />
              </div>
              <div className="setting-item">
                <label>
                  <input
                    type="checkbox"
                    checked={dashboardConfig.showMetrics}
                    onChange={(e) => setDashboardConfig({
                      ...dashboardConfig,
                      showMetrics: e.target.checked
                    })}
                  />
                  Show Performance Metrics
                </label>
              </div>
              <div className="setting-item">
                <label>
                  <input
                    type="checkbox"
                    checked={dashboardConfig.showCharts}
                    onChange={(e) => setDashboardConfig({
                      ...dashboardConfig,
                      showCharts: e.target.checked
                    })}
                  />
                  Show Interactive Charts
                </label>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default AnalyticsDashboard
