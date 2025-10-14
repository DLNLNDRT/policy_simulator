import React, { useState } from 'react'
import { 
  AlertTriangle, 
  AlertCircle, 
  Info, 
  X, 
  CheckCircle,
  Clock,
  MapPin,
  Filter
} from 'lucide-react'
import { QualityAlert as QualityAlertType } from '@/types/quality'

interface QualityAlertsProps {
  alerts: QualityAlertType[]
  onResolveAlert?: (alertId: string) => void
  onDismissAlert?: (alertId: string) => void
}

const QualityAlerts: React.FC<QualityAlertsProps> = ({
  alerts,
  onResolveAlert,
  onDismissAlert
}) => {
  const [filter, setFilter] = useState<'all' | 'unresolved' | 'resolved'>('unresolved')
  const [severityFilter, setSeverityFilter] = useState<'all' | 'low' | 'medium' | 'high' | 'critical'>('all')

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'critical':
        return <AlertTriangle className="w-5 h-5 text-red-600" />
      case 'high':
        return <AlertCircle className="w-5 h-5 text-orange-600" />
      case 'medium':
        return <AlertCircle className="w-5 h-5 text-yellow-600" />
      case 'low':
        return <Info className="w-5 h-5 text-blue-600" />
      default:
        return <Info className="w-5 h-5 text-gray-600" />
    }
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'bg-red-50 border-red-200 text-red-800'
      case 'high':
        return 'bg-orange-50 border-orange-200 text-orange-800'
      case 'medium':
        return 'bg-yellow-50 border-yellow-200 text-yellow-800'
      case 'low':
        return 'bg-blue-50 border-blue-200 text-blue-800'
      default:
        return 'bg-gray-50 border-gray-200 text-gray-800'
    }
  }

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'completeness':
        return <CheckCircle className="w-4 h-4" />
      case 'validity':
        return <AlertTriangle className="w-4 h-4" />
      case 'consistency':
        return <Filter className="w-4 h-4" />
      case 'freshness':
        return <Clock className="w-4 h-4" />
      default:
        return <Info className="w-4 h-4" />
    }
  }

  const filteredAlerts = alerts.filter(alert => {
    const statusMatch = filter === 'all' || 
      (filter === 'unresolved' && !alert.resolved) ||
      (filter === 'resolved' && alert.resolved)
    
    const severityMatch = severityFilter === 'all' || alert.severity === severityFilter
    
    return statusMatch && severityMatch
  })

  const handleResolveAlert = (alertId: string) => {
    if (onResolveAlert) {
      onResolveAlert(alertId)
    }
  }

  const handleDismissAlert = (alertId: string) => {
    if (onDismissAlert) {
      onDismissAlert(alertId)
    }
  }

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString()
  }

  return (
    <div className="card">
      <div className="card-header">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-yellow-100 rounded-lg flex items-center justify-center">
              <AlertTriangle className="w-4 h-4 text-yellow-600" />
            </div>
            <div>
              <h3 className="card-title">Quality Alerts</h3>
              <p className="text-sm text-gray-600">
                {filteredAlerts.length} of {alerts.length} alerts
              </p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <select
              value={filter}
              onChange={(e) => setFilter(e.target.value as any)}
              className="text-sm border border-gray-300 rounded-md px-2 py-1"
            >
              <option value="all">All Alerts</option>
              <option value="unresolved">Unresolved</option>
              <option value="resolved">Resolved</option>
            </select>
            
            <select
              value={severityFilter}
              onChange={(e) => setSeverityFilter(e.target.value as any)}
              className="text-sm border border-gray-300 rounded-md px-2 py-1"
            >
              <option value="all">All Severities</option>
              <option value="critical">Critical</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>
          </div>
        </div>
      </div>
      
      <div className="card-content">
        {filteredAlerts.length === 0 ? (
          <div className="text-center py-8">
            <CheckCircle className="w-12 h-12 text-green-500 mx-auto mb-4" />
            <h4 className="text-lg font-medium text-gray-900 mb-2">No Alerts</h4>
            <p className="text-gray-600">
              {filter === 'unresolved' 
                ? 'All quality alerts have been resolved!' 
                : 'No alerts match the current filters.'}
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {filteredAlerts.map((alert) => (
              <div
                key={alert.id}
                className={`p-4 rounded-lg border ${getSeverityColor(alert.severity)} ${
                  alert.resolved ? 'opacity-75' : ''
                }`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-start space-x-3 flex-1">
                    <div className="flex-shrink-0 mt-1">
                      {getSeverityIcon(alert.severity)}
                    </div>
                    
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center space-x-2 mb-2">
                        <div className="flex items-center space-x-1">
                          {getTypeIcon(alert.type)}
                          <span className="text-sm font-medium capitalize">
                            {alert.type}
                          </span>
                        </div>
                        <span className="text-sm font-medium capitalize">
                          {alert.severity}
                        </span>
                        {alert.resolved && (
                          <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                            Resolved
                          </span>
                        )}
                      </div>
                      
                      <p className="text-sm font-medium mb-2">
                        {alert.message}
                      </p>
                      
                      {alert.affected_indicators && alert.affected_indicators.length > 0 && (
                        <div className="flex items-center space-x-2 mb-2">
                          <MapPin className="w-4 h-4" />
                          <span className="text-sm text-gray-600">
                            Affects: {alert.affected_indicators.join(', ')}
                          </span>
                        </div>
                      )}
                      
                      {alert.affected_countries && alert.affected_countries.length > 0 && (
                        <div className="flex items-center space-x-2 mb-2">
                          <MapPin className="w-4 h-4" />
                          <span className="text-sm text-gray-600">
                            Countries: {alert.affected_countries.join(', ')}
                          </span>
                        </div>
                      )}
                      
                      <div className="flex items-center space-x-4 text-xs text-gray-600">
                        <div className="flex items-center space-x-1">
                          <Clock className="w-3 h-3" />
                          <span>Created: {formatTimestamp(alert.created_at)}</span>
                        </div>
                        {alert.resolved && alert.resolved_at && (
                          <div className="flex items-center space-x-1">
                            <CheckCircle className="w-3 h-3" />
                            <span>Resolved: {formatTimestamp(alert.resolved_at)}</span>
                          </div>
                        )}
                      </div>
                      
                      {alert.recommendations && alert.recommendations.length > 0 && (
                        <div className="mt-3">
                          <h5 className="text-sm font-medium mb-2">Recommendations:</h5>
                          <ul className="text-sm space-y-1">
                            {alert.recommendations.map((recommendation, index) => (
                              <li key={index} className="flex items-start space-x-2">
                                <span className="text-gray-400 mt-1">•</span>
                                <span>{recommendation}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  </div>
                  
                  {!alert.resolved && (
                    <div className="flex items-center space-x-2 ml-4">
                      <button
                        onClick={() => handleResolveAlert(alert.id)}
                        className="text-sm px-3 py-1 bg-green-100 text-green-700 rounded-md hover:bg-green-200 transition-colors"
                      >
                        Resolve
                      </button>
                      <button
                        onClick={() => handleDismissAlert(alert.id)}
                        className="text-gray-400 hover:text-gray-600 transition-colors"
                      >
                        <X className="w-4 h-4" />
                      </button>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default QualityAlerts
