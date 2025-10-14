import React, { useState, useEffect } from 'react'
import { BarChart, FileText, TrendingUp, AlertTriangle, Users, Target } from 'lucide-react'
import NarrativeBuilder from './NarrativeBuilder'
import { NarrativeRequest, NarrativeType, AudienceType, ToneType, LengthType, FocusArea } from '@/types/narrative'

interface BenchmarkNarrativeProps {
  benchmarkData?: any // Data from Feature 2 benchmark results
  onNarrativeGenerated?: (narrative: any) => void
}

const BenchmarkNarrative: React.FC<BenchmarkNarrativeProps> = ({
  benchmarkData,
  onNarrativeGenerated
}) => {
  const [hasData, setHasData] = useState(false)

  useEffect(() => {
    setHasData(!!benchmarkData && Object.keys(benchmarkData).length > 0)
  }, [benchmarkData])

  // Transform benchmark data for narrative generation
  const transformBenchmarkData = (data: any) => {
    if (!data) return {}

    return {
      countries: data.countries || [],
      best_performer: data.summary?.best_performer || 'N/A',
      worst_performer: data.summary?.worst_performer || 'N/A',
      total_anomalies: data.summary?.total_anomalies || 0,
      high_severity_anomalies: data.summary?.high_severity_anomalies || 0,
      peer_groups: data.summary?.peer_groups || 0,
      average_score: data.summary?.average_score || 0,
      rankings: data.rankings || [],
      anomalies: data.anomalies || [],
      peer_analysis: data.peer_analysis || {}
    }
  }

  const defaultNarrativeRequest: NarrativeRequest = {
    narrative_type: NarrativeType.BENCHMARK_COMPARISON,
    audience: AudienceType.POLICY_MAKERS,
    tone: ToneType.FORMAL,
    length: LengthType.STANDARD,
    focus_areas: [FocusArea.POLICY_RECOMMENDATIONS, FocusArea.HEALTH_OUTCOMES],
    data_source: transformBenchmarkData(benchmarkData),
    include_citations: true,
    include_recommendations: true,
    custom_instructions: ''
  }

  if (!hasData) {
    return (
      <div className="card">
        <div className="card-content text-center py-12">
          <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <BarChart className="w-8 h-8 text-gray-400" />
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            No Benchmark Data Available
          </h3>
          <p className="text-gray-600 mb-6">
            Run a benchmark comparison first to generate a narrative about country performance.
          </p>
          <div className="space-y-2 text-sm text-gray-500">
            <p>• Go to Feature 2: Benchmark Dashboard</p>
            <p>• Compare countries across health indicators</p>
            <p>• Return here to generate a narrative</p>
          </div>
        </div>
      </div>
    )
  }

  const getTopPerformers = () => {
    if (!benchmarkData.rankings) return []
    return benchmarkData.rankings.slice(0, 3)
  }

  const getAnomalyCount = () => {
    if (!benchmarkData.anomalies) return 0
    return benchmarkData.anomalies.length
  }

  const getHighSeverityAnomalies = () => {
    if (!benchmarkData.anomalies) return 0
    return benchmarkData.anomalies.filter((a: any) => a.severity === 'high').length
  }

  return (
    <div className="space-y-6">
      {/* Benchmark Data Summary */}
      <div className="card">
        <div className="card-header">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
              <BarChart className="w-4 h-4 text-green-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900">Benchmark Results</h3>
              <p className="text-sm text-gray-600">Data from your country comparison</p>
            </div>
          </div>
        </div>
        
        <div className="card-content">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center p-3 bg-blue-50 rounded-lg">
              <div className="text-lg font-semibold text-blue-900">
                {benchmarkData.countries?.length || 0}
              </div>
              <div className="text-xs text-blue-600">Countries Compared</div>
            </div>
            
            <div className="text-center p-3 bg-green-50 rounded-lg">
              <div className="text-lg font-semibold text-green-900">
                {benchmarkData.summary?.best_performer || 'N/A'}
              </div>
              <div className="text-xs text-green-600">Best Performer</div>
            </div>
            
            <div className="text-center p-3 bg-yellow-50 rounded-lg">
              <div className="text-lg font-semibold text-yellow-900">
                {getAnomalyCount()}
              </div>
              <div className="text-xs text-yellow-600">Anomalies Detected</div>
            </div>
            
            <div className="text-center p-3 bg-purple-50 rounded-lg">
              <div className="text-lg font-semibold text-purple-900">
                {benchmarkData.summary?.peer_groups || 0}
              </div>
              <div className="text-xs text-purple-600">Peer Groups</div>
            </div>
          </div>
          
          {/* Top Performers */}
          {getTopPerformers().length > 0 && (
            <div className="mt-4 pt-4 border-t border-gray-200">
              <h4 className="text-sm font-medium text-gray-900 mb-3">Top Performers</h4>
              <div className="space-y-2">
                {getTopPerformers().map((country: any, index: number) => (
                  <div key={index} className="flex items-center justify-between p-2 bg-gray-50 rounded-lg">
                    <div className="flex items-center space-x-3">
                      <div className="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center">
                        <span className="text-xs font-medium text-blue-600">#{index + 1}</span>
                      </div>
                      <span className="text-sm font-medium text-gray-900">{country.country_name}</span>
                    </div>
                    <div className="text-sm text-gray-600">
                      Score: {(country.total_score * 100).toFixed(1)}%
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
          
          {/* Anomalies Summary */}
          {getAnomalyCount() > 0 && (
            <div className="mt-4 pt-4 border-t border-gray-200">
              <h4 className="text-sm font-medium text-gray-900 mb-3 flex items-center">
                <AlertTriangle className="w-4 h-4 mr-2 text-yellow-500" />
                Anomalies Detected
              </h4>
              <div className="grid grid-cols-3 gap-4">
                <div className="text-center p-2 bg-red-50 rounded-lg">
                  <div className="text-sm font-semibold text-red-900">{getHighSeverityAnomalies()}</div>
                  <div className="text-xs text-red-600">High Severity</div>
                </div>
                <div className="text-center p-2 bg-yellow-50 rounded-lg">
                  <div className="text-sm font-semibold text-yellow-900">
                    {getAnomalyCount() - getHighSeverityAnomalies()}
                  </div>
                  <div className="text-xs text-yellow-600">Medium/Low</div>
                </div>
                <div className="text-center p-2 bg-gray-50 rounded-lg">
                  <div className="text-sm font-semibold text-gray-900">{getAnomalyCount()}</div>
                  <div className="text-xs text-gray-600">Total</div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Narrative Builder */}
      <NarrativeBuilder
        dataSource={transformBenchmarkData(benchmarkData)}
        onNarrativeGenerated={onNarrativeGenerated}
      />
    </div>
  )
}

export default BenchmarkNarrative
