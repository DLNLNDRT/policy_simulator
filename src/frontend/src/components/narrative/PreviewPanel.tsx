import React, { useState } from 'react'
import { FileText, Eye, EyeOff, Clock, Star, Users, Target, Download } from 'lucide-react'
import { NarrativeResponse, NarrativeSection } from '@/types/narrative'

interface PreviewPanelProps {
  narrative: NarrativeResponse
}

const PreviewPanel: React.FC<PreviewPanelProps> = ({ narrative }) => {
  const [expandedSections, setExpandedSections] = useState<Set<number>>(new Set([0])) // First section expanded by default
  const [showFullContent, setShowFullContent] = useState(false)

  const toggleSection = (index: number) => {
    const newExpanded = new Set(expandedSections)
    if (newExpanded.has(index)) {
      newExpanded.delete(index)
    } else {
      newExpanded.add(index)
    }
    setExpandedSections(newExpanded)
  }

  const formatReadingTime = (minutes: number) => {
    if (minutes < 1) return '< 1 min'
    if (minutes === 1) return '1 min'
    return `${minutes} mins`
  }

  const getQualityColor = (score: number) => {
    if (score >= 4.5) return 'text-green-600 bg-green-100'
    if (score >= 4.0) return 'text-blue-600 bg-blue-100'
    if (score >= 3.5) return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
  }

  return (
    <div className="card">
      <div className="card-header">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
              <FileText className="w-4 h-4 text-purple-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900">{narrative.title}</h3>
              <p className="text-sm text-gray-600">Generated Narrative Preview</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setShowFullContent(!showFullContent)}
              className="btn-outline btn-sm inline-flex items-center space-x-2"
            >
              {showFullContent ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              <span>{showFullContent ? 'Collapse' : 'Expand'}</span>
            </button>
          </div>
        </div>
      </div>

      <div className="card-content">
        {/* Narrative Metadata */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div className="flex items-center space-x-2 p-3 bg-gray-50 rounded-lg">
            <Clock className="w-4 h-4 text-gray-600" />
            <div>
              <p className="text-sm font-medium text-gray-900">
                {formatReadingTime(narrative.quality_metrics.reading_time_minutes)}
              </p>
              <p className="text-xs text-gray-500">Reading time</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2 p-3 bg-gray-50 rounded-lg">
            <FileText className="w-4 h-4 text-gray-600" />
            <div>
              <p className="text-sm font-medium text-gray-900">
                {narrative.quality_metrics.word_count.toLocaleString()}
              </p>
              <p className="text-xs text-gray-500">Words</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2 p-3 bg-gray-50 rounded-lg">
            <Star className="w-4 h-4 text-gray-600" />
            <div>
              <p className="text-sm font-medium text-gray-900">
                {narrative.quality_metrics.overall_score.toFixed(1)}/5.0
              </p>
              <p className="text-xs text-gray-500">Quality score</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2 p-3 bg-gray-50 rounded-lg">
            <Target className="w-4 h-4 text-gray-600" />
            <div>
              <p className="text-sm font-medium text-gray-900">
                {narrative.sections.length}
              </p>
              <p className="text-xs text-gray-500">Sections</p>
            </div>
          </div>
        </div>

        {/* Executive Summary */}
        {narrative.executive_summary && (
          <div className="mb-6">
            <h4 className="text-md font-semibold text-gray-900 mb-3 flex items-center">
              <Star className="w-4 h-4 mr-2 text-yellow-500" />
              Executive Summary
            </h4>
            <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
              <p className="text-sm text-gray-800 leading-relaxed">
                {narrative.executive_summary}
              </p>
            </div>
          </div>
        )}

        {/* Key Insights */}
        {narrative.key_insights && narrative.key_insights.length > 0 && (
          <div className="mb-6">
            <h4 className="text-md font-semibold text-gray-900 mb-3 flex items-center">
              <Target className="w-4 h-4 mr-2 text-blue-500" />
              Key Insights
            </h4>
            <div className="space-y-2">
              {narrative.key_insights.map((insight, index) => (
                <div key={index} className="flex items-start space-x-3 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                  <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>
                  <p className="text-sm text-gray-800">{insight}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Narrative Sections */}
        <div className="space-y-4">
          <h4 className="text-md font-semibold text-gray-900 flex items-center">
            <FileText className="w-4 h-4 mr-2 text-purple-500" />
            Narrative Sections
          </h4>
          
          {narrative.sections.map((section: NarrativeSection, index: number) => (
            <div key={index} className="border border-gray-200 rounded-lg">
              <button
                onClick={() => toggleSection(index)}
                className="w-full px-4 py-3 text-left flex items-center justify-between hover:bg-gray-50 focus:outline-none focus:bg-gray-50"
              >
                <div className="flex items-center space-x-3">
                  <div className="w-6 h-6 bg-purple-100 rounded-full flex items-center justify-center">
                    <span className="text-xs font-medium text-purple-600">{index + 1}</span>
                  </div>
                  <div>
                    <h5 className="text-sm font-medium text-gray-900">{section.title}</h5>
                    <p className="text-xs text-gray-500">{section.word_count} words</p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-2">
                  {section.key_points && section.key_points.length > 0 && (
                    <span className="text-xs text-gray-500">
                      {section.key_points.length} key points
                    </span>
                  )}
                  <div className={`w-2 h-2 rounded-full transition-transform ${
                    expandedSections.has(index) ? 'rotate-180' : ''
                  }`}>
                    <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                  </div>
                </div>
              </button>
              
              {expandedSections.has(index) && (
                <div className="px-4 pb-4 border-t border-gray-100">
                  <div className="pt-4">
                    <div className="prose prose-sm max-w-none">
                      <p className="text-sm text-gray-800 leading-relaxed whitespace-pre-wrap">
                        {section.content}
                      </p>
                    </div>
                    
                    {/* Key Points */}
                    {section.key_points && section.key_points.length > 0 && (
                      <div className="mt-4">
                        <h6 className="text-xs font-medium text-gray-700 mb-2">Key Points:</h6>
                        <ul className="space-y-1">
                          {section.key_points.map((point, pointIndex) => (
                            <li key={pointIndex} className="flex items-start space-x-2 text-xs text-gray-600">
                              <div className="w-1 h-1 bg-gray-400 rounded-full mt-2 flex-shrink-0"></div>
                              <span>{point}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Recommendations */}
        {narrative.recommendations && narrative.recommendations.length > 0 && (
          <div className="mt-6">
            <h4 className="text-md font-semibold text-gray-900 mb-3 flex items-center">
              <Target className="w-4 h-4 mr-2 text-green-500" />
              Recommendations
            </h4>
            <div className="space-y-3">
              {narrative.recommendations.map((rec, index) => (
                <div key={index} className="p-4 bg-green-50 border border-green-200 rounded-lg">
                  <h5 className="text-sm font-medium text-green-900 mb-2">{rec.title}</h5>
                  <p className="text-sm text-green-800">{rec.description}</p>
                  {rec.priority && (
                    <div className="mt-2">
                      <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                        rec.priority === 'high' ? 'bg-red-100 text-red-800' :
                        rec.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-green-100 text-green-800'
                      }`}>
                        {rec.priority} priority
                      </span>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Citations */}
        {narrative.citations && narrative.citations.length > 0 && (
          <div className="mt-6">
            <h4 className="text-md font-semibold text-gray-900 mb-3 flex items-center">
              <FileText className="w-4 h-4 mr-2 text-gray-500" />
              Citations
            </h4>
            <div className="space-y-2">
              {narrative.citations.map((citation, index) => (
                <div key={index} className="p-3 bg-gray-50 border border-gray-200 rounded-lg">
                  <p className="text-sm text-gray-800">{citation.source}</p>
                  {citation.url && (
                    <a 
                      href={citation.url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-xs text-blue-600 hover:text-blue-800"
                    >
                      View Source
                    </a>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default PreviewPanel
