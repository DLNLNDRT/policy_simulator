import React from 'react'
import { BarChart3, TrendingUp, TrendingDown, Minus, Award, AlertTriangle } from 'lucide-react'

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

interface MetricComparisonProps {
  rankings: CountryRanking[]
  selectedMetrics: string[]
}

const MetricComparison: React.FC<MetricComparisonProps> = ({
  rankings,
  selectedMetrics
}) => {
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

  const getRankColor = (rank: number, total: number) => {
    const percentage = (rank / total) * 100
    if (percentage <= 25) return 'text-green-600 bg-green-100'
    if (percentage <= 50) return 'text-blue-600 bg-blue-100'
    if (percentage <= 75) return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
  }

  const getScoreColor = (score: number) => {
    if (score >= 0.8) return 'text-green-600'
    if (score >= 0.6) return 'text-blue-600'
    if (score >= 0.4) return 'text-yellow-600'
    return 'text-red-600'
  }

  const formatValue = (value: number, unit: string) => {
    if (unit === 'years') return `${value.toFixed(1)} ${unit}`
    if (unit === '% of GDP') return `${value.toFixed(1)}%`
    if (unit.includes('per 1,000')) return `${value.toFixed(1)}/1k`
    return `${value.toFixed(2)} ${unit}`
  }

  const getMetricDisplayName = (metricName: string) => {
    const names: Record<string, string> = {
      'life_expectancy': 'Life Expectancy',
      'doctor_density': 'Doctor Density',
      'nurse_density': 'Nurse Density',
      'health_spending': 'Health Spending'
    }
    return names[metricName] || metricName.replace('_', ' ').toUpperCase()
  }

  return (
    <div className="space-y-6">
      {/* Overall Rankings */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <Award className="w-5 h-5 mr-2 text-yellow-600" />
          Overall Rankings
        </h3>
        
        <div className="space-y-3">
          {rankings.map((ranking, index) => (
            <div key={ranking.country_code} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
              <div className="flex items-center space-x-4">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
                  index === 0 ? 'bg-yellow-100 text-yellow-800' :
                  index === 1 ? 'bg-gray-100 text-gray-800' :
                  index === 2 ? 'bg-orange-100 text-orange-800' :
                  'bg-gray-50 text-gray-600'
                }`}>
                  {ranking.overall_rank}
                </div>
                <div>
                  <div className="font-medium text-gray-900">{ranking.country_name}</div>
                  <div className="text-sm text-gray-500">{ranking.country_code}</div>
                </div>
              </div>
              <div className="flex items-center space-x-4">
                <div className="text-right">
                  <div className={`text-lg font-semibold ${getScoreColor(ranking.total_score)}`}>
                    {(ranking.total_score * 100).toFixed(0)}%
                  </div>
                  <div className="text-sm text-gray-500">Overall Score</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Metric Comparison Table */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <BarChart3 className="w-5 h-5 mr-2 text-blue-600" />
          Metric Comparison
        </h3>
        
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Country
                </th>
                {selectedMetrics.map((metric) => (
                  <th key={metric} className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    {getMetricDisplayName(metric)}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {rankings.map((ranking) => (
                <tr key={ranking.country_code}>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="text-sm font-medium text-gray-900">
                        {ranking.country_name}
                      </div>
                    </div>
                  </td>
                  {selectedMetrics.map((metricName) => {
                    const metric = ranking.metrics.find(m => m.name === metricName)
                    if (!metric) return <td key={metricName} className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">-</td>
                    
                    return (
                      <td key={metricName} className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center space-x-2">
                          <div className="text-sm font-medium text-gray-900">
                            {formatValue(metric.value, metric.unit)}
                          </div>
                          {metric.anomaly && (
                            <AlertTriangle className="w-4 h-4 text-red-500" />
                          )}
                        </div>
                        <div className="flex items-center space-x-2 mt-1">
                          <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getRankColor(metric.rank, rankings.length)}`}>
                            Rank {metric.rank}
                          </span>
                          <div className="flex items-center space-x-1">
                            {getTrendIcon(metric.trend)}
                            <span className="text-xs text-gray-500">
                              {metric.percentile.toFixed(0)}th percentile
                            </span>
                          </div>
                        </div>
                      </td>
                    )
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Summary Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <div className="flex items-center space-x-2 mb-2">
            <Award className="w-5 h-5 text-green-600" />
            <span className="text-sm font-medium text-gray-900">Best Performer</span>
          </div>
          <div className="text-lg font-semibold text-gray-900">
            {rankings[0]?.country_name || 'N/A'}
          </div>
          <div className="text-sm text-gray-500">
            Score: {((rankings[0]?.total_score || 0) * 100).toFixed(0)}%
          </div>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <div className="flex items-center space-x-2 mb-2">
            <TrendingDown className="w-5 h-5 text-red-600" />
            <span className="text-sm font-medium text-gray-900">Needs Improvement</span>
          </div>
          <div className="text-lg font-semibold text-gray-900">
            {rankings[rankings.length - 1]?.country_name || 'N/A'}
          </div>
          <div className="text-sm text-gray-500">
            Score: {((rankings[rankings.length - 1]?.total_score || 0) * 100).toFixed(0)}%
          </div>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <div className="flex items-center space-x-2 mb-2">
            <BarChart3 className="w-5 h-5 text-blue-600" />
            <span className="text-sm font-medium text-gray-900">Average Score</span>
          </div>
          <div className="text-lg font-semibold text-gray-900">
            {(rankings.reduce((sum, r) => sum + r.total_score, 0) / rankings.length * 100).toFixed(0)}%
          </div>
          <div className="text-sm text-gray-500">
            Across {rankings.length} countries
          </div>
        </div>
      </div>
    </div>
  )
}

export default MetricComparison