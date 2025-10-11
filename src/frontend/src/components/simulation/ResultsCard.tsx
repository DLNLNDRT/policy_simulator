import React from 'react'
import { TrendingUp, TrendingDown, Clock, DollarSign, Target } from 'lucide-react'

interface SimulationResult {
  predictedChange: number
  confidenceInterval: [number, number]
  narrative: string
  disclaimers: string[]
  citations: string[]
  responseTime: number
  cost: number
}

interface ResultsCardProps {
  results: SimulationResult
}

const ResultsCard: React.FC<ResultsCardProps> = ({ results }) => {
  const isPositive = results.predictedChange > 0
  const confidenceWidth = results.confidenceInterval[1] - results.confidenceInterval[0]

  return (
    <div className="card">
      <div className="card-header">
        <h2 className="card-title">Simulation Results</h2>
        <p className="card-description">
          Predicted impact on life expectancy
        </p>
      </div>
      
      <div className="card-content">
        {/* Main Prediction */}
        <div className="text-center mb-6">
          <div className={`inline-flex items-center space-x-2 px-4 py-2 rounded-lg mb-4 ${
            isPositive ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
          }`}>
            {isPositive ? (
              <TrendingUp className="w-5 h-5" />
            ) : (
              <TrendingDown className="w-5 h-5" />
            )}
            <span className="text-2xl font-bold">
              {isPositive ? '+' : ''}{results.predictedChange.toFixed(2)} years
            </span>
          </div>
          <p className="text-gray-600">
            Predicted change in life expectancy
          </p>
        </div>

        {/* Confidence Interval */}
        <div className="mb-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-700">Confidence Interval (95%)</span>
            <span className="text-sm text-gray-500">±{confidenceWidth.toFixed(2)} years</span>
          </div>
          <div className="relative">
            <div className="w-full h-2 bg-gray-200 rounded-full">
              <div 
                className="absolute h-2 bg-primary-500 rounded-full"
                style={{
                  left: `${Math.max(0, (results.confidenceInterval[0] + 2) * 20)}%`,
                  width: `${Math.min(100, confidenceWidth * 20)}%`
                }}
              />
            </div>
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>{results.confidenceInterval[0].toFixed(2)}</span>
              <span>{results.confidenceInterval[1].toFixed(2)}</span>
            </div>
          </div>
        </div>

        {/* Performance Metrics */}
        <div className="grid grid-cols-2 gap-4">
          <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
            <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
              <Clock className="w-4 h-4 text-blue-600" />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-900">
                {(results.responseTime / 1000).toFixed(1)}s
              </p>
              <p className="text-xs text-gray-500">Response Time</p>
            </div>
          </div>

          <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
            <div className="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
              <DollarSign className="w-4 h-4 text-green-600" />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-900">
                ${results.cost.toFixed(3)}
              </p>
              <p className="text-xs text-gray-500">Cost</p>
            </div>
          </div>
        </div>

        {/* Interpretation */}
        <div className="mt-6 p-4 bg-blue-50 rounded-lg">
          <div className="flex items-start space-x-3">
            <Target className="w-5 h-5 text-blue-600 mt-0.5" />
            <div>
              <h4 className="text-sm font-medium text-blue-900 mb-1">
                Interpretation
              </h4>
              <p className="text-sm text-blue-800">
                {isPositive 
                  ? `The simulation predicts a positive impact on life expectancy, suggesting that the proposed policy changes may lead to improved health outcomes.`
                  : `The simulation predicts a negative impact on life expectancy, indicating that the proposed policy changes may lead to worsened health outcomes.`
                }
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ResultsCard
