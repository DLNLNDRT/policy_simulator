import React from 'react'
import { Users, TrendingUp, BarChart3, Globe } from 'lucide-react'
import { PeerGroup } from '@/types/benchmark'

interface PeerGroupAnalysisProps {
  peerGroups: PeerGroup[]
  className?: string
}

const PeerGroupAnalysis: React.FC<PeerGroupAnalysisProps> = ({
  peerGroups,
  className = ''
}) => {
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

  const getCountryName = (code: string) => {
    const names: Record<string, string> = {
      'PRT': 'Portugal',
      'ESP': 'Spain',
      'SWE': 'Sweden',
      'GRC': 'Greece'
    }
    return names[code] || code
  }

  if (peerGroups.length === 0) {
    return (
      <div className={`peer-group-analysis ${className}`}>
        <div className="bg-white rounded-lg border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900 flex items-center">
              <Users className="w-5 h-5 mr-2 text-blue-600" />
              Peer Group Analysis
            </h3>
            <p className="text-sm text-gray-600 mt-1">
              No peer groups identified
            </p>
          </div>
          <div className="px-6 py-8 text-center">
            <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Users className="w-8 h-8 text-gray-400" />
            </div>
            <h4 className="text-lg font-medium text-gray-900 mb-2">
              No Peer Groups Found
            </h4>
            <p className="text-gray-600">
              Unable to identify peer groups for the selected countries based on current criteria.
            </p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className={`peer-group-analysis ${className}`}>
      <div className="bg-white rounded-lg border border-gray-200">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 flex items-center">
            <Users className="w-5 h-5 mr-2 text-blue-600" />
            Peer Group Analysis
          </h3>
          <p className="text-sm text-gray-600 mt-1">
            {peerGroups.length} peer group{peerGroups.length !== 1 ? 's' : ''} identified
          </p>
        </div>

        <div className="divide-y divide-gray-200">
          {peerGroups.map((group, index) => (
            <div key={index} className="p-6">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h4 className="text-lg font-medium text-gray-900 mb-1">
                    {group.name}
                  </h4>
                  <div className="flex items-center space-x-2 text-sm text-gray-600">
                    <Users className="w-4 h-4" />
                    <span>{group.size} countries</span>
                    <span>•</span>
                    <span>Criteria: {group.criteria.join(', ')}</span>
                  </div>
                </div>
                <div className="flex items-center space-x-1">
                  <Globe className="w-4 h-4 text-gray-400" />
                  <span className="text-sm text-gray-500">
                    {group.countries.length} members
                  </span>
                </div>
              </div>

              {/* Countries in Group */}
              <div className="mb-4">
                <h5 className="text-sm font-medium text-gray-700 mb-2">Countries</h5>
                <div className="flex flex-wrap gap-2">
                  {group.countries.map(countryCode => (
                    <span
                      key={countryCode}
                      className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                    >
                      {getCountryName(countryCode)}
                    </span>
                  ))}
                </div>
              </div>

              {/* Group Averages */}
              {Object.keys(group.average).length > 0 && (
                <div>
                  <h5 className="text-sm font-medium text-gray-700 mb-3">Group Averages</h5>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {Object.entries(group.average).map(([metric, value]) => (
                      <div key={metric} className="bg-gray-50 rounded-lg p-3">
                        <div className="flex items-center space-x-2 mb-1">
                          <BarChart3 className="w-4 h-4 text-gray-600" />
                          <span className="text-xs font-medium text-gray-600">
                            {getMetricDisplayName(metric)}
                          </span>
                        </div>
                        <div className="text-lg font-semibold text-gray-900">
                          {formatMetricValue(value, metric)}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Summary */}
        <div className="px-6 py-4 bg-gray-50 border-t border-gray-200">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div className="text-center">
              <div className="text-lg font-semibold text-blue-600">
                {peerGroups.length}
              </div>
              <div className="text-xs text-gray-600">Peer Groups</div>
            </div>
            <div className="text-center">
              <div className="text-lg font-semibold text-green-600">
                {peerGroups.reduce((sum, group) => sum + group.size, 0)}
              </div>
              <div className="text-xs text-gray-600">Total Countries</div>
            </div>
            <div className="text-center">
              <div className="text-lg font-semibold text-purple-600">
                {peerGroups.reduce((sum, group) => sum + group.criteria.length, 0)}
              </div>
              <div className="text-xs text-gray-600">Grouping Criteria</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default PeerGroupAnalysis
