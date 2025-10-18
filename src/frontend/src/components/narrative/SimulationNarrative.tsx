import React, { useState, useEffect } from 'react'
import { Play, FileText, TrendingUp, Users, DollarSign } from 'lucide-react'
import NarrativeBuilder from './NarrativeBuilder'
import { NarrativeRequest, NarrativeType, AudienceType, ToneType, LengthType, FocusArea } from '@/types/narrative'

interface SimulationNarrativeProps {
  simulationData?: any // Data from Feature 1 simulation results
  onNarrativeGenerated?: (narrative: any) => void
}

const SimulationNarrative: React.FC<SimulationNarrativeProps> = ({
  simulationData,
  onNarrativeGenerated
}) => {
  const [hasData, setHasData] = useState(false)

  useEffect(() => {
    setHasData(!!simulationData && Object.keys(simulationData).length > 0)
  }, [simulationData])

  // Transform simulation data for narrative generation
  const transformSimulationData = (data: any) => {
    if (!data) return {}

    return {
      country: data.country || 'Unknown',
      baseline_life_expectancy: data.baseline?.life_expectancy || 0,
      predicted_change: data.prediction?.change || 0,
      new_life_expectancy: data.prediction?.life_expectancy || 0,
      confidence_interval: data.prediction?.confidence_interval || {},
      doctor_density_change: data.parameters?.doctor_density || 0,
      nurse_density_change: data.parameters?.nurse_density || 0,
      spending_change: data.parameters?.health_spending || 0,
      gender: data.gender || 'BOTH',
      model_confidence: data.prediction?.confidence_score || 0,
      response_time: data.response_time_ms || 0,
      cost: data.cost_usd || 0
    }
  }

  const defaultNarrativeRequest = {
    simulation_results: simulationData || {},
    template: "policy_insight",
    audience: "policy_makers"
  }

  if (!hasData) {
    return (
      <div className="card">
        <div className="card-content text-center py-12">
          <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <Play className="w-8 h-8 text-gray-400" />
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            No Simulation Data Available
          </h3>
          <p className="text-gray-600 mb-6">
            Run a policy simulation first to generate a narrative about the predicted impact.
          </p>
          <div className="space-y-2 text-sm text-gray-500">
            <p>• Go to Feature 1: Policy Simulation</p>
            <p>• Run a simulation with your desired parameters</p>
            <p>• Return here to generate a narrative</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Simulation Data Summary */}
      <div className="card">
        <div className="card-header">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
              <TrendingUp className="w-4 h-4 text-blue-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900">Simulation Results</h3>
              <p className="text-sm text-gray-600">Data from your policy simulation</p>
            </div>
          </div>
        </div>
        
        <div className="card-content">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center p-3 bg-blue-50 rounded-lg">
              <div className="text-lg font-semibold text-blue-900">
                {simulationData.country || 'N/A'}
              </div>
              <div className="text-xs text-blue-600">Country</div>
            </div>
            
            <div className="text-center p-3 bg-green-50 rounded-lg">
              <div className="text-lg font-semibold text-green-900">
                {simulationData.prediction?.change > 0 ? '+' : ''}{simulationData.prediction?.change?.toFixed(2) || '0.00'} years
              </div>
              <div className="text-xs text-green-600">Predicted Change</div>
            </div>
            
            <div className="text-center p-3 bg-purple-50 rounded-lg">
              <div className="text-lg font-semibold text-purple-900">
                {simulationData.prediction?.life_expectancy?.toFixed(1) || '0.0'} years
              </div>
              <div className="text-xs text-purple-600">New Life Expectancy</div>
            </div>
            
            <div className="text-center p-3 bg-yellow-50 rounded-lg">
              <div className="text-lg font-semibold text-yellow-900">
                {simulationData.prediction?.confidence_score ? (simulationData.prediction.confidence_score * 100).toFixed(0) : '0'}%
              </div>
              <div className="text-xs text-yellow-600">Confidence</div>
            </div>
          </div>
          
          {/* Policy Changes */}
          <div className="mt-4 pt-4 border-t border-gray-200">
            <h4 className="text-sm font-medium text-gray-900 mb-3">Policy Changes</h4>
            <div className="grid grid-cols-3 gap-4">
              <div className="flex items-center space-x-2">
                <Users className="w-4 h-4 text-gray-500" />
                <div>
                  <div className="text-sm font-medium text-gray-900">
                    {simulationData.parameters?.doctor_density > 0 ? '+' : ''}{simulationData.parameters?.doctor_density || 0}
                  </div>
                  <div className="text-xs text-gray-500">Doctors/1k</div>
                </div>
              </div>
              
              <div className="flex items-center space-x-2">
                <Users className="w-4 h-4 text-gray-500" />
                <div>
                  <div className="text-sm font-medium text-gray-900">
                    {simulationData.parameters?.nurse_density > 0 ? '+' : ''}{simulationData.parameters?.nurse_density || 0}
                  </div>
                  <div className="text-xs text-gray-500">Nurses/1k</div>
                </div>
              </div>
              
              <div className="flex items-center space-x-2">
                <DollarSign className="w-4 h-4 text-gray-500" />
                <div>
                  <div className="text-sm font-medium text-gray-900">
                    {simulationData.parameters?.health_spending > 0 ? '+' : ''}{simulationData.parameters?.health_spending || 0}%
                  </div>
                  <div className="text-xs text-gray-500">Health Spending</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Narrative Builder */}
      <NarrativeBuilder
        dataSource={simulationData}
        onNarrativeGenerated={onNarrativeGenerated}
      />
    </div>
  )
}

export default SimulationNarrative
