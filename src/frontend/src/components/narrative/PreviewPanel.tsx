import React, { useState } from 'react'
import { FileText, Eye, EyeOff, Clock, Download, AlertTriangle, BookOpen } from 'lucide-react'

interface NarrativeResponse {
  narrative_id: string
  narrative: string
  disclaimers: string[]
  citations: string[]
  metadata: {
    country: string
    template: string
    audience: string
    generated_at: string
    word_count: number
  }
}

interface PreviewPanelProps {
  narrative: NarrativeResponse
}

const PreviewPanel: React.FC<PreviewPanelProps> = ({ narrative }) => {
  const [showFullContent, setShowFullContent] = useState(false)

  const formatReadingTime = (wordCount: number) => {
    const minutes = Math.ceil(wordCount / 200) // Average reading speed
    if (minutes < 1) return '< 1 min'
    if (minutes === 1) return '1 min'
    return `${minutes} mins`
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
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
              <h3 className="text-lg font-semibold text-gray-900">Policy Simulation Narrative</h3>
              <p className="text-sm text-gray-600">Generated for {narrative.metadata.country} • {narrative.metadata.audience}</p>
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
            
            <button className="btn-outline btn-sm inline-flex items-center space-x-2">
              <Download className="w-4 h-4" />
              <span>Export</span>
            </button>
          </div>
        </div>
      </div>

      <div className="card-content">
        {/* Narrative Content */}
        <div className="space-y-6">
          <div className="prose prose-sm max-w-none">
            <div className="whitespace-pre-wrap text-gray-700 leading-relaxed">
              {narrative.narrative}
            </div>
          </div>

          {/* Disclaimers */}
          {narrative.disclaimers && narrative.disclaimers.length > 0 && (
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <div className="flex items-start space-x-3">
                <AlertTriangle className="w-5 h-5 text-yellow-600 mt-0.5" />
                <div>
                  <h4 className="text-sm font-medium text-yellow-800 mb-2">Important Disclaimers</h4>
                  <ul className="text-sm text-yellow-700 space-y-1">
                    {narrative.disclaimers.map((disclaimer, index) => (
                      <li key={index} className="flex items-start space-x-2">
                        <span className="text-yellow-600 mt-1">•</span>
                        <span>{disclaimer}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          )}

          {/* Citations */}
          {narrative.citations && narrative.citations.length > 0 && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div className="flex items-start space-x-3">
                <BookOpen className="w-5 h-5 text-blue-600 mt-0.5" />
                <div>
                  <h4 className="text-sm font-medium text-blue-800 mb-2">Data Sources & Citations</h4>
                  <ul className="text-sm text-blue-700 space-y-1">
                    {narrative.citations.map((citation, index) => (
                      <li key={index} className="flex items-start space-x-2">
                        <span className="text-blue-600 mt-1">•</span>
                        <span>{citation}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Metadata */}
        <div className="mt-6 pt-6 border-t border-gray-200">
          <div className="flex items-center justify-between text-sm text-gray-500">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-1">
                <Clock className="w-4 h-4" />
                <span>{formatReadingTime(narrative.metadata.word_count)}</span>
              </div>
              <div className="flex items-center space-x-1">
                <FileText className="w-4 h-4" />
                <span>{narrative.metadata.word_count} words</span>
              </div>
            </div>
            <div className="text-xs">
              Generated {formatDate(narrative.metadata.generated_at)}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default PreviewPanel