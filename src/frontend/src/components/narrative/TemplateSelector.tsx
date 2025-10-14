import React from 'react'
import { Settings, Target, MessageSquare, FileText, CheckSquare } from 'lucide-react'
import { NarrativeRequest, NarrativeType, AudienceType, ToneType, LengthType, FocusArea } from '@/types/narrative'

interface TemplateSelectorProps {
  request: NarrativeRequest
  onRequestChange: (changes: Partial<NarrativeRequest>) => void
  disabled?: boolean
}

const TemplateSelector: React.FC<TemplateSelectorProps> = ({
  request,
  onRequestChange,
  disabled = false
}) => {
  const narrativeTypes = [
    { value: NarrativeType.SIMULATION_IMPACT, label: 'Policy Impact Analysis', description: 'Analyzes the impact of policy changes on health outcomes' },
    { value: NarrativeType.BENCHMARK_COMPARISON, label: 'Country Performance Comparison', description: 'Compares country performance across health indicators' },
    { value: NarrativeType.ANOMALY_ALERT, label: 'Anomaly Detection Report', description: 'Reports on detected anomalies in health data' },
    { value: NarrativeType.TREND_ANALYSIS, label: 'Trend Analysis Report', description: 'Analyzes trends in health indicators over time' },
    { value: NarrativeType.EXECUTIVE_SUMMARY, label: 'Executive Summary', description: 'High-level summary for decision makers' }
  ]

  const audiences = [
    { value: AudienceType.MINISTERS, label: 'Ministers', description: 'High-level government officials' },
    { value: AudienceType.POLICY_MAKERS, label: 'Policy Makers', description: 'Government policy analysts' },
    { value: AudienceType.NGOS, label: 'NGOs', description: 'Non-governmental organizations' },
    { value: AudienceType.RESEARCHERS, label: 'Researchers', description: 'Academic and research community' },
    { value: AudienceType.PUBLIC, label: 'Public', description: 'General public audience' }
  ]

  const tones = [
    { value: ToneType.FORMAL, label: 'Formal', description: 'Professional and authoritative' },
    { value: ToneType.CONVERSATIONAL, label: 'Conversational', description: 'Friendly and accessible' },
    { value: ToneType.TECHNICAL, label: 'Technical', description: 'Detailed and analytical' },
    { value: ToneType.PERSUASIVE, label: 'Persuasive', description: 'Compelling and action-oriented' }
  ]

  const lengths = [
    { value: LengthType.BRIEF, label: 'Brief (1-2 pages)', description: 'Quick overview and key points' },
    { value: LengthType.STANDARD, label: 'Standard (3-5 pages)', description: 'Comprehensive analysis' },
    { value: LengthType.DETAILED, label: 'Detailed (5+ pages)', description: 'In-depth examination' }
  ]

  const focusAreas = [
    { value: FocusArea.ECONOMIC_IMPACT, label: 'Economic Impact', description: 'Financial implications and costs' },
    { value: FocusArea.HEALTH_OUTCOMES, label: 'Health Outcomes', description: 'Health indicators and results' },
    { value: FocusArea.IMPLEMENTATION, label: 'Implementation', description: 'Practical implementation guidance' },
    { value: FocusArea.POLICY_RECOMMENDATIONS, label: 'Policy Recommendations', description: 'Actionable policy suggestions' },
    { value: FocusArea.RISK_ASSESSMENT, label: 'Risk Assessment', description: 'Potential risks and mitigation' }
  ]

  const handleNarrativeTypeChange = (type: NarrativeType) => {
    onRequestChange({ narrative_type: type })
  }

  const handleAudienceChange = (audience: AudienceType) => {
    onRequestChange({ audience })
  }

  const handleToneChange = (tone: ToneType) => {
    onRequestChange({ tone })
  }

  const handleLengthChange = (length: LengthType) => {
    onRequestChange({ length })
  }

  const handleFocusAreaToggle = (area: FocusArea) => {
    const currentAreas = request.focus_areas || []
    const newAreas = currentAreas.includes(area)
      ? currentAreas.filter(a => a !== area)
      : [...currentAreas, area]
    
    onRequestChange({ focus_areas: newAreas })
  }

  const handleCustomInstructionsChange = (instructions: string) => {
    onRequestChange({ custom_instructions: instructions })
  }

  const handleIncludeCitationsChange = (include: boolean) => {
    onRequestChange({ include_citations: include })
  }

  const handleIncludeRecommendationsChange = (include: boolean) => {
    onRequestChange({ include_recommendations: include })
  }

  return (
    <div className="space-y-6">
      {/* Narrative Type */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">
          <FileText className="w-4 h-4 inline mr-2" />
          Narrative Type
        </label>
        <div className="space-y-2">
          {narrativeTypes.map((type) => (
            <label key={type.value} className="flex items-start space-x-3 p-3 border rounded-lg cursor-pointer hover:bg-gray-50">
              <input
                type="radio"
                name="narrativeType"
                value={type.value}
                checked={request.narrative_type === type.value}
                onChange={() => handleNarrativeTypeChange(type.value)}
                disabled={disabled}
                className="mt-1"
              />
              <div className="flex-1">
                <div className="text-sm font-medium text-gray-900">{type.label}</div>
                <div className="text-xs text-gray-500">{type.description}</div>
              </div>
            </label>
          ))}
        </div>
      </div>

      {/* Audience */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">
          <Target className="w-4 h-4 inline mr-2" />
          Target Audience
        </label>
        <select
          value={request.audience}
          onChange={(e) => handleAudienceChange(e.target.value as AudienceType)}
          disabled={disabled}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
        >
          {audiences.map((audience) => (
            <option key={audience.value} value={audience.value}>
              {audience.label} - {audience.description}
            </option>
          ))}
        </select>
      </div>

      {/* Tone */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">
          <MessageSquare className="w-4 h-4 inline mr-2" />
          Tone
        </label>
        <select
          value={request.tone}
          onChange={(e) => handleToneChange(e.target.value as ToneType)}
          disabled={disabled}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
        >
          {tones.map((tone) => (
            <option key={tone.value} value={tone.value}>
              {tone.label} - {tone.description}
            </option>
          ))}
        </select>
      </div>

      {/* Length */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">
          <FileText className="w-4 h-4 inline mr-2" />
          Length
        </label>
        <select
          value={request.length}
          onChange={(e) => handleLengthChange(e.target.value as LengthType)}
          disabled={disabled}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
        >
          {lengths.map((length) => (
            <option key={length.value} value={length.value}>
              {length.label} - {length.description}
            </option>
          ))}
        </select>
      </div>

      {/* Focus Areas */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">
          <CheckSquare className="w-4 h-4 inline mr-2" />
          Focus Areas
        </label>
        <div className="space-y-2">
          {focusAreas.map((area) => (
            <label key={area.value} className="flex items-start space-x-3 p-2 border rounded cursor-pointer hover:bg-gray-50">
              <input
                type="checkbox"
                checked={request.focus_areas?.includes(area.value) || false}
                onChange={() => handleFocusAreaToggle(area.value)}
                disabled={disabled}
                className="mt-1"
              />
              <div className="flex-1">
                <div className="text-sm font-medium text-gray-900">{area.label}</div>
                <div className="text-xs text-gray-500">{area.description}</div>
              </div>
            </label>
          ))}
        </div>
      </div>

      {/* Custom Instructions */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          <Settings className="w-4 h-4 inline mr-2" />
          Custom Instructions
        </label>
        <textarea
          value={request.custom_instructions || ''}
          onChange={(e) => handleCustomInstructionsChange(e.target.value)}
          disabled={disabled}
          placeholder="Add any specific instructions for the narrative generation..."
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
          rows={3}
        />
      </div>

      {/* Options */}
      <div className="space-y-3">
        <label className="flex items-center space-x-3">
          <input
            type="checkbox"
            checked={request.include_citations || false}
            onChange={(e) => handleIncludeCitationsChange(e.target.checked)}
            disabled={disabled}
            className="rounded"
          />
          <span className="text-sm font-medium text-gray-700">Include Citations</span>
        </label>
        
        <label className="flex items-center space-x-3">
          <input
            type="checkbox"
            checked={request.include_recommendations || false}
            onChange={(e) => handleIncludeRecommendationsChange(e.target.checked)}
            disabled={disabled}
            className="rounded"
          />
          <span className="text-sm font-medium text-gray-700">Include Recommendations</span>
        </label>
      </div>
    </div>
  )
}

export default TemplateSelector