import React, { useState } from 'react'
import { 
  FileText, 
  Download, 
  Share2, 
  Clock, 
  DollarSign,
  Star,
  MessageSquare,
  Target,
  ExternalLink
} from 'lucide-react'
import { NarrativeResponse } from '@/types/narrative'

interface NarrativePreviewProps {
  narrative: NarrativeResponse
  onExport: (format: 'pdf' | 'docx' | 'html' | 'markdown') => void
}

const NarrativePreview: React.FC<NarrativePreviewProps> = ({
  narrative,
  onExport
}) => {
  const [activeSection, setActiveSection] = useState<string | null>(null)

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp)
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  }

  const getQualityColor = (score: number) => {
    if (score >= 4.5) return 'text-green-600 bg-green-100'
    if (score >= 4.0) return 'text-blue-600 bg-blue-100'
    if (score >= 3.5) return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
  }

  const getQualityLabel = (score: number) => {
    if (score >= 4.5) return 'Excellent'
    if (score >= 4.0) return 'Good'
    if (score >= 3.5) return 'Fair'
    return 'Poor'
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">{narrative.title}</h2>
            <div className="flex items-center space-x-4 text-sm text-gray-600">
              <div className="flex items-center space-x-1">
                <FileText className="w-4 h-4" />
                <span>{narrative.narrative_type.replace('_', ' ').toUpperCase()}</span>
              </div>
              <div className="flex items-center space-x-1">
                <Clock className="w-4 h-4" />
                <span>{narrative.quality_metrics.reading_time_minutes} min read</span>
              </div>
              <div className="flex items-center space-x-1">
                <DollarSign className="w-4 h-4" />
                <span>${narrative.cost_usd.toFixed(3)}</span>
              </div>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getQualityColor(narrative.quality_metrics.overall_score)}`}>
              <Star className="w-3 h-3 mr-1" />
              {narrative.quality_metrics.overall_score.toFixed(1)} - {getQualityLabel(narrative.quality_metrics.overall_score)}
            </span>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center space-x-3">
          <button
            onClick={() => onExport('pdf')}
            className="btn-outline inline-flex items-center space-x-2"
          >
            <Download className="w-4 h-4" />
            <span>Export PDF</span>
          </button>
          <button
            onClick={() => onExport('docx')}
            className="btn-outline inline-flex items-center space-x-2"
          >
            <Download className="w-4 h-4" />
            <span>Export DOCX</span>
          </button>
          <button
            onClick={() => onExport('html')}
            className="btn-outline inline-flex items-center space-x-2"
          >
            <ExternalLink className="w-4 h-4" />
            <span>Export HTML</span>
          </button>
        </div>
      </div>

      {/* Executive Summary */}
      {narrative.executive_summary && (
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <MessageSquare className="w-5 h-5 mr-2 text-blue-600" />
            Executive Summary
          </h3>
          <div className="prose max-w-none">
            <p className="text-gray-700 leading-relaxed">{narrative.executive_summary}</p>
          </div>
        </div>
      )}

      {/* Key Insights */}
      {narrative.key_insights && narrative.key_insights.length > 0 && (
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <Target className="w-5 h-5 mr-2 text-green-600" />
            Key Insights
          </h3>
          <ul className="space-y-3">
            {narrative.key_insights.map((insight, index) => (
              <li key={index} className="flex items-start space-x-3">
                <div className="w-2 h-2 bg-green-600 rounded-full mt-2 flex-shrink-0"></div>
                <span className="text-gray-700">{insight}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Sections */}
      {narrative.sections && narrative.sections.length > 0 && (
        <div className="bg-white rounded-lg border border-gray-200">
          <div className="p-6 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900">Narrative Sections</h3>
          </div>
          
          <div className="divide-y divide-gray-200">
            {narrative.sections.map((section, index) => (
              <div key={index} className="p-6">
                <div className="flex items-start justify-between mb-3">
                  <h4 className="text-lg font-medium text-gray-900">{section.title}</h4>
                  <div className="flex items-center space-x-2 text-sm text-gray-500">
                    <span>{section.word_count} words</span>
                  </div>
                </div>
                
                <div className="prose max-w-none">
                  <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">{section.content}</p>
                </div>
                
                {section.key_points && section.key_points.length > 0 && (
                  <div className="mt-4">
                    <h5 className="text-sm font-medium text-gray-900 mb-2">Key Points:</h5>
                    <ul className="space-y-1">
                      {section.key_points.map((point, pointIndex) => (
                        <li key={pointIndex} className="flex items-start space-x-2 text-sm text-gray-600">
                          <div className="w-1.5 h-1.5 bg-gray-400 rounded-full mt-2 flex-shrink-0"></div>
                          <span>{point}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Recommendations */}
      {narrative.recommendations && narrative.recommendations.length > 0 && (
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <Target className="w-5 h-5 mr-2 text-orange-600" />
            Recommendations
          </h3>
          <div className="space-y-4">
            {narrative.recommendations.map((recommendation, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-start justify-between mb-2">
                  <h4 className="font-medium text-gray-900">{recommendation.title}</h4>
                  <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                    recommendation.priority === 'high' ? 'bg-red-100 text-red-800' :
                    recommendation.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-green-100 text-green-800'
                  }`}>
                    {recommendation.priority.toUpperCase()}
                  </span>
                </div>
                <p className="text-gray-700 text-sm">{recommendation.description}</p>
                {recommendation.timeline && (
                  <div className="mt-2 text-xs text-gray-500">
                    <strong>Timeline:</strong> {recommendation.timeline}
                  </div>
                )}
                {recommendation.resources_needed && (
                  <div className="mt-2 text-xs text-gray-500">
                    <strong>Resources:</strong> {recommendation.resources_needed}
                  </div>
                )}
                {recommendation.expected_impact && (
                  <div className="mt-2 text-xs text-gray-500">
                    <strong>Expected Impact:</strong> {recommendation.expected_impact}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Citations */}
      {narrative.citations && narrative.citations.length > 0 && (
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <ExternalLink className="w-5 h-5 mr-2 text-gray-600" />
            Citations
          </h3>
          <div className="space-y-3">
            {narrative.citations.map((citation, index) => (
              <div key={index} className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg">
                <div className="w-6 h-6 bg-gray-200 rounded-full flex items-center justify-center text-xs font-medium text-gray-600 flex-shrink-0">
                  {index + 1}
                </div>
                <div className="flex-1">
                  <div className="font-medium text-gray-900">{citation.source}</div>
                  <div className="text-sm text-gray-600">{citation.type}</div>
                  <div className="text-sm text-gray-500">{citation.relevance}</div>
                  {citation.url && (
                    <a href={citation.url} target="_blank" rel="noopener noreferrer" className="text-sm text-blue-600 hover:text-blue-800">
                      {citation.url}
                    </a>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Metadata */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Generation Details</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div>
            <div className="text-gray-500">Generated</div>
            <div className="font-medium text-gray-900">{formatTimestamp(narrative.generated_at)}</div>
          </div>
          <div>
            <div className="text-gray-500">Generation Time</div>
            <div className="font-medium text-gray-900">{(narrative.generation_time_ms / 1000).toFixed(1)}s</div>
          </div>
          <div>
            <div className="text-gray-500">Word Count</div>
            <div className="font-medium text-gray-900">{narrative.quality_metrics.word_count}</div>
          </div>
          <div>
            <div className="text-gray-500">Cost</div>
            <div className="font-medium text-gray-900">${narrative.cost_usd.toFixed(3)}</div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default NarrativePreview
