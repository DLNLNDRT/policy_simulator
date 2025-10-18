import React, { useState } from 'react'
import { Download, FileText, File, Image, X, Loader2, CheckCircle } from 'lucide-react'

// Define the actual backend response type
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

interface ExportManagerProps {
  narrative: NarrativeResponse
  onClose: () => void
}

const ExportManager: React.FC<ExportManagerProps> = ({ narrative, onClose }) => {
  const [isExporting, setIsExporting] = useState(false)
  const [exportFormat, setExportFormat] = useState<string>('')
  const [exportStatus, setExportStatus] = useState<'idle' | 'exporting' | 'success' | 'error'>('idle')
  const [downloadUrl, setDownloadUrl] = useState<string>('')

  const exportFormats = [
    {
      id: 'pdf',
      name: 'PDF Document',
      description: 'Professional PDF report with formatting',
      icon: FileText,
      color: 'text-red-600 bg-red-100'
    },
    {
      id: 'docx',
      name: 'Word Document',
      description: 'Editable Microsoft Word document',
      icon: File,
      color: 'text-blue-600 bg-blue-100'
    },
    {
      id: 'html',
      name: 'HTML Report',
      description: 'Web-ready HTML format',
      icon: FileText,
      color: 'text-green-600 bg-green-100'
    },
    {
      id: 'markdown',
      name: 'Markdown',
      description: 'Plain text with markdown formatting',
      icon: FileText,
      color: 'text-gray-600 bg-gray-100'
    }
  ]

  const handleExport = async (format: string) => {
    setIsExporting(true)
    setExportFormat(format)
    setExportStatus('exporting')

    try {
      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL || ''}/api/narratives/export`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          narrative_id: narrative.narrative_id,
          format: format
        }),
      })

      if (!response.ok) {
        throw new Error('Export failed')
      }

      const exportData = await response.json()
      setDownloadUrl(exportData.download_url)
      setExportStatus('success')
    } catch (error) {
      console.error('Export error:', error)
      setExportStatus('error')
    } finally {
      setIsExporting(false)
    }
  }

  const handleDownload = () => {
    if (downloadUrl) {
      const link = document.createElement('a')
      link.href = downloadUrl
      const filename = `narrative_${narrative.metadata.country}_${narrative.metadata.template}`.replace(/[^a-z0-9]/gi, '_').toLowerCase()
      link.download = `${filename}.${exportFormat}`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
              <Download className="w-5 h-5 text-purple-600" />
            </div>
            <div>
              <h2 className="text-xl font-semibold text-gray-900">Export Narrative</h2>
              <p className="text-sm text-gray-600">Choose your preferred format</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6">
          {/* Narrative Info */}
          <div className="mb-6 p-4 bg-gray-50 rounded-lg">
            <h3 className="text-sm font-medium text-gray-900 mb-2">Narrative Details</h3>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-gray-600">Title:</span>
                <span className="ml-2 font-medium text-gray-900">Policy Simulation Narrative</span>
              </div>
              <div>
                <span className="text-gray-600">Type:</span>
                <span className="ml-2 font-medium text-gray-900">{narrative.metadata.template}</span>
              </div>
              <div>
                <span className="text-gray-600">Word Count:</span>
                <span className="ml-2 font-medium text-gray-900">{narrative.metadata.word_count.toLocaleString()}</span>
              </div>
              <div>
                <span className="text-gray-600">Quality Score:</span>
                <span className="ml-2 font-medium text-gray-900">N/A</span>
              </div>
            </div>
          </div>

          {/* Export Status */}
          {exportStatus === 'exporting' && (
            <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <div className="flex items-center space-x-3">
                <Loader2 className="w-5 h-5 text-blue-600 animate-spin" />
                <div>
                  <h4 className="text-sm font-medium text-blue-900">Exporting...</h4>
                  <p className="text-sm text-blue-700">Generating {exportFormat.toUpperCase()} file</p>
                </div>
              </div>
            </div>
          )}

          {exportStatus === 'success' && (
            <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg">
              <div className="flex items-center space-x-3">
                <CheckCircle className="w-5 h-5 text-green-600" />
                <div>
                  <h4 className="text-sm font-medium text-green-900">Export Complete!</h4>
                  <p className="text-sm text-green-700">Your {exportFormat.toUpperCase()} file is ready for download</p>
                </div>
              </div>
            </div>
          )}

          {exportStatus === 'error' && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
              <div className="flex items-center space-x-3">
                <X className="w-5 h-5 text-red-600" />
                <div>
                  <h4 className="text-sm font-medium text-red-900">Export Failed</h4>
                  <p className="text-sm text-red-700">There was an error generating your file. Please try again.</p>
                </div>
              </div>
            </div>
          )}

          {/* Export Formats */}
          <div className="space-y-3">
            <h3 className="text-sm font-medium text-gray-900">Choose Export Format</h3>
            {exportFormats.map((format) => {
              const IconComponent = format.icon
              return (
                <button
                  key={format.id}
                  onClick={() => handleExport(format.id)}
                  disabled={isExporting}
                  className="w-full p-4 border border-gray-200 rounded-lg hover:border-purple-300 hover:bg-purple-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <div className="flex items-center space-x-4">
                    <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${format.color}`}>
                      <IconComponent className="w-5 h-5" />
                    </div>
                    <div className="flex-1 text-left">
                      <h4 className="text-sm font-medium text-gray-900">{format.name}</h4>
                      <p className="text-xs text-gray-600">{format.description}</p>
                    </div>
                    {isExporting && exportFormat === format.id ? (
                      <Loader2 className="w-5 h-5 text-purple-600 animate-spin" />
                    ) : (
                      <Download className="w-5 h-5 text-gray-400" />
                    )}
                  </div>
                </button>
              )
            })}
          </div>

          {/* Download Button */}
          {exportStatus === 'success' && downloadUrl && (
            <div className="mt-6 pt-6 border-t border-gray-200">
              <button
                onClick={handleDownload}
                className="w-full btn-primary inline-flex items-center justify-center space-x-2"
              >
                <Download className="w-4 h-4" />
                <span>Download {exportFormat.toUpperCase()} File</span>
              </button>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-end space-x-3 p-6 border-t border-gray-200">
          <button
            onClick={onClose}
            className="btn-outline"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  )
}

export default ExportManager
