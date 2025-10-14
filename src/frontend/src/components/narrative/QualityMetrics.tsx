import React from 'react'
import { Star, CheckCircle, Target, BookOpen, TrendingUp } from 'lucide-react'
import { QualityMetrics as QualityMetricsType } from '@/types/narrative'

interface QualityMetricsProps {
  metrics: QualityMetricsType
}

const QualityMetrics: React.FC<QualityMetricsProps> = ({ metrics }) => {
  const getScoreColor = (score: number) => {
    if (score >= 4.5) return 'text-green-600'
    if (score >= 4.0) return 'text-blue-600'
    if (score >= 3.5) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getScoreBgColor = (score: number) => {
    if (score >= 4.5) return 'bg-green-100'
    if (score >= 4.0) return 'bg-blue-100'
    if (score >= 3.5) return 'bg-yellow-100'
    return 'bg-red-100'
  }

  const getScoreLabel = (score: number) => {
    if (score >= 4.5) return 'Excellent'
    if (score >= 4.0) return 'Good'
    if (score >= 3.5) return 'Fair'
    return 'Needs Improvement'
  }

  const renderStars = (score: number) => {
    const stars = []
    const fullStars = Math.floor(score)
    const hasHalfStar = score % 1 >= 0.5

    for (let i = 0; i < 5; i++) {
      if (i < fullStars) {
        stars.push(
          <Star key={i} className="w-4 h-4 text-yellow-400 fill-current" />
        )
      } else if (i === fullStars && hasHalfStar) {
        stars.push(
          <Star key={i} className="w-4 h-4 text-yellow-400 fill-current opacity-50" />
        )
      } else {
        stars.push(
          <Star key={i} className="w-4 h-4 text-gray-300" />
        )
      }
    }
    return stars
  }

  return (
    <div className="card">
      <div className="card-header">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
            <TrendingUp className="w-4 h-4 text-green-600" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">Quality Metrics</h3>
            <p className="text-sm text-gray-600">Narrative quality assessment</p>
          </div>
        </div>
      </div>

      <div className="card-content">
        {/* Overall Score */}
        <div className="mb-6">
          <div className="flex items-center justify-between mb-2">
            <h4 className="text-md font-medium text-gray-900">Overall Quality Score</h4>
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${getScoreBgColor(metrics.overall_score)} ${getScoreColor(metrics.overall_score)}`}>
              {getScoreLabel(metrics.overall_score)}
            </span>
          </div>
          
          <div className="flex items-center space-x-3">
            <div className="flex space-x-1">
              {renderStars(metrics.overall_score)}
            </div>
            <span className={`text-2xl font-bold ${getScoreColor(metrics.overall_score)}`}>
              {metrics.overall_score.toFixed(1)}/5.0
            </span>
          </div>
        </div>

        {/* Individual Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Coherence Score */}
          <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <div className="flex items-center space-x-3 mb-2">
              <CheckCircle className="w-5 h-5 text-blue-600" />
              <h5 className="text-sm font-medium text-gray-900">Coherence</h5>
            </div>
            <div className="flex items-center space-x-2">
              <div className="flex space-x-1">
                {renderStars(metrics.coherence_score)}
              </div>
              <span className={`text-lg font-semibold ${getScoreColor(metrics.coherence_score)}`}>
                {metrics.coherence_score.toFixed(1)}
              </span>
            </div>
            <p className="text-xs text-gray-600 mt-1">Logical flow and consistency</p>
          </div>

          {/* Accuracy Score */}
          <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
            <div className="flex items-center space-x-3 mb-2">
              <Target className="w-5 h-5 text-green-600" />
              <h5 className="text-sm font-medium text-gray-900">Accuracy</h5>
            </div>
            <div className="flex items-center space-x-2">
              <div className="flex space-x-1">
                {renderStars(metrics.accuracy_score)}
              </div>
              <span className={`text-lg font-semibold ${getScoreColor(metrics.accuracy_score)}`}>
                {metrics.accuracy_score.toFixed(1)}
              </span>
            </div>
            <p className="text-xs text-gray-600 mt-1">Factual correctness</p>
          </div>

          {/* Actionability Score */}
          <div className="p-4 bg-purple-50 border border-purple-200 rounded-lg">
            <div className="flex items-center space-x-3 mb-2">
              <Star className="w-5 h-5 text-purple-600" />
              <h5 className="text-sm font-medium text-gray-900">Actionability</h5>
            </div>
            <div className="flex items-center space-x-2">
              <div className="flex space-x-1">
                {renderStars(metrics.actionability_score)}
              </div>
              <span className={`text-lg font-semibold ${getScoreColor(metrics.actionability_score)}`}>
                {metrics.actionability_score.toFixed(1)}
              </span>
            </div>
            <p className="text-xs text-gray-600 mt-1">Practical recommendations</p>
          </div>

          {/* Readability Score */}
          <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
            <div className="flex items-center space-x-3 mb-2">
              <BookOpen className="w-5 h-5 text-yellow-600" />
              <h5 className="text-sm font-medium text-gray-900">Readability</h5>
            </div>
            <div className="flex items-center space-x-2">
              <div className="flex space-x-1">
                {renderStars(metrics.readability_score)}
              </div>
              <span className={`text-lg font-semibold ${getScoreColor(metrics.readability_score)}`}>
                {metrics.readability_score.toFixed(1)}
              </span>
            </div>
            <p className="text-xs text-gray-600 mt-1">Clarity and accessibility</p>
          </div>
        </div>

        {/* Additional Metrics */}
        <div className="mt-6 pt-6 border-t border-gray-200">
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">{metrics.word_count.toLocaleString()}</div>
              <div className="text-sm text-gray-600">Words</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">{metrics.reading_time_minutes}</div>
              <div className="text-sm text-gray-600">Minutes to read</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">
                {metrics.reading_time_minutes < 5 ? 'Quick' : 
                 metrics.reading_time_minutes < 10 ? 'Standard' : 'Detailed'}
              </div>
              <div className="text-sm text-gray-600">Reading level</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default QualityMetrics