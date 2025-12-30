import React, { useState, useMemo } from 'react'
import { Brain, AlertTriangle, ExternalLink, ChevronDown, ChevronUp } from 'lucide-react'

interface NarrativeCardProps {
  narrative: string
  disclaimers: string[]
  citations: string[]
}

const NarrativeCard: React.FC<NarrativeCardProps> = ({ narrative, disclaimers, citations }) => {
  const [showDisclaimers, setShowDisclaimers] = useState(true)
  const [showCitations, setShowCitations] = useState(false)

  // Format narrative text with proper structure and line breaks
  const formattedNarrative = useMemo(() => {
    if (!narrative) return []

    // Split text into sections based on markdown headers (**Section:**)
    const sections: Array<{ type: 'header' | 'paragraph'; title?: string; content: string[] }> = []
    
    // Split by sections that start with **Header:**
    const parts = narrative.split(/(?=\*\*[^*]+\*\*:)/g)
    
    parts.forEach((part) => {
      const trimmedPart = part.trim()
      if (!trimmedPart) return
      
      // Check if this part starts with a bold header
      const headerMatch = trimmedPart.match(/^\*\*([^*]+)\*\*:\s*(.*)/s)
      
      if (headerMatch) {
        const [, title, content] = headerMatch
        const contentLines = content
          .split('\n')
          .map(line => line.trim())
          .filter(line => line.length > 0)
        
        sections.push({
          type: 'header',
          title: title.trim(),
          content: contentLines
        })
      } else {
        // Regular paragraph
        const lines = trimmedPart
          .split('\n')
          .map(line => line.trim())
          .filter(line => line.length > 0)
        
        if (lines.length > 0) {
          sections.push({
            type: 'paragraph',
            content: lines
          })
        }
      }
    })
    
    // Convert sections to JSX
    return sections.map((section, sectionIndex) => {
      if (section.type === 'header' && section.title) {
        const hasBulletPoints = section.content.some(line => line.startsWith('- '))
        const bulletItems: string[] = []
        const regularLines: string[] = []
        
        section.content.forEach(line => {
          if (line.startsWith('- ')) {
            bulletItems.push(line.substring(2).trim())
          } else {
            regularLines.push(line)
          }
        })
        
        return (
          <div key={sectionIndex} className="mb-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-3">
              {section.title}
            </h3>
            {hasBulletPoints && bulletItems.length > 0 && (
              <ul className="list-disc list-inside space-y-2 mb-3 text-gray-700">
                {bulletItems.map((item, itemIndex) => (
                  <li key={itemIndex} className="leading-relaxed">
                    {item}
                  </li>
                ))}
              </ul>
            )}
            {regularLines.length > 0 && (
              <div className="space-y-2">
                {regularLines.map((line, lineIndex) => (
                  <p key={lineIndex} className="text-gray-700 leading-relaxed">
                    {line}
                  </p>
                ))}
              </div>
            )}
          </div>
        )
      } else {
        // Regular paragraph section
        return (
          <div key={sectionIndex} className="mb-4">
            {section.content.map((line, lineIndex) => (
              <p key={lineIndex} className="text-gray-700 leading-relaxed mb-2">
                {line}
              </p>
            ))}
          </div>
        )
      }
    })
  }, [narrative])

  return (
    <div className="card">
      <div className="card-header">
        <h2 className="card-title flex items-center space-x-2">
          <Brain className="w-5 h-5 text-purple-600" />
          <span>AI-Generated Analysis</span>
        </h2>
        <p className="card-description">
          Contextual insights and policy implications
        </p>
      </div>
      
      <div className="card-content space-y-6">
        {/* Main Narrative */}
        <div className="prose prose-sm max-w-none">
          <div className="text-gray-700 leading-relaxed">
            {formattedNarrative}
          </div>
        </div>

        {/* Disclaimers */}
        <div className="border-t border-gray-200 pt-6">
          <button
            onClick={() => setShowDisclaimers(!showDisclaimers)}
            className="flex items-center justify-between w-full text-left"
          >
            <h3 className="text-lg font-semibold text-gray-900 flex items-center space-x-2">
              <AlertTriangle className="w-5 h-5 text-yellow-600" />
              <span>Important Disclaimers</span>
            </h3>
            {showDisclaimers ? (
              <ChevronUp className="w-5 h-5 text-gray-400" />
            ) : (
              <ChevronDown className="w-5 h-5 text-gray-400" />
            )}
          </button>
          
          {showDisclaimers && (
            <div className="mt-4 space-y-3">
              {disclaimers.map((disclaimer, index) => (
                <div key={index} className="flex items-start space-x-3 p-3 bg-yellow-50 rounded-lg">
                  <AlertTriangle className="w-4 h-4 text-yellow-600 mt-0.5 flex-shrink-0" />
                  <p className="text-sm text-yellow-800">{disclaimer}</p>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Citations */}
        <div className="border-t border-gray-200 pt-6">
          <button
            onClick={() => setShowCitations(!showCitations)}
            className="flex items-center justify-between w-full text-left"
          >
            <h3 className="text-lg font-semibold text-gray-900 flex items-center space-x-2">
              <ExternalLink className="w-5 h-5 text-blue-600" />
              <span>Data Sources & Citations</span>
            </h3>
            {showCitations ? (
              <ChevronUp className="w-5 h-5 text-gray-400" />
            ) : (
              <ChevronDown className="w-5 h-5 text-gray-400" />
            )}
          </button>
          
          {showCitations && (
            <div className="mt-4 space-y-2">
              {citations.map((citation, index) => (
                <div key={index} className="flex items-center space-x-3 p-3 bg-blue-50 rounded-lg">
                  <ExternalLink className="w-4 h-4 text-blue-600 flex-shrink-0" />
                  <p className="text-sm text-blue-800">{citation}</p>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* AI Notice */}
        <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
          <div className="flex items-start space-x-3">
            <Brain className="w-5 h-5 text-purple-600 mt-0.5" />
            <div>
              <h4 className="text-sm font-medium text-purple-900 mb-1">
                AI-Generated Content
              </h4>
              <p className="text-sm text-purple-800">
                This analysis was generated using GPT-4 and is based on statistical correlations 
                in the underlying health data. It should be used for exploratory analysis and 
                policy discussion, not as definitive policy recommendations.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default NarrativeCard
