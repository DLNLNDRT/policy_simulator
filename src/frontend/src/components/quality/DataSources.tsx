import React, { useState, useEffect } from 'react'
import { 
  Database, 
  ExternalLink, 
  Clock, 
  Shield, 
  CheckCircle,
  AlertTriangle,
  RefreshCw,
  Eye,
  Download
} from 'lucide-react'
import { DataSource as DataSourceType } from '@/types/quality'

interface DataSourcesProps {
  sources?: Record<string, any>
  onViewProvenance?: (sourceId: string) => void
  onExportProvenance?: (sourceId: string) => void
}

const DataSources: React.FC<DataSourcesProps> = ({
  sources = {},
  onViewProvenance,
  onExportProvenance
}) => {
  const [sourcesData, setSourcesData] = useState<DataSourceType[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8005'

  useEffect(() => {
    fetchDataSources()
  }, [])

  const fetchDataSources = async () => {
    try {
      setLoading(true)
      setError(null)
      
      const response = await fetch(`${API_BASE_URL}/api/quality/sources`)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      setSourcesData(data || [])
    } catch (err: any) {
      console.error('Failed to fetch data sources:', err)
      setError(err.message || 'Failed to load data sources')
    } finally {
      setLoading(false)
    }
  }

  const getSourceIcon = (sourceId: string) => {
    switch (sourceId) {
      case 'who_gho':
        return <Shield className="w-5 h-5 text-blue-600" />
      case 'world_bank':
        return <Database className="w-5 h-5 text-green-600" />
      case 'oecd_health':
        return <CheckCircle className="w-5 h-5 text-purple-600" />
      default:
        return <Database className="w-5 h-5 text-gray-600" />
    }
  }

  const getSourceColor = (sourceId: string) => {
    switch (sourceId) {
      case 'who_gho':
        return 'bg-blue-50 border-blue-200'
      case 'world_bank':
        return 'bg-green-50 border-green-200'
      case 'oecd_health':
        return 'bg-purple-50 border-purple-200'
      default:
        return 'bg-gray-50 border-gray-200'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active':
        return <CheckCircle className="w-4 h-4 text-green-600" />
      case 'warning':
        return <AlertTriangle className="w-4 h-4 text-yellow-600" />
      case 'error':
        return <AlertTriangle className="w-4 h-4 text-red-600" />
      default:
        return <Clock className="w-4 h-4 text-gray-600" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'text-green-600 bg-green-100'
      case 'warning':
        return 'text-yellow-600 bg-yellow-100'
      case 'error':
        return 'text-red-600 bg-red-100'
      default:
        return 'text-gray-600 bg-gray-100'
    }
  }

  const formatLastUpdated = (lastUpdated: string) => {
    const date = new Date(lastUpdated)
    const now = new Date()
    const diffInHours = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60))
    
    if (diffInHours < 1) {
      return 'Just now'
    } else if (diffInHours < 24) {
      return `${diffInHours} hours ago`
    } else {
      const diffInDays = Math.floor(diffInHours / 24)
      return `${diffInDays} days ago`
    }
  }

  const getReliabilityColor = (score: number) => {
    if (score >= 0.9) return 'text-green-600'
    if (score >= 0.8) return 'text-yellow-600'
    return 'text-red-600'
  }

  if (loading) {
    return (
      <div className="card p-8 text-center">
        <div className="flex items-center justify-center space-x-3">
          <RefreshCw className="w-6 h-6 text-primary-500 animate-spin" />
          <span className="text-lg font-medium text-gray-900">Loading Data Sources...</span>
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
            <h3 className="text-lg font-semibold text-red-900">Error Loading Data Sources</h3>
            <p className="text-red-700">{error}</p>
            <button
              onClick={fetchDataSources}
              className="mt-3 btn-outline text-red-700 border-red-300 hover:bg-red-50"
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    )
  }

  if (sourcesData.length === 0) {
    return (
      <div className="card p-6 text-center">
        <Database className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-semibold text-gray-900 mb-2">No Data Sources Available</h3>
        <p className="text-gray-600">Unable to load data source information.</p>
      </div>
    )
  }

  return (
    <div className="card">
      <div className="card-header">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-indigo-100 rounded-lg flex items-center justify-center">
              <Database className="w-4 h-4 text-indigo-600" />
            </div>
            <div>
              <h3 className="card-title">Data Sources & Provenance</h3>
              <p className="text-sm text-gray-600">
                {sourcesData.length} data sources
              </p>
            </div>
          </div>
          
          <button
            onClick={fetchDataSources}
            className="btn-outline inline-flex items-center space-x-2"
            disabled={loading}
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            <span>Refresh</span>
          </button>
        </div>
      </div>
      
      <div className="card-content">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {sourcesData.map((source) => (
            <div
              key={source.source_id}
              className={`p-4 rounded-lg border ${getSourceColor(source.source_id)}`}
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center space-x-3">
                  <div className="flex-shrink-0">
                    {getSourceIcon(source.source_id)}
                  </div>
                  <div className="flex-1 min-w-0">
                    <h4 className="text-sm font-semibold text-gray-900 truncate">
                      {source.name}
                    </h4>
                    <p className="text-xs text-gray-600">
                      {source.description}
                    </p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-1">
                  <CheckCircle className="w-4 h-4 text-green-600" />
                  <span className="text-xs px-2 py-1 rounded-full font-medium text-green-600 bg-green-100">
                    Active
                  </span>
                </div>
              </div>
              
              <div className="space-y-2 mb-4">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600">Quality Score:</span>
                  <span className="font-medium text-green-600">
                    {source.quality_score}%
                  </span>
                </div>
                
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600">Last Updated:</span>
                  <span className="font-medium text-gray-900">
                    {formatLastUpdated(source.last_updated)}
                  </span>
                </div>
                
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600">Coverage:</span>
                  <span className="font-medium text-gray-900">
                    {source.coverage}
                  </span>
                </div>
              </div>
              
              <div className="flex items-center justify-between pt-3 border-t border-opacity-20">
                <a
                  href={source.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center space-x-1 text-xs text-gray-600 hover:text-gray-900 transition-colors"
                >
                  <ExternalLink className="w-3 h-3" />
                  <span>Visit Source</span>
                </a>
                
                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => onViewProvenance?.(source.source_id)}
                    className="inline-flex items-center space-x-1 text-xs text-gray-600 hover:text-gray-900 transition-colors"
                  >
                    <Eye className="w-3 h-3" />
                    <span>View</span>
                  </button>
                  
                  <button
                    onClick={() => onExportProvenance?.(source.source_id)}
                    className="inline-flex items-center space-x-1 text-xs text-gray-600 hover:text-gray-900 transition-colors"
                  >
                    <Download className="w-3 h-3" />
                    <span>Export</span>
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
        
        {/* Summary Statistics */}
        <div className="mt-6 pt-6 border-t border-gray-200">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center p-3 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-gray-900">
                {sourcesData.length}
              </div>
              <div className="text-sm text-gray-600">Total Sources</div>
            </div>
            <div className="text-center p-3 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-gray-900">
                {sourcesData.length}
              </div>
              <div className="text-sm text-gray-600">Active Sources</div>
            </div>
            <div className="text-center p-3 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-gray-900">
                {sourcesData.length}
              </div>
              <div className="text-sm text-gray-600">Coverage Areas</div>
            </div>
            <div className="text-center p-3 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-gray-900">
                {(sourcesData.reduce((sum, s) => sum + s.quality_score, 0) / sourcesData.length).toFixed(1)}%
              </div>
              <div className="text-sm text-gray-600">Avg Quality</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default DataSources
