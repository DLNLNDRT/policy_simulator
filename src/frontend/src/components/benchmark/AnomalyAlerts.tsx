import React from 'react'
import { AlertTriangle, AlertCircle, AlertOctagon, CheckCircle, Clock, Target } from 'lucide-react'

interface AnomalyAlert {
  country: string
  metric: string
  severity: string
  description: string
  confidence: number
  recommendation: string
  detected_at: string
}

interface AnomalyAlertsProps {
  anomalies: AnomalyAlert[]
}

const AnomalyAlerts: React.FC<AnomalyAlertsProps> = ({ anomalies }) => {
  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'high':
        return <AlertOctagon className="w-5 h-5 text-red-600" />
      case 'medium':
        return <AlertTriangle className="w-5 h-5 text-yellow-600" />
      case 'low':
        return <AlertCircle className="w-5 h-5 text-blue-600" />
      default:
        return <AlertCircle className="w-5 h-5 text-gray-600" />
    }
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high':
        return 'border-red-200 bg-red-50'
      case 'medium':
        return 'border-yellow-200 bg-yellow-50'
      case 'low':
        return 'border-blue-200 bg-blue-50'
      default:
        return 'border-gray-200 bg-gray-50'
    }
  }

  const getSeverityBadgeColor = (severity: string) => {
    switch (severity) {
      case 'high':
        return 'bg-red-100 text-red-800'
      case 'medium':
        return 'bg-yellow-100 text-yellow-800'
      case 'low':
        return 'bg-blue-100 text-blue-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return 'text-green-600'
    if (confidence >= 0.6) return 'text-yellow-600'
    return 'text-red-600'
  }

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp)
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  }

  const getMetricDisplayName = (metric: string) => {
    const names: Record<string, string> = {
      'life_expectancy': 'Life Expectancy',
      'doctor_density': 'Doctor Density',
      'nurse_density': 'Nurse Density',
      'health_spending': 'Health Spending'
    }
    return names[metric] || metric.replace('_', ' ').toUpperCase()
  }

  if (anomalies.length === 0) {
    return (
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="text-center">
          <CheckCircle className="w-12 h-12 text-green-600 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">No Anomalies Detected</h3>
          <p className="text-gray-600">
            All health indicators are within expected ranges for the selected countries.
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-900 flex items-center">
          <AlertTriangle className="w-5 h-5 mr-2 text-orange-600" />
          Anomaly Alerts
        </h3>
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-orange-100 text-orange-800">
          {anomalies.length} detected
        </span>
      </div>

      <div className="space-y-4">
        {anomalies.map((anomaly, index) => (
          <div key={index} className={`border rounded-lg p-4 ${getSeverityColor(anomaly.severity)}`}>
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-center space-x-3">
                {getSeverityIcon(anomaly.severity)}
                <div>
                  <div className="flex items-center space-x-2">
                    <span className="font-medium text-gray-900">
                      {anomaly.country} - {getMetricDisplayName(anomaly.metric)}
                    </span>
                    <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getSeverityBadgeColor(anomaly.severity)}`}>
                      {anomaly.severity.toUpperCase()}
                    </span>
                  </div>
                  <div className="flex items-center space-x-2 mt-1">
                    <Clock className="w-3 h-3 text-gray-500" />
                    <span className="text-sm text-gray-500">
                      Detected {formatTimestamp(anomaly.detected_at)}
                    </span>
                    <span className={`text-sm font-medium ${getConfidenceColor(anomaly.confidence)}`}>
                      {(anomaly.confidence * 100).toFixed(0)}% confidence
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <div className="mb-3">
              <h4 className="text-sm font-medium text-gray-900 mb-1">Description</h4>
              <p className="text-sm text-gray-700">{anomaly.description}</p>
            </div>

            <div className="flex items-start space-x-2">
              <Target className="w-4 h-4 text-blue-600 mt-0.5 flex-shrink-0" />
              <div>
                <h4 className="text-sm font-medium text-gray-900 mb-1">Recommendation</h4>
                <p className="text-sm text-gray-700">{anomaly.recommendation}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Summary */}
      <div className="bg-white rounded-lg border border-gray-200 p-4">
        <h4 className="text-sm font-medium text-gray-900 mb-3">Anomaly Summary</h4>
        <div className="grid grid-cols-3 gap-4 text-center">
          <div>
            <div className="text-2xl font-bold text-red-600">
              {anomalies.filter(a => a.severity === 'high').length}
            </div>
            <div className="text-sm text-gray-500">High Severity</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-yellow-600">
              {anomalies.filter(a => a.severity === 'medium').length}
            </div>
            <div className="text-sm text-gray-500">Medium Severity</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-blue-600">
              {anomalies.filter(a => a.severity === 'low').length}
            </div>
            <div className="text-sm text-gray-500">Low Severity</div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AnomalyAlerts