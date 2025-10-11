import React from 'react'
import { Play, RotateCcw, Globe, Users, DollarSign } from 'lucide-react'

interface SimulationParams {
  country: string
  doctorDensityChange: number
  nurseDensityChange: number
  spendingChange: number
}

interface Country {
  code: string
  name: string
}

interface SimulationCardProps {
  params: SimulationParams
  onParamsChange: (params: SimulationParams) => void
  countries: Country[]
  isRunning: boolean
  onRun: () => void
  onReset: () => void
}

const SimulationCard: React.FC<SimulationCardProps> = ({
  params,
  onParamsChange,
  countries,
  isRunning,
  onRun,
  onReset
}) => {
  const handleCountryChange = (country: string) => {
    onParamsChange({ ...params, country })
  }

  const handleParameterChange = (param: keyof Omit<SimulationParams, 'country'>, value: number) => {
    onParamsChange({ ...params, [param]: value })
  }

  const formatValue = (value: number) => {
    return value > 0 ? `+${value.toFixed(1)}` : value.toFixed(1)
  }

  return (
    <div className="card">
      <div className="card-header">
        <h2 className="card-title">Simulation Parameters</h2>
        <p className="card-description">
          Configure your policy simulation parameters
        </p>
      </div>
      
      <div className="card-content space-y-6">
        {/* Country Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <Globe className="w-4 h-4 inline mr-2" />
            Country
          </label>
          <select
            value={params.country}
            onChange={(e) => handleCountryChange(e.target.value)}
            className="select w-full"
            disabled={isRunning}
          >
            {countries.map((country) => (
              <option key={country.code} value={country.name}>
                {country.name}
              </option>
            ))}
          </select>
        </div>

        {/* Doctor Density Change */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <Users className="w-4 h-4 inline mr-2" />
            Doctor Density Change
            <span className="text-gray-500 ml-1">(per 10,000 population)</span>
          </label>
          <div className="space-y-2">
            <input
              type="range"
              min="-5"
              max="5"
              step="0.1"
              value={params.doctorDensityChange}
              onChange={(e) => handleParameterChange('doctorDensityChange', parseFloat(e.target.value))}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
              disabled={isRunning}
            />
            <div className="flex justify-between text-sm text-gray-600">
              <span>-5.0</span>
              <span className="font-medium text-gray-900">
                {formatValue(params.doctorDensityChange)}
              </span>
              <span>+5.0</span>
            </div>
          </div>
        </div>

        {/* Nurse Density Change */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <Users className="w-4 h-4 inline mr-2" />
            Nurse Density Change
            <span className="text-gray-500 ml-1">(per 10,000 population)</span>
          </label>
          <div className="space-y-2">
            <input
              type="range"
              min="-20"
              max="20"
              step="0.5"
              value={params.nurseDensityChange}
              onChange={(e) => handleParameterChange('nurseDensityChange', parseFloat(e.target.value))}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
              disabled={isRunning}
            />
            <div className="flex justify-between text-sm text-gray-600">
              <span>-20.0</span>
              <span className="font-medium text-gray-900">
                {formatValue(params.nurseDensityChange)}
              </span>
              <span>+20.0</span>
            </div>
          </div>
        </div>

        {/* Government Spending Change */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <DollarSign className="w-4 h-4 inline mr-2" />
            Government Spending Change
            <span className="text-gray-500 ml-1">(% of GDP)</span>
          </label>
          <div className="space-y-2">
            <input
              type="range"
              min="-5"
              max="5"
              step="0.1"
              value={params.spendingChange}
              onChange={(e) => handleParameterChange('spendingChange', parseFloat(e.target.value))}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
              disabled={isRunning}
            />
            <div className="flex justify-between text-sm text-gray-600">
              <span>-5.0%</span>
              <span className="font-medium text-gray-900">
                {formatValue(params.spendingChange)}%
              </span>
              <span>+5.0%</span>
            </div>
          </div>
        </div>
      </div>

      <div className="card-footer">
        <div className="flex space-x-3 w-full">
          <button
            onClick={onRun}
            disabled={isRunning}
            className="btn-primary flex-1 inline-flex items-center justify-center space-x-2"
          >
            {isRunning ? (
              <>
                <div className="loading-spinner w-4 h-4" />
                <span>Running...</span>
              </>
            ) : (
              <>
                <Play className="w-4 h-4" />
                <span>Run Simulation</span>
              </>
            )}
          </button>
          
          <button
            onClick={onReset}
            disabled={isRunning}
            className="btn-outline inline-flex items-center justify-center space-x-2"
          >
            <RotateCcw className="w-4 h-4" />
            <span>Reset</span>
          </button>
        </div>
      </div>
    </div>
  )
}

export default SimulationCard
