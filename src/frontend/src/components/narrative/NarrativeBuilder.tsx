import React, { useState, useEffect } from 'react'
import { FileText, Download, Eye, Loader2, AlertCircle } from 'lucide-react'
import TemplateSelector from './TemplateSelector'
import PreviewPanel from './PreviewPanel'
import ExportManager from './ExportManager'
import QualityMetrics from './QualityMetrics'
import { NarrativeRequest, NarrativeResponse, NarrativeType, AudienceType, ToneType, LengthType, FocusArea } from '@/types/narrative'

interface NarrativeBuilderProps {
  dataSource?: Record<string, any> // Data from Feature 1 or Feature 2
  onNarrativeGenerated?: (narrative: NarrativeResponse) => void
}

const NarrativeBuilder: React.FC<NarrativeBuilderProps> = ({
  dataSource,
  onNarrativeGenerated
}) => {
  const [isGenerating, setIsGenerating] = useState(false)
  const [generatedNarrative, setGeneratedNarrative] = useState<NarrativeResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [showPreview, setShowPreview] = useState(false)
  const [showExport, setShowExport] = useState(false)

  // Default narrative request
  const [narrativeRequest, setNarrativeRequest] = useState<NarrativeRequest>({
    narrative_type: NarrativeType.SIMULATION_IMPACT,
    audience: AudienceType.POLICY_MAKERS,
    tone: ToneType.FORMAL,
    length: LengthType.STANDARD,
    focus_areas: [FocusArea.POLICY_RECOMMENDATIONS, FocusArea.HEALTH_OUTCOMES],
    data_source: dataSource || {},
    include_citations: true,
    include_recommendations: true,
    custom_instructions: ''
  })

  // Update data source when prop changes
  useEffect(() => {
    if (dataSource) {
      setNarrativeRequest(prev => ({
        ...prev,
        data_source: dataSource
      }))
    }
  }, [dataSource])

  const handleGenerateNarrative = async () => {
    setIsGenerating(true)
    setError(null)
    setGeneratedNarrative(null)

    try {
      const response = await fetch('/api/narratives/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(narrativeRequest),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to generate narrative')
      }

      const narrative: NarrativeResponse = await response.json()
      setGeneratedNarrative(narrative)
      setShowPreview(true)
      
      if (onNarrativeGenerated) {
        onNarrativeGenerated(narrative)
      }
    } catch (err: any) {
      console.error('Narrative generation failed:', err)
      setError(err.message || 'An error occurred while generating the narrative')
    } finally {
      setIsGenerating(false)
    }
  }

  const handleTemplateChange = (template: Partial<NarrativeRequest>) => {
    setNarrativeRequest((prev: NarrativeRequest) => ({
      ...prev,
      ...template
    }))
  }

  const handleExport = () => {
    setShowExport(true)
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
            <FileText className="w-5 h-5 text-purple-600" />
          </div>
          <div>
            <h2 className="text-xl font-semibold text-gray-900">Narrative Generator</h2>
            <p className="text-sm text-gray-600">Transform data into compelling policy narratives</p>
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          <button
            onClick={() => setShowPreview(!showPreview)}
            className="btn-outline inline-flex items-center space-x-2"
            disabled={!generatedNarrative}
          >
            <Eye className="w-4 h-4" />
            <span>{showPreview ? 'Hide' : 'Show'} Preview</span>
          </button>
          
          <button
            onClick={handleExport}
            className="btn-outline inline-flex items-center space-x-2"
            disabled={!generatedNarrative}
          >
            <Download className="w-4 h-4" />
            <span>Export</span>
          </button>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start space-x-3">
          <AlertCircle className="w-5 h-5 text-red-600 mt-0.5" />
          <div>
            <h4 className="text-sm font-medium text-red-800">Generation Error</h4>
            <p className="text-sm text-red-700 mt-1">{error}</p>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Template Selection */}
        <div className="lg:col-span-1">
          <TemplateSelector
            request={narrativeRequest}
            onRequestChange={handleTemplateChange}
            disabled={isGenerating}
          />
        </div>

        {/* Right Column: Preview and Results */}
        <div className="lg:col-span-2 space-y-6">
          {/* Generation Button */}
          <div className="card">
            <div className="card-content">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-medium text-gray-900">Generate Narrative</h3>
                  <p className="text-sm text-gray-600">
                    Create a compelling narrative based on your selected template and data
                  </p>
                </div>
                
                <button
                  onClick={handleGenerateNarrative}
                  disabled={isGenerating || !narrativeRequest.data_source}
                  className="btn-primary inline-flex items-center space-x-2"
                >
                  {isGenerating ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      <span>Generating...</span>
                    </>
                  ) : (
                    <>
                      <FileText className="w-4 h-4" />
                      <span>Generate</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>

          {/* Preview Panel */}
          {showPreview && generatedNarrative && (
            <PreviewPanel narrative={generatedNarrative} />
          )}

          {/* Quality Metrics */}
          {generatedNarrative && (
            <QualityMetrics metrics={generatedNarrative.quality_metrics} />
          )}
        </div>
      </div>

      {/* Export Modal */}
      {showExport && generatedNarrative && (
        <ExportManager
          narrative={generatedNarrative}
          onClose={() => setShowExport(false)}
        />
      )}
    </div>
  )
}

export default NarrativeBuilder