import React, { useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ScatterChart, Scatter, LineChart, Line, Cell } from 'recharts'
import { BarChart3, TrendingUp, Target, Grid3X3, Eye, EyeOff } from 'lucide-react'
import { CountryComparison, CountryRanking, MetricType } from '@/types/benchmark'

interface BenchmarkChartsProps {
  comparison: CountryComparison
  viewMode: 'table' | 'charts'
  className?: string
}

const BenchmarkCharts: React.FC<BenchmarkChartsProps> = ({
  comparison,
  viewMode,
  className = ''
}) => {
  const [visibleCharts, setVisibleCharts] = useState({
    overall: true,
    metrics: true,
    rankings: true,
    scatter: true,
    heatmap: true
  })

  const toggleChart = (chartType: keyof typeof visibleCharts) => {
    setVisibleCharts(prev => ({
      ...prev,
      [chartType]: !prev[chartType]
    }))
  }
  const formatMetricValue = (value: number, metric: string) => {
    if (metric === 'life_expectancy') {
      return `${value.toFixed(1)} years`
    } else if (metric === 'doctor_density' || metric === 'nurse_density') {
      return `${value.toFixed(1)}/1k`
    } else if (metric === 'government_spending') {
      return `${value.toFixed(1)}%`
    }
    return value.toFixed(1)
  }

  const getMetricDisplayName = (metric: string) => {
    return metric
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ')
  }

  // Prepare data for charts
  const prepareBarChartData = () => {
    return comparison.rankings.map(ranking => {
      const data: any = {
        country: ranking.country_name,
        overall_score: ranking.total_score * 100
      }
      
      // Add individual metrics
      ranking.metrics.forEach(metric => {
        data[metric.name] = metric.value
      })
      
      return data
    })
  }

  const prepareScatterData = () => {
    const data: any[] = []
    
    comparison.rankings.forEach(ranking => {
      ranking.metrics.forEach(metric => {
        data.push({
          country: ranking.country_name,
          metric: getMetricDisplayName(metric.name),
          value: metric.value,
          rank: metric.rank,
          percentile: metric.percentile
        })
      })
    })
    
    return data
  }

  const prepareRankingData = () => {
    return comparison.rankings.map(ranking => ({
      country: ranking.country_name,
      overall_rank: ranking.overall_rank,
      total_score: ranking.total_score * 100
    }))
  }

  const prepareHeatmapData = () => {
    const data: any[] = []
    const metrics = comparison.metrics || ['life_expectancy', 'doctor_density', 'nurse_density', 'health_spending']
    
    comparison.rankings.forEach(ranking => {
      const countryData: any = { country: ranking.country_name }
      
      ranking.metrics.forEach(metric => {
        if (metrics.includes(metric.name as MetricType)) {
          // Normalize values to 0-100 scale for heat map
          let normalizedValue = 0
          if (metric.name === 'life_expectancy') {
            normalizedValue = Math.min(100, (metric.value / 100) * 100)
          } else if (metric.name === 'doctor_density' || metric.name === 'nurse_density') {
            normalizedValue = Math.min(100, (metric.value / 10) * 100)
          } else if (metric.name === 'health_spending') {
            normalizedValue = Math.min(100, (metric.value / 15) * 100)
          }
          countryData[metric.name] = normalizedValue
        }
      })
      
      data.push(countryData)
    })
    
    return data
  }

  const getHeatmapColor = (value: number) => {
    // Color scale from red (low) to green (high)
    if (value >= 80) return '#10B981' // Green
    if (value >= 60) return '#F59E0B' // Yellow
    if (value >= 40) return '#F97316' // Orange
    return '#EF4444' // Red
  }

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
          <p className="font-medium text-gray-900">{label}</p>
          {payload.map((entry: any, index: number) => (
            <p key={index} className="text-sm" style={{ color: entry.color }}>
              {entry.dataKey}: {formatMetricValue(entry.value, entry.dataKey)}
            </p>
          ))}
        </div>
      )
    }
    return null
  }

  const barChartData = prepareBarChartData()
  const scatterData = prepareScatterData()
  const rankingData = prepareRankingData()
  const heatmapData = prepareHeatmapData()

  return (
    <div className={`benchmark-charts ${className}`}>
      {/* Chart Controls */}
      <div className="bg-white rounded-lg border border-gray-200 p-4 mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-3">Chart Visibility</h3>
        <div className="flex flex-wrap gap-3">
          {Object.entries(visibleCharts).map(([chartType, isVisible]) => (
            <button
              key={chartType}
              onClick={() => toggleChart(chartType as keyof typeof visibleCharts)}
              className={`inline-flex items-center space-x-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                isVisible
                  ? 'bg-blue-100 text-blue-800'
                  : 'bg-gray-100 text-gray-600'
              }`}
            >
              {isVisible ? <Eye className="w-4 h-4" /> : <EyeOff className="w-4 h-4" />}
              <span className="capitalize">{chartType.replace(/([A-Z])/g, ' $1').trim()}</span>
            </button>
          ))}
        </div>
      </div>

      <div className="space-y-6">
        {/* Overall Performance Chart */}
        {visibleCharts.overall && (
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="mb-4">
            <h3 className="text-lg font-semibold text-gray-900 flex items-center">
              <BarChart3 className="w-5 h-5 mr-2 text-blue-600" />
              Overall Performance Comparison
            </h3>
            <p className="text-sm text-gray-600 mt-1">
              Composite scores across all health indicators
            </p>
          </div>
          
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={rankingData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="country" />
                <YAxis 
                  label={{ value: 'Score', angle: -90, position: 'insideLeft' }}
                  domain={[0, 100]}
                />
                <Tooltip content={<CustomTooltip />} />
                <Legend />
                <Bar 
                  dataKey="total_score" 
                  fill="#3B82F6" 
                  name="Overall Score"
                  radius={[4, 4, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
        )}

        {/* Metric Comparison Chart */}
        {visibleCharts.metrics && (
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="mb-4">
            <h3 className="text-lg font-semibold text-gray-900 flex items-center">
              <TrendingUp className="w-5 h-5 mr-2 text-green-600" />
              Metric Comparison
            </h3>
            <p className="text-sm text-gray-600 mt-1">
              Side-by-side comparison of health indicators
            </p>
          </div>
          
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={barChartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="country" />
                <YAxis />
                <Tooltip content={<CustomTooltip />} />
                <Legend />
                {comparison.metrics.map((metric, index) => (
                  <Bar 
                    key={metric}
                    dataKey={metric}
                    fill={`hsl(${index * 60}, 70%, 50%)`}
                    name={getMetricDisplayName(metric)}
                    radius={[2, 2, 0, 0]}
                  />
                ))}
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
        )}

        {/* Ranking Visualization */}
        {visibleCharts.rankings && (
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="mb-4">
            <h3 className="text-lg font-semibold text-gray-900 flex items-center">
              <Target className="w-5 h-5 mr-2 text-purple-600" />
              Country Rankings
            </h3>
            <p className="text-sm text-gray-600 mt-1">
              Overall ranking with performance scores
            </p>
          </div>
          
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={rankingData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="country" />
                <YAxis 
                  label={{ value: 'Rank', angle: -90, position: 'insideLeft' }}
                  reversed={true}
                  domain={[1, comparison.rankings.length]}
                />
                <Tooltip content={<CustomTooltip />} />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="overall_rank" 
                  stroke="#8B5CF6" 
                  strokeWidth={3}
                  name="Overall Rank"
                  dot={{ fill: '#8B5CF6', strokeWidth: 2, r: 6 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
        )}

        {/* Metric Distribution Scatter Plot */}
        {visibleCharts.scatter && (
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="mb-4">
            <h3 className="text-lg font-semibold text-gray-900 flex items-center">
              <BarChart3 className="w-5 h-5 mr-2 text-orange-600" />
              Metric Distribution
            </h3>
            <p className="text-sm text-gray-600 mt-1">
              Value distribution across countries and metrics
            </p>
          </div>
          
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <ScatterChart data={scatterData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="metric" />
                <YAxis dataKey="value" />
                <Tooltip content={<CustomTooltip />} />
                <Legend />
                <Scatter 
                  dataKey="value" 
                  fill="#F59E0B"
                  name="Metric Value"
                />
              </ScatterChart>
            </ResponsiveContainer>
          </div>
        </div>
        )}

        {/* Heat Map Visualization */}
        {visibleCharts.heatmap && (
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="mb-4">
            <h3 className="text-lg font-semibold text-gray-900 flex items-center">
              <Grid3X3 className="w-5 h-5 mr-2 text-red-600" />
              Health Metrics Heat Map
            </h3>
            <p className="text-sm text-gray-600 mt-1">
              Color-coded performance across all metrics and countries
            </p>
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full border-collapse">
              <thead>
                <tr>
                  <th className="border border-gray-300 p-3 text-left font-medium text-gray-900">Country</th>
                  {comparison.metrics?.map(metric => (
                    <th key={metric} className="border border-gray-300 p-3 text-center font-medium text-gray-900">
                      {getMetricDisplayName(metric)}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {heatmapData.map((countryData, index) => (
                  <tr key={countryData.country}>
                    <td className="border border-gray-300 p-3 font-medium text-gray-900">
                      {countryData.country}
                    </td>
                    {comparison.metrics?.map(metric => {
                      const value = countryData[metric] || 0
                      const color = getHeatmapColor(value)
                      return (
                        <td 
                          key={metric} 
                          className="border border-gray-300 p-3 text-center text-white font-medium"
                          style={{ backgroundColor: color }}
                        >
                          {value.toFixed(0)}
                        </td>
                      )
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          
          {/* Color Legend */}
          <div className="mt-4 flex items-center justify-center space-x-4">
            <span className="text-sm text-gray-600">Performance Scale:</span>
            <div className="flex items-center space-x-2">
              <div className="w-4 h-4 bg-red-500 rounded"></div>
              <span className="text-xs text-gray-600">Low (0-39)</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-4 h-4 bg-orange-500 rounded"></div>
              <span className="text-xs text-gray-600">Medium (40-59)</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-4 h-4 bg-yellow-500 rounded"></div>
              <span className="text-xs text-gray-600">Good (60-79)</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-4 h-4 bg-green-500 rounded"></div>
              <span className="text-xs text-gray-600">Excellent (80-100)</span>
            </div>
          </div>
        </div>
        )}
      </div>
    </div>
  )
}

export default BenchmarkCharts
