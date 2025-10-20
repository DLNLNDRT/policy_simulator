import React, { useState, useEffect } from 'react'
import { 
  TrendingUp, 
  TrendingDown, 
  Minus,
  Calendar,
  BarChart3,
  RefreshCw
} from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { QualityTrend } from '@/types/quality'

interface QualityTrendsProps {
  days?: number
}

const QualityTrends: React.FC<QualityTrendsProps> = ({ days = 30 }) => {
  const [trends, setTrends] = useState<QualityTrend[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [selectedMetric, setSelectedMetric] = useState<'overall_score' | 'completeness_score' | 'validity_score' | 'consistency_score' | 'freshness_score'>('overall_score')

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8005'

  useEffect(() => {
    fetchQualityTrends()
  }, [days])

  const fetchQualityTrends = async () => {
    try {
      setLoading(true)
      setError(null)
      
      const response = await fetch(`${API_BASE_URL}/api/quality/trends?days=${days}`)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      setTrends(data)
    } catch (err: any) {
      console.error('Failed to fetch quality trends:', err)
      setError(err.message || 'Failed to load quality trends')
    } finally {
      setLoading(false)
    }
  }

  const formatChartData = (trends: QualityTrend[]) => {
    return trends.map(trend => ({
      date: new Date(trend.timestamp).toLocaleDateString('en-US', { 
        month: 'short', 
        day: 'numeric' 
      }),
      timestamp: trend.timestamp,
      overall: trend.overall_score,
      completeness: trend.completeness_score,
      validity: trend.validity_score,
      consistency: trend.consistency_score,
      freshness: trend.freshness_score,
      alerts: trend.alert_count
    }))
  }

  const getMetricInfo = (metric: string) => {
    switch (metric) {
      case 'overall_score':
        return { label: 'Overall Quality', color: '#3B82F6' }
      case 'completeness_score':
        return { label: 'Completeness', color: '#10B981' }
      case 'validity_score':
        return { label: 'Validity', color: '#8B5CF6' }
      case 'consistency_score':
        return { label: 'Consistency', color: '#F59E0B' }
      case 'freshness_score':
        return { label: 'Freshness', color: '#EF4444' }
      default:
        return { label: 'Overall Quality', color: '#3B82F6' }
    }
  }

  const calculateTrend = (trends: QualityTrend[], metric: string) => {
    if (trends.length < 2) return 'stable'
    
    const firstValue = trends[0][metric as keyof QualityTrend] as number
    const lastValue = trends[trends.length - 1][metric as keyof QualityTrend] as number
    const change = lastValue - firstValue
    
    if (change > 1) return 'up'
    if (change < -1) return 'down'
    return 'stable'
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
          <span className="text-lg font-medium text-gray-900">Loading Quality Trends...</span>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="card p-6 bg-red-50 border-red-200">
        <div className="flex items-center space-x-3">
          <TrendingDown className="w-6 h-6 text-red-600" />
          <div>
            <h3 className="text-lg font-semibold text-red-900">Error Loading Trends</h3>
            <p className="text-red-700">{error}</p>
            <button
              onClick={fetchQualityTrends}
              className="mt-3 btn-outline text-red-700 border-red-300 hover:bg-red-50"
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    )
  }

  if (trends.length === 0) {
    return (
      <div className="card p-6 text-center">
        <BarChart3 className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-semibold text-gray-900 mb-2">No Trend Data Available</h3>
        <p className="text-gray-600">Unable to load quality trend data for the selected period.</p>
      </div>
    )
  }

  const chartData = formatChartData(trends)
  const currentTrend = calculateTrend(trends, selectedMetric)
  const metricInfo = getMetricInfo(selectedMetric)
  const currentValue = trends[trends.length - 1]?.[selectedMetric as keyof QualityTrend] as number || 0

  return (
    <div className="card">
      <div className="card-header">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
              <BarChart3 className="w-4 h-4 text-purple-600" />
            </div>
            <div>
              <h3 className="card-title">Quality Trends</h3>
              <p className="text-sm text-gray-600">
                Last {days} days
              </p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <select
              value={selectedMetric}
              onChange={(e) => setSelectedMetric(e.target.value as any)}
              className="text-sm border border-gray-300 rounded-md px-2 py-1"
            >
              <option value="overall_score">Overall Quality</option>
              <option value="completeness_score">Completeness</option>
              <option value="validity_score">Validity</option>
              <option value="consistency_score">Consistency</option>
              <option value="freshness_score">Freshness</option>
            </select>
          </div>
        </div>
      </div>
      
      <div className="card-content">
        {/* Trend Summary */}
        <div className="mb-6 p-4 bg-gray-50 rounded-lg">
          <div className="flex items-center justify-between">
            <div>
              <h4 className="text-lg font-semibold text-gray-900">
                {metricInfo.label}
              </h4>
              <p className="text-sm text-gray-600">
                Current: {currentValue.toFixed(1)}/100
              </p>
            </div>
            <div className="flex items-center space-x-2">
              {getTrendIcon(currentTrend)}
              <span className={`text-sm font-medium ${getTrendColor(currentTrend)}`}>
                {currentTrend === 'up' ? 'Improving' : currentTrend === 'down' ? 'Declining' : 'Stable'}
              </span>
            </div>
          </div>
        </div>

        {/* Chart */}
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis 
                dataKey="date" 
                stroke="#6b7280"
                fontSize={12}
                tickLine={false}
                axisLine={false}
              />
              <YAxis 
                stroke="#6b7280"
                fontSize={12}
                tickLine={false}
                axisLine={false}
                domain={[0, 100]}
                tickFormatter={(value) => `${value}%`}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'white',
                  border: '1px solid #e5e7eb',
                  borderRadius: '8px',
                  boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                }}
                labelFormatter={(label) => `Date: ${label}`}
                formatter={(value: any, name: string) => [
                  `${Number(value).toFixed(1)}%`,
                  getMetricInfo(name).label
                ]}
              />
              <Legend />
              <Line
                type="monotone"
                dataKey={selectedMetric.replace('_score', '')}
                stroke={metricInfo.color}
                strokeWidth={2}
                dot={{ fill: metricInfo.color, strokeWidth: 2, r: 4 }}
                activeDot={{ r: 6, stroke: metricInfo.color, strokeWidth: 2 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Additional Metrics */}
        <div className="mt-6 grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center p-3 bg-gray-50 rounded-lg">
            <div className="text-2xl font-bold text-gray-900">
              {trends[trends.length - 1]?.alert_count || 0}
            </div>
            <div className="text-sm text-gray-600">Active Alerts</div>
          </div>
          <div className="text-center p-3 bg-gray-50 rounded-lg">
            <div className="text-2xl font-bold text-gray-900">
              {trends.length}
            </div>
            <div className="text-sm text-gray-600">Data Points</div>
          </div>
          <div className="text-center p-3 bg-gray-50 rounded-lg">
            <div className="text-2xl font-bold text-gray-900">
              {Math.min(...trends.map(t => t.overall_score)).toFixed(1)}
            </div>
            <div className="text-sm text-gray-600">Min Score</div>
          </div>
          <div className="text-center p-3 bg-gray-50 rounded-lg">
            <div className="text-2xl font-bold text-gray-900">
              {Math.max(...trends.map(t => t.overall_score)).toFixed(1)}
            </div>
            <div className="text-sm text-gray-600">Max Score</div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default QualityTrends
