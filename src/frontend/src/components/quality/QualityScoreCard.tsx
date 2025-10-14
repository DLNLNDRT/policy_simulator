import React from 'react'
import { LucideIcon } from 'lucide-react'

interface QualityScoreCardProps {
  title: string
  score: number
  icon: React.ReactElement<LucideIcon>
  color: 'green' | 'blue' | 'purple' | 'orange' | 'red'
  trend?: 'up' | 'down' | 'stable'
  subtitle?: string
}

const QualityScoreCard: React.FC<QualityScoreCardProps> = ({
  title,
  score,
  icon,
  color,
  trend,
  subtitle
}) => {
  const getColorClasses = (color: string) => {
    switch (color) {
      case 'green':
        return {
          bg: 'bg-green-50',
          icon: 'text-green-600',
          score: 'text-green-700',
          title: 'text-green-800'
        }
      case 'blue':
        return {
          bg: 'bg-blue-50',
          icon: 'text-blue-600',
          score: 'text-blue-700',
          title: 'text-blue-800'
        }
      case 'purple':
        return {
          bg: 'bg-purple-50',
          icon: 'text-purple-600',
          score: 'text-purple-700',
          title: 'text-purple-800'
        }
      case 'orange':
        return {
          bg: 'bg-orange-50',
          icon: 'text-orange-600',
          score: 'text-orange-700',
          title: 'text-orange-800'
        }
      case 'red':
        return {
          bg: 'bg-red-50',
          icon: 'text-red-600',
          score: 'text-red-700',
          title: 'text-red-800'
        }
      default:
        return {
          bg: 'bg-gray-50',
          icon: 'text-gray-600',
          score: 'text-gray-700',
          title: 'text-gray-800'
        }
    }
  }

  const getScoreStatus = (score: number) => {
    if (score >= 95) return { status: 'Excellent', color: 'text-green-600' }
    if (score >= 85) return { status: 'Good', color: 'text-blue-600' }
    if (score >= 75) return { status: 'Fair', color: 'text-orange-600' }
    return { status: 'Poor', color: 'text-red-600' }
  }

  const getTrendIcon = (trend?: string) => {
    if (!trend) return null
    
    switch (trend) {
      case 'up':
        return (
          <svg className="w-3 h-3 text-green-500" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M5.293 9.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 7.414V15a1 1 0 11-2 0V7.414L6.707 9.707a1 1 0 01-1.414 0z" clipRule="evenodd" />
          </svg>
        )
      case 'down':
        return (
          <svg className="w-3 h-3 text-red-500" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M14.707 10.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 12.586V5a1 1 0 012 0v7.586l2.293-2.293a1 1 0 011.414 0z" clipRule="evenodd" />
          </svg>
        )
      default:
        return (
          <svg className="w-3 h-3 text-gray-500" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clipRule="evenodd" />
          </svg>
        )
    }
  }

  const colors = getColorClasses(color)
  const scoreStatus = getScoreStatus(score)

  return (
    <div className={`p-4 rounded-lg ${colors.bg} border border-opacity-20`}>
      <div className="flex items-center justify-between mb-3">
        <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${colors.bg}`}>
          <div className={colors.icon}>
            {icon}
          </div>
        </div>
        {trend && (
          <div className="flex items-center space-x-1">
            {getTrendIcon(trend)}
          </div>
        )}
      </div>
      
      <div className="space-y-1">
        <h4 className={`text-sm font-medium ${colors.title}`}>
          {title}
        </h4>
        <div className="flex items-baseline space-x-2">
          <span className={`text-2xl font-bold ${colors.score}`}>
            {score.toFixed(1)}
          </span>
          <span className="text-sm text-gray-500">/100</span>
        </div>
        <p className={`text-xs font-medium ${scoreStatus.color}`}>
          {scoreStatus.status}
        </p>
        {subtitle && (
          <p className="text-xs text-gray-600">
            {subtitle}
          </p>
        )}
      </div>
    </div>
  )
}

export default QualityScoreCard
