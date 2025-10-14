import React, { useState } from 'react'
import { Helmet } from 'react-helmet-async'
import { 
  Shield, 
  Download, 
  FileText,
  BarChart3,
  AlertTriangle,
  CheckCircle
} from 'lucide-react'
import QualityDashboard from '@/components/quality/QualityDashboard'
import { QualityOverview } from '@/types/quality'

const QualityPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'overview' | 'trends' | 'sources' | 'alerts'>('overview')
  const [exporting, setExporting] = useState(false)

  const handleRefresh = () => {
    // Refresh logic will be handled by individual components
    console.log('Refreshing quality data...')
  }

  const handleExport = async () => {
    setExporting(true)
    try {
      // Export quality data
      const exportData = {
        timestamp: new Date().toISOString(),
        type: 'quality_export',
        data: {
          overview: 'Quality overview data would be exported here',
          trends: 'Quality trends data would be exported here',
          sources: 'Data sources information would be exported here',
          alerts: 'Quality alerts would be exported here'
        }
      }
      
      const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `quality-export-${Date.now()}.json`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    } catch (error) {
      console.error('Export failed:', error)
    } finally {
      setExporting(false)
    }
  }

  const tabs = [
    {
      id: 'overview' as const,
      name: 'Overview',
      icon: <Shield className="w-4 h-4" />,
      description: 'Overall quality metrics and alerts'
    },
    {
      id: 'trends' as const,
      name: 'Trends',
      icon: <BarChart3 className="w-4 h-4" />,
      description: 'Quality trends over time'
    },
    {
      id: 'sources' as const,
      name: 'Data Sources',
      icon: <FileText className="w-4 h-4" />,
      description: 'Data sources and provenance'
    },
    {
      id: 'alerts' as const,
      name: 'Alerts',
      icon: <AlertTriangle className="w-4 h-4" />,
      description: 'Quality alerts and issues'
    }
  ]

  return (
    <>
      <Helmet>
        <title>Data Quality Assurance - Policy Simulation Assistant</title>
        <meta name="description" content="Monitor data quality, track provenance, and ensure data integrity for health policy simulations." />
      </Helmet>

      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Data Quality Assurance
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Monitor data quality, track data provenance, and ensure the integrity 
              of health indicators used in policy simulations.
            </p>
          </div>

          {/* Tab Navigation */}
          <div className="mb-8">
            <div className="border-b border-gray-200">
              <nav className="-mb-px flex space-x-8">
                {tabs.map((tab) => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`py-2 px-1 border-b-2 font-medium text-sm inline-flex items-center space-x-2 ${
                      activeTab === tab.id
                        ? 'border-primary-500 text-primary-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    {tab.icon}
                    <span>{tab.name}</span>
                  </button>
                ))}
              </nav>
            </div>
            <div className="mt-2">
              <p className="text-sm text-gray-600">
                {tabs.find(tab => tab.id === activeTab)?.description}
              </p>
            </div>
          </div>

          {/* Tab Content */}
          <div className="space-y-6">
            {activeTab === 'overview' && (
              <QualityDashboard 
                onRefresh={handleRefresh}
                onExport={handleExport}
              />
            )}
            
            {activeTab === 'trends' && (
              <div className="space-y-6">
                <div className="card">
                  <div className="card-header">
                    <h3 className="card-title">Quality Trends Analysis</h3>
                    <p className="text-sm text-gray-600">
                      Track quality metrics over time and identify patterns
                    </p>
                  </div>
                  <div className="card-content">
                    <div className="text-center py-12">
                      <BarChart3 className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                      <h4 className="text-lg font-semibold text-gray-900 mb-2">
                        Quality Trends
                      </h4>
                      <p className="text-gray-600 mb-4">
                        Interactive quality trends will be displayed here
                      </p>
                      <button
                        onClick={handleRefresh}
                        className="btn-primary"
                      >
                        Load Trends
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            )}
            
            {activeTab === 'sources' && (
              <div className="space-y-6">
                <div className="card">
                  <div className="card-header">
                    <h3 className="card-title">Data Sources & Provenance</h3>
                    <p className="text-sm text-gray-600">
                      Track data sources, processing steps, and maintain audit trails
                    </p>
                  </div>
                  <div className="card-content">
                    <div className="text-center py-12">
                      <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                      <h4 className="text-lg font-semibold text-gray-900 mb-2">
                        Data Sources
                      </h4>
                      <p className="text-gray-600 mb-4">
                        Data source information and provenance tracking will be displayed here
                      </p>
                      <button
                        onClick={handleRefresh}
                        className="btn-primary"
                      >
                        Load Sources
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            )}
            
            {activeTab === 'alerts' && (
              <div className="space-y-6">
                <div className="card">
                  <div className="card-header">
                    <h3 className="card-title">Quality Alerts & Issues</h3>
                    <p className="text-sm text-gray-600">
                      Monitor and manage data quality alerts and issues
                    </p>
                  </div>
                  <div className="card-content">
                    <div className="text-center py-12">
                      <AlertTriangle className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                      <h4 className="text-lg font-semibold text-gray-900 mb-2">
                        Quality Alerts
                      </h4>
                      <p className="text-gray-600 mb-4">
                        Quality alerts and issue management will be displayed here
                      </p>
                      <button
                        onClick={handleRefresh}
                        className="btn-primary"
                      >
                        Load Alerts
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Info Cards */}
          <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="card p-6">
              <div className="flex items-center space-x-3 mb-4">
                <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                  <CheckCircle className="w-5 h-5 text-green-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900">
                  Quality Monitoring
                </h3>
              </div>
              <p className="text-gray-600 text-sm">
                Real-time monitoring of data completeness, validity, consistency, 
                and freshness across all health indicators.
              </p>
            </div>

            <div className="card p-6">
              <div className="flex items-center space-x-3 mb-4">
                <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                  <FileText className="w-5 h-5 text-blue-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900">
                  Provenance Tracking
                </h3>
              </div>
              <p className="text-gray-600 text-sm">
                Complete audit trail of data sources, processing steps, 
                and transformations for full transparency.
              </p>
            </div>

            <div className="card p-6">
              <div className="flex items-center space-x-3 mb-4">
                <div className="w-10 h-10 bg-yellow-100 rounded-lg flex items-center justify-center">
                  <AlertTriangle className="w-5 h-5 text-yellow-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900">
                  Alert Management
                </h3>
              </div>
              <p className="text-gray-600 text-sm">
                Proactive alerts for quality issues with actionable 
                recommendations and resolution tracking.
              </p>
            </div>
          </div>

          {/* Export Section */}
          <div className="mt-8 text-center">
            <button
              onClick={handleExport}
              disabled={exporting}
              className="btn-outline btn-lg inline-flex items-center space-x-2"
            >
              {exporting ? (
                <>
                  <div className="loading-spinner w-5 h-5" />
                  <span>Exporting...</span>
                </>
              ) : (
                <>
                  <Download className="w-5 h-5" />
                  <span>Export Quality Report</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </>
  )
}

export default QualityPage
