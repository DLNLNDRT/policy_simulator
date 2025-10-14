import React, { useState, useEffect } from 'react'
import { 
  Shield, 
  AlertTriangle, 
  CheckCircle, 
  TrendingUp, 
  TrendingDown, 
  Minus,
  RefreshCw,
  Download,
  Eye,
  Clock,
  Database,
  BarChart3
} from 'lucide-react'
import QualityScoreCard from './QualityScoreCard'
import QualityAlerts from './QualityAlerts'
import QualityTrends from './QualityTrends'
import DataSources from './DataSources'
import { QualityOverview, QualityAlert as QualityAlertType } from '@/types/quality'

interface QualityDashboardProps {
  onRefresh?: () => void
  onExport?: () => void
}

const QualityDashboard: React.FC<QualityDashboardProps> = ({
  onRefresh,
  onExport
}) => {
  const [overview, setOverview] = useState<QualityOverview | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [lastRefresh, setLastRefresh] = useState<Date>(new Date())

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

  useEffect(() => {
    fetchQualityOverview()
  }, [])

  const fetchQualityOverview = async () => {
    try {
      setLoading(true)
      setError(null)
      
      const response = await fetch(`${API_BASE_URL}/api/quality/overview`)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      setOverview(data)
      setLastRefresh(new Date())
    } catch (err: any) {
      console.error('Failed to fetch quality overview:', err)
      setError(err.message || 'Failed to load quality overview')
    } finally {
      setLoading(false)
    }
  }

  const handleRefresh = () => {
    fetchQualityOverview()
    if (onRefresh) {
      onRefresh()
    }
  }

  const handleExport = () => {
    if (onExport) {
      onExport()
    }
  }

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'up':
        return <TrendingUp className="w-4 h-4 text-green-600" />
      case 'down':
        return <TrendingDown className="w-4 h-4 text-red-600" />
      default:
        return <Minus className="w-4 h-4 text-gray-600" />
    }
  }

  const getTrendColor = (trend: string) => {
    switch (trend) {
      case 'up':
        return 'text-green-600'
      case 'down':
        return 'text-red-600'
      default:
        return 'text-gray-600'
    }
  }

  if (loading) {
    return (
      <div className="card p-8 text-center">
        <div className="flex items-center justify-center space-x-3">
          <RefreshCw className="w-6 h-6 text-primary-500 animate-spin" />
          <span className="text-lg font-medium text-gray-900">Loading Quality Dashboard...</span>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="card p-6 bg-red-50 border-red-200">
        <div className="flex items-center space-x-3">
          <AlertTriangle className="w-6 h-6 text-red-600" />
          <div>
            <h3 className="text-lg font-semibold text-red-900">Error Loading Quality Data</h3>
            <p className="text-red-700">{error}</p>
            <button
              onClick={handleRefresh}
              className="mt-3 btn-outline text-red-700 border-red-300 hover:bg-red-50"
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    )
  }

  if (!overview) {
    return (
      <div className="card p-6 text-center">
        <Database className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-semibold text-gray-900 mb-2">No Quality Data Available</h3>
        <p className="text-gray-600">Unable to load quality overview data.</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
            <Shield className="w-5 h-5 text-blue-600" />
          </div>
          <div>
            <h2 className="text-xl font-semibold text-gray-900">Data Quality Dashboard</h2>
            <p className="text-sm text-gray-600">
              Last updated: {lastRefresh.toLocaleTimeString()}
            </p>
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          <button
            onClick={handleRefresh}
            className="btn-outline inline-flex items-center space-x-2"
            disabled={loading}
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            <span>Refresh</span>
          </button>
          
          <button
            onClick={handleExport}
            className="btn-outline inline-flex items-center space-x-2"
          >
            <Download className="w-4 h-4" />
            <span>Export</span>
          </button>
        </div>
      </div>

      {/* Overall Quality Score */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">Overall Quality Score</h3>
          <div className="flex items-center space-x-2">
            {getTrendIcon(overview.trend)}
            <span className={`text-sm font-medium ${getTrendColor(overview.trend)}`}>
              {overview.trend === 'up' ? 'Improving' : overview.trend === 'down' ? 'Declining' : 'Stable'}
            </span>
          </div>
        </div>
        
        <div className="card-content">
          <div className="text-center mb-6">
            <div className="inline-flex items-center justify-center w-24 h-24 rounded-full bg-gradient-to-r from-blue-500 to-green-500 text-white mb-4">
              <span className="text-3xl font-bold">{overview.overall_score.toFixed(1)}</span>
            </div>
            <p className="text-2xl font-bold text-gray-900 mb-2">
              {overview.overall_score.toFixed(1)}/100
            </p>
            <p className="text-gray-600">Data Quality Score</p>
          </div>

          {/* Quality Breakdown */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <QualityScoreCard
              title="Completeness"
              score={overview.completeness_score}
              icon={<CheckCircle className="w-5 h-5" />}
              color="green"
            />
            <QualityScoreCard
              title="Validity"
              score={overview.validity_score}
              icon={<Shield className="w-5 h-5" />}
              color="blue"
            />
            <QualityScoreCard
              title="Consistency"
              score={overview.consistency_score}
              icon={<BarChart3 className="w-5 h-5" />}
              color="purple"
            />
            <QualityScoreCard
              title="Freshness"
              score={overview.freshness_score}
              icon={<Clock className="w-5 h-5" />}
              color="orange"
            />
          </div>
        </div>
      </div>

      {/* Quality Alerts */}
      {overview.alerts && overview.alerts.length > 0 && (
        <QualityAlerts alerts={overview.alerts} />
      )}

      {/* Quality Trends */}
      <QualityTrends />

      {/* Data Sources */}
      <DataSources sources={overview.data_sources} />
    </div>
  )
}

export default QualityDashboard
