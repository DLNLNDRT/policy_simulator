import React, { useState } from 'react'
import { 
  FileText, 
  Download, 
  Eye, 
  Settings, 
  Plus, 
  Trash2, 
  Move,
  Save,
  Upload
} from 'lucide-react'

interface ReportSection {
  id: string
  title: string
  type: 'text' | 'chart' | 'table' | 'analysis'
  content: any
  enabled: boolean
}

interface ReportTemplate {
  id: string
  name: string
  description: string
  sections: string[]
}

interface ReportBuilderProps {
  onGenerate?: (config: any) => void
}

const ReportBuilder: React.FC<ReportBuilderProps> = ({ onGenerate }) => {
  const [reportConfig, setReportConfig] = useState({
    title: 'Policy Analysis Report',
    template: 'executive_summary',
    format: 'pdf',
    branding: {
      logo: '',
      primaryColor: '#3498db',
      secondaryColor: '#2c3e50',
      font: 'Arial'
    }
  })

  const [sections, setSections] = useState<ReportSection[]>([
    { id: 'executive_summary', title: 'Executive Summary', type: 'text', content: '', enabled: true },
    { id: 'key_findings', title: 'Key Findings', type: 'analysis', content: '', enabled: true },
    { id: 'methodology', title: 'Methodology', type: 'text', content: '', enabled: true },
    { id: 'recommendations', title: 'Recommendations', type: 'text', content: '', enabled: true }
  ])

  const [isGenerating, setIsGenerating] = useState(false)
  const [showPreview, setShowPreview] = useState(false)
  const [showSettings, setShowSettings] = useState(false)

  const templates: ReportTemplate[] = [
    {
      id: 'executive_summary',
      name: 'Executive Summary',
      description: 'High-level summary for decision makers',
      sections: ['executive_summary', 'key_findings', 'recommendations', 'methodology']
    },
    {
      id: 'detailed_analysis',
      name: 'Detailed Analysis Report',
      description: 'Comprehensive analysis with methodology',
      sections: ['executive_summary', 'methodology', 'data_sources', 'analysis_results', 'statistical_analysis', 'recommendations', 'appendix']
    },
    {
      id: 'policy_brief',
      name: 'Policy Brief',
      description: 'Concise policy-focused report',
      sections: ['policy_context', 'key_findings', 'policy_implications', 'recommendations', 'next_steps']
    },
    {
      id: 'research_report',
      name: 'Research Report',
      description: 'Academic-style research report',
      sections: ['abstract', 'introduction', 'literature_review', 'methodology', 'results', 'discussion', 'conclusions', 'references']
    }
  ]

  const handleTemplateChange = (templateId: string) => {
    const template = templates.find(t => t.id === templateId)
    if (template) {
      setReportConfig({ ...reportConfig, template: templateId })
      // Update sections based on template
      const newSections = template.sections.map(sectionId => ({
        id: sectionId,
        title: sectionId.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()),
        type: 'text' as const,
        content: '',
        enabled: true
      }))
      setSections(newSections)
    }
  }

  const handleSectionToggle = (sectionId: string) => {
    setSections(sections.map(section => 
      section.id === sectionId 
        ? { ...section, enabled: !section.enabled }
        : section
    ))
  }

  const handleSectionContentChange = (sectionId: string, content: any) => {
    setSections(sections.map(section => 
      section.id === sectionId 
        ? { ...section, content }
        : section
    ))
  }

  const handleGenerateReport = async () => {
    if (!onGenerate) return

    setIsGenerating(true)
    try {
      const config = {
        template: reportConfig.template,
        title: reportConfig.title,
        config: {
          branding: reportConfig.branding,
          sections: sections.filter(s => s.enabled)
        },
        simulation_data: {
          // Mock simulation data
          predicted_change: 0.75,
          confidence_score: 0.85
        },
        analytics_data: {
          // Mock analytics data
          trend_analysis: {
            trend_direction: 'increasing',
            trend_strength: 0.78
          }
        },
        data_sources: [
          'WHO Global Health Observatory'
        ]
      }

      await onGenerate(config)
    } finally {
      setIsGenerating(false)
    }
  }

  const handleExport = (format: string) => {
    // Handle export functionality
    console.log(`Exporting report as ${format}`)
  }

  return (
    <div className="report-builder">
      <div className="builder-header">
        <div className="header-content">
          <h2 className="builder-title">Report Builder</h2>
          <p className="builder-description">
            Create professional reports with customizable templates
          </p>
        </div>
        <div className="header-actions">
          <button
            onClick={() => setShowPreview(!showPreview)}
            className="btn-outline inline-flex items-center space-x-2"
          >
            <Eye className="w-4 h-4" />
            <span>{showPreview ? 'Hide' : 'Show'} Preview</span>
          </button>
          <button
            onClick={() => setShowSettings(!showSettings)}
            className="btn-outline inline-flex items-center space-x-2"
          >
            <Settings className="w-4 h-4" />
            <span>Settings</span>
          </button>
          <button
            onClick={handleGenerateReport}
            disabled={isGenerating}
            className="btn-primary inline-flex items-center space-x-2"
          >
            <FileText className="w-4 h-4" />
            <span>{isGenerating ? 'Generating...' : 'Generate Report'}</span>
          </button>
        </div>
      </div>

      <div className="builder-content">
        <div className="builder-main">
          {/* Report Configuration */}
          <div className="config-section">
            <h3>Report Configuration</h3>
            <div className="config-form">
              <div className="form-row">
                <div className="form-group">
                  <label>Report Title</label>
                  <input
                    type="text"
                    value={reportConfig.title}
                    onChange={(e) => setReportConfig({ ...reportConfig, title: e.target.value })}
                    className="form-input"
                    placeholder="Enter report title"
                  />
                </div>
                <div className="form-group">
                  <label>Template</label>
                  <select
                    value={reportConfig.template}
                    onChange={(e) => handleTemplateChange(e.target.value)}
                    className="form-select"
                  >
                    {templates.map(template => (
                      <option key={template.id} value={template.id}>
                        {template.name}
                      </option>
                    ))}
                  </select>
                </div>
                <div className="form-group">
                  <label>Export Format</label>
                  <select
                    value={reportConfig.format}
                    onChange={(e) => setReportConfig({ ...reportConfig, format: e.target.value })}
                    className="form-select"
                  >
                    <option value="pdf">PDF</option>
                    <option value="docx">DOCX</option>
                    <option value="html">HTML</option>
                    <option value="pptx">PowerPoint</option>
                  </select>
                </div>
              </div>
            </div>
          </div>

          {/* Report Sections */}
          <div className="sections-section">
            <div className="sections-header">
              <h3>Report Sections</h3>
              <p>Configure which sections to include in your report</p>
            </div>
            <div className="sections-list">
              {sections.map((section, index) => (
                <div key={section.id} className="section-item">
                  <div className="section-header">
                    <div className="section-info">
                      <div className="section-controls">
                        <button className="drag-handle">
                          <Move className="w-4 h-4" />
                        </button>
                        <input
                          type="checkbox"
                          checked={section.enabled}
                          onChange={() => handleSectionToggle(section.id)}
                          className="section-checkbox"
                        />
                      </div>
                      <div className="section-details">
                        <h4 className="section-title">{section.title}</h4>
                        <span className="section-type">{section.type}</span>
                      </div>
                    </div>
                    <div className="section-actions">
                      <button className="btn-icon">
                        <Settings className="w-4 h-4" />
                      </button>
                      <button className="btn-icon text-red-600">
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                  
                  {section.enabled && (
                    <div className="section-content">
                      {section.type === 'text' && (
                        <textarea
                          value={section.content}
                          onChange={(e) => handleSectionContentChange(section.id, e.target.value)}
                          className="section-textarea"
                          placeholder={`Enter content for ${section.title}...`}
                          rows={4}
                        />
                      )}
                      {section.type === 'analysis' && (
                        <div className="analysis-placeholder">
                          <p>Analysis content will be automatically generated based on available data.</p>
                        </div>
                      )}
                      {section.type === 'chart' && (
                        <div className="chart-placeholder">
                          <p>Chart content will be automatically generated based on selected visualizations.</p>
                        </div>
                      )}
                      {section.type === 'table' && (
                        <div className="table-placeholder">
                          <p>Table content will be automatically generated based on analysis results.</p>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Settings Panel */}
        {showSettings && (
          <div className="settings-panel">
            <div className="settings-header">
              <h3>Report Settings</h3>
              <button
                onClick={() => setShowSettings(false)}
                className="btn-icon"
              >
                ×
              </button>
            </div>
            
            <div className="settings-content">
              <div className="setting-group">
                <h4>Branding</h4>
                <div className="setting-item">
                  <label>Logo</label>
                  <div className="logo-upload">
                    <input
                      type="file"
                      accept="image/*"
                      onChange={(e) => {
                        // Handle logo upload
                        console.log('Logo upload:', e.target.files?.[0])
                      }}
                      className="file-input"
                    />
                    <button className="btn-outline">
                      <Upload className="w-4 h-4" />
                      Upload Logo
                    </button>
                  </div>
                </div>
                <div className="setting-item">
                  <label>Primary Color</label>
                  <input
                    type="color"
                    value={reportConfig.branding.primaryColor}
                    onChange={(e) => setReportConfig({
                      ...reportConfig,
                      branding: { ...reportConfig.branding, primaryColor: e.target.value }
                    })}
                    className="color-input"
                  />
                </div>
                <div className="setting-item">
                  <label>Secondary Color</label>
                  <input
                    type="color"
                    value={reportConfig.branding.secondaryColor}
                    onChange={(e) => setReportConfig({
                      ...reportConfig,
                      branding: { ...reportConfig.branding, secondaryColor: e.target.value }
                    })}
                    className="color-input"
                  />
                </div>
                <div className="setting-item">
                  <label>Font</label>
                  <select
                    value={reportConfig.branding.font}
                    onChange={(e) => setReportConfig({
                      ...reportConfig,
                      branding: { ...reportConfig.branding, font: e.target.value }
                    })}
                    className="form-select"
                  >
                    <option value="Arial">Arial</option>
                    <option value="Times New Roman">Times New Roman</option>
                    <option value="Calibri">Calibri</option>
                    <option value="Helvetica">Helvetica</option>
                  </select>
                </div>
              </div>

              <div className="setting-group">
                <h4>Export Options</h4>
                <div className="export-buttons">
                  <button
                    onClick={() => handleExport('pdf')}
                    className="btn-outline"
                  >
                    <Download className="w-4 h-4" />
                    Export PDF
                  </button>
                  <button
                    onClick={() => handleExport('docx')}
                    className="btn-outline"
                  >
                    <Download className="w-4 h-4" />
                    Export DOCX
                  </button>
                  <button
                    onClick={() => handleExport('pptx')}
                    className="btn-outline"
                  >
                    <Download className="w-4 h-4" />
                    Export PowerPoint
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Preview Panel */}
        {showPreview && (
          <div className="preview-panel">
            <div className="preview-header">
              <h3>Report Preview</h3>
              <button
                onClick={() => setShowPreview(false)}
                className="btn-icon"
              >
                ×
              </button>
            </div>
            <div className="preview-content">
              <div className="preview-document">
                <div className="document-header">
                  <h1>{reportConfig.title}</h1>
                  <p className="document-meta">
                    Generated on {new Date().toLocaleDateString()}
                  </p>
                </div>
                <div className="document-sections">
                  {sections.filter(s => s.enabled).map(section => (
                    <div key={section.id} className="preview-section">
                      <h2>{section.title}</h2>
                      <div className="preview-content">
                        {section.content || (
                          <p className="placeholder-text">
                            Content for {section.title} will appear here...
                          </p>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default ReportBuilder
