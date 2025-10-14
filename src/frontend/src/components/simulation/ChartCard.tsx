import React from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts'
import { TrendingUp, TrendingDown } from 'lucide-react'

interface ChartCardProps {
  baseline: number
  predicted: number
  confidenceInterval: [number, number]
}

const ChartCard: React.FC<ChartCardProps> = ({ baseline, predicted, confidenceInterval }) => {
  const data = [
    {
      name: 'Baseline',
      value: baseline,
      type: 'baseline'
    },
    {
      name: 'Predicted',
      value: predicted,
      type: 'predicted'
    }
  ]

  const change = predicted - baseline
  const isPositive = change > 0

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload
      return (
        <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
          <p className="font-medium text-gray-900">{label}</p>
          <p className="text-sm text-gray-600">
            Life Expectancy: <span className="font-medium">{data.value.toFixed(1)} years</span>
          </p>
          {data.type === 'predicted' && (
            <p className="text-sm text-gray-600">
              Change: <span className={`font-medium ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
                {isPositive ? '+' : ''}{change.toFixed(2)} years
              </span>
            </p>
          )}
        </div>
      )
    }
    return null
  }

  return (
    <div className="card">
      <div className="card-header">
        <h2 className="card-title">Life Expectancy Comparison</h2>
        <p className="card-description">
          Baseline vs. predicted outcomes
        </p>
      </div>
      
      <div className="card-content">
        {/* Summary Stats */}
        <div className="grid grid-cols-3 gap-4 mb-6">
          <div className="text-center">
            <p className="text-2xl font-bold text-gray-900">{baseline.toFixed(1)}</p>
            <p className="text-sm text-gray-500">Baseline (years)</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-gray-900">{predicted.toFixed(1)}</p>
            <p className="text-sm text-gray-500">Predicted (years)</p>
          </div>
          <div className="text-center">
            <div className={`inline-flex items-center space-x-1 ${
              isPositive ? 'text-green-600' : 'text-red-600'
            }`}>
              {isPositive ? (
                <TrendingUp className="w-4 h-4" />
              ) : (
                <TrendingDown className="w-4 h-4" />
              )}
              <span className="text-2xl font-bold">
                {isPositive ? '+' : ''}{change.toFixed(2)}
              </span>
            </div>
            <p className="text-sm text-gray-500">Change (years)</p>
          </div>
        </div>

        {/* Chart */}
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis 
                dataKey="name" 
                tick={{ fontSize: 12 }}
                axisLine={false}
                tickLine={false}
              />
              <YAxis 
                domain={[Math.min(baseline, predicted) - 2, Math.max(baseline, predicted) + 2]}
                tick={{ fontSize: 12 }}
                axisLine={false}
                tickLine={false}
                tickFormatter={(value) => `${value.toFixed(1)}`}
              />
              <Tooltip content={<CustomTooltip />} />
              <Bar 
                dataKey="value" 
                fill="#3b82f6"
                radius={[4, 4, 0, 0]}
                maxBarSize={60}
              />
              <ReferenceLine 
                y={baseline} 
                stroke="#6b7280" 
                strokeDasharray="5 5"
                label={{ value: "Baseline", position: "top" }}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Confidence Interval Info */}
        <div className="mt-4 p-3 bg-gray-50 rounded-lg">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-gray-700">95% Confidence Interval</span>
            <span className="text-sm text-gray-600">
              {confidenceInterval[0].toFixed(2)} - {confidenceInterval[1].toFixed(2)} years
            </span>
          </div>
          <div className="mt-2 text-xs text-gray-500">
            The predicted value has a 95% probability of falling within this range
          </div>
        </div>
      </div>
    </div>
  )
}

export default ChartCard
