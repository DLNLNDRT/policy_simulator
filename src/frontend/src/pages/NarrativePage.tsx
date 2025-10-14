import React, { useState, useEffect } from 'react'
import { Helmet } from 'react-helmet-async'
import { FileText, BarChart, TrendingUp, Settings, Info } from 'lucide-react'
import SimulationNarrative from '@/components/narrative/SimulationNarrative'
import BenchmarkNarrative from '@/components/narrative/BenchmarkNarrative'
import NarrativeBuilder from '@/components/narrative/NarrativeBuilder'

interface NarrativePageProps {
  simulationData?: any
  benchmarkData?: any
}

const NarrativePage: React.FC<NarrativePageProps> = ({
  simulationData,
  benchmarkData
}) => {
  const [activeTab, setActiveTab] = useState<'simulation' | 'benchmark' | 'custom'>('simulation')
  const [hasSimulationData, setHasSimulationData] = useState(false)
  const [hasBenchmarkData, setHasBenchmarkData] = useState(false)

  useEffect(() => {
    setHasSimulationData(!!simulationData && Object.keys(simulationData).length > 0)
    setHasBenchmarkData(!!benchmarkData && Object.keys(benchmarkData).length > 0)
    
    // Auto-select tab based on available data
    if (hasSimulationData && !hasBenchmarkData) {
      setActiveTab('simulation')
    } else if (hasBenchmarkData && !hasSimulationData) {
      setActiveTab('benchmark')
    } else if (hasSimulationData && hasBenchmarkData) {
      setActiveTab('simulation') // Default to simulation if both available
    }
  }, [simulationData, benchmarkData, hasSimulationData, hasBenchmarkData])

  const tabs = [
    {
      id: 'simulation' as const,
      name: 'Simulation Narrative',
      description: 'Generate narratives from policy simulation results',
      icon: TrendingUp,
      available: hasSimulationData,
      badge: hasSimulationData ? 'Data Available' : 'No Data'
    },
    {
      id: 'benchmark' as const,
      name: 'Benchmark Narrative',
      description: 'Generate narratives from country comparisons',
      icon: BarChart,
      available: hasBenchmarkData,
      badge: hasBenchmarkData ? 'Data Available' : 'No Data'
    },
    {
      id: 'custom' as const,
      name: 'Custom Narrative',
      description: 'Generate narratives from custom data',
      icon: FileText,
      available: true,
      badge: 'Always Available'
    }
  ]

  const handleNarrativeGenerated = (narrative: any) => {
    console.log('Narrative generated:', narrative)
    // Here you could save to state, show notifications, etc.
  }

  return (
    <>
      <Helmet>
        <title>Narrative Generator - Policy Simulation Assistant</title>
        <meta name="description" content="Transform data into compelling policy narratives using AI-powered narrative generation." />
      </Helmet>

      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Narrative Generator
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Transform your data into compelling, actionable policy narratives using AI-powered 
              narrative generation. Create executive summaries, detailed reports, and presentations 
              tailored to your audience.
            </p>
          </div>

          {/* Tab Navigation */}
          <div className="mb-8">
            <div className="border-b border-gray-200">
              <nav className="-mb-px flex space-x-8">
                {tabs.map((tab) => {
                  const IconComponent = tab.icon
                  return (
                    <button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id)}
                      disabled={!tab.available && tab.id !== 'custom'}
                      className={`py-2 px-1 border-b-2 font-medium text-sm flex items-center space-x-2 ${
                        activeTab === tab.id
                          ? 'border-purple-500 text-purple-600'
                          : tab.available
                          ? 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                          : 'border-transparent text-gray-300 cursor-not-allowed'
                      }`}
                    >
                      <IconComponent className="w-4 h-4" />
                      <span>{tab.name}</span>
                      <span className={`px-2 py-1 text-xs rounded-full ${
                        tab.available 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-gray-100 text-gray-500'
                      }`}>
                        {tab.badge}
                      </span>
                    </button>
                  )
                })}
              </nav>
            </div>
          </div>

          {/* Tab Content */}
          <div className="space-y-6">
            {activeTab === 'simulation' && (
              <SimulationNarrative
                simulationData={simulationData}
                onNarrativeGenerated={handleNarrativeGenerated}
              />
            )}

            {activeTab === 'benchmark' && (
              <BenchmarkNarrative
                benchmarkData={benchmarkData}
                onNarrativeGenerated={handleNarrativeGenerated}
              />
            )}

            {activeTab === 'custom' && (
              <NarrativeBuilder
                onNarrativeGenerated={handleNarrativeGenerated}
              />
            )}
          </div>

          {/* Info Cards */}
          <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="card p-6">
              <div className="flex items-center space-x-3 mb-4">
                <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                  <FileText className="w-5 h-5 text-purple-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900">
                  AI-Powered Generation
                </h3>
              </div>
              <p className="text-gray-600 text-sm">
                Our advanced AI analyzes your data and generates contextually appropriate narratives 
                tailored to your specific audience and requirements.
              </p>
            </div>

            <div className="card p-6">
              <div className="flex items-center space-x-3 mb-4">
                <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                  <Settings className="w-5 h-5 text-blue-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900">
                  Customizable Templates
                </h3>
              </div>
              <p className="text-gray-600 text-sm">
                Choose from multiple narrative types, adjust tone and length, and focus on specific 
                areas that matter most to your stakeholders.
              </p>
            </div>

            <div className="card p-6">
              <div className="flex items-center space-x-3 mb-4">
                <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                  <Info className="w-5 h-5 text-green-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900">
                  Quality Assurance
                </h3>
              </div>
              <p className="text-gray-600 text-sm">
                Every narrative includes quality metrics, proper citations, and actionable recommendations 
                to ensure maximum impact and credibility.
              </p>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}

export default NarrativePage