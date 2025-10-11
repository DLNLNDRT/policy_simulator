import React, { useState, useEffect } from 'react';
import { Play, RotateCcw, Globe, Users, DollarSign } from 'lucide-react';

interface SimulationParameters {
  doctor_density: number;
  nurse_density: number;
  health_spending: number;
}

interface CountryInfo {
  code: string;
  name: string;
  baseline: {
    life_expectancy: number;
    doctor_density: number;
    nurse_density: number;
    health_spending: number;
    year: number;
  };
  data_quality: number;
}

interface SimulationCardProps {
  onRunSimulation: (country: string, parameters: SimulationParameters) => void;
  isLoading: boolean;
}

const SimulationCardNew: React.FC<SimulationCardProps> = ({ onRunSimulation, isLoading }) => {
  const [countries, setCountries] = useState<CountryInfo[]>([]);
  const [selectedCountry, setSelectedCountry] = useState<string>('');
  const [parameters, setParameters] = useState<SimulationParameters>({
    doctor_density: 0,
    nurse_density: 0,
    health_spending: 0
  });
  const [baselineData, setBaselineData] = useState<CountryInfo['baseline'] | null>(null);

  // Load countries on component mount
  useEffect(() => {
    const loadCountries = async () => {
      try {
        const response = await fetch('/api/simulations/countries');
        const data = await response.json();
        setCountries(data.countries);
        
        // Set default country
        if (data.countries.length > 0) {
          setSelectedCountry(data.countries[0].code);
          setBaselineData(data.countries[0].baseline);
          setParameters({
            doctor_density: data.countries[0].baseline.doctor_density,
            nurse_density: data.countries[0].baseline.nurse_density,
            health_spending: data.countries[0].baseline.health_spending
          });
        }
      } catch (error) {
        console.error('Error loading countries:', error);
      }
    };

    loadCountries();
  }, []);

  // Update parameters when country changes
  useEffect(() => {
    const country = countries.find(c => c.code === selectedCountry);
    if (country) {
      setBaselineData(country.baseline);
      setParameters({
        doctor_density: country.baseline.doctor_density,
        nurse_density: country.baseline.nurse_density,
        health_spending: country.baseline.health_spending
      });
    }
  }, [selectedCountry, countries]);

  const handleParameterChange = (param: keyof SimulationParameters, value: number) => {
    setParameters(prev => ({
      ...prev,
      [param]: value
    }));
  };

  const handleRunSimulation = () => {
    if (selectedCountry && parameters) {
      onRunSimulation(selectedCountry, parameters);
    }
  };

  const handleReset = () => {
    if (baselineData) {
      setParameters({
        doctor_density: baselineData.doctor_density,
        nurse_density: baselineData.nurse_density,
        health_spending: baselineData.health_spending
      });
    }
  };

  return (
    <div className="card">
      <div className="card-header">
        <h2 className="card-title">Policy Simulation</h2>
        <p className="card-description">
          Configure your policy simulation parameters
        </p>
      </div>
      
      <div className="card-content space-y-6">
        {/* Country Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <Globe className="w-4 h-4 inline mr-2" />
            Select Country
          </label>
          <select
            value={selectedCountry}
            onChange={(e) => setSelectedCountry(e.target.value)}
            className="select w-full"
            disabled={isLoading}
          >
            {countries.map(country => (
              <option key={country.code} value={country.code}>
                {country.name} (Baseline: {country.baseline.life_expectancy.toFixed(1)} years)
              </option>
            ))}
          </select>
        </div>

        {/* Baseline Information */}
        {baselineData && (
          <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
            <h4 className="font-medium text-blue-800 mb-2">Baseline Data ({baselineData.year})</h4>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-blue-600">Life Expectancy:</span>
                <span className="ml-2 font-medium">{baselineData.life_expectancy.toFixed(1)} years</span>
              </div>
              <div>
                <span className="text-blue-600">Doctors:</span>
                <span className="ml-2 font-medium">{baselineData.doctor_density.toFixed(1)}/1k</span>
              </div>
              <div>
                <span className="text-blue-600">Nurses:</span>
                <span className="ml-2 font-medium">{baselineData.nurse_density.toFixed(1)}/1k</span>
              </div>
              <div>
                <span className="text-blue-600">Health Spending:</span>
                <span className="ml-2 font-medium">{baselineData.health_spending.toFixed(1)}% GDP</span>
              </div>
            </div>
          </div>
        )}

        {/* Doctor Density */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <Users className="w-4 h-4 inline mr-2" />
            Doctor Density: {parameters.doctor_density.toFixed(1)} per 1,000 population
          </label>
          <div className="space-y-2">
            <input
              type="range"
              min="0"
              max="10"
              step="0.1"
              value={parameters.doctor_density}
              onChange={(e) => handleParameterChange('doctor_density', parseFloat(e.target.value))}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
              disabled={isLoading}
            />
            <div className="flex justify-between text-sm text-gray-600">
              <span>0</span>
              <span>10</span>
            </div>
          </div>
        </div>

        {/* Nurse Density */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <Users className="w-4 h-4 inline mr-2" />
            Nurse Density: {parameters.nurse_density.toFixed(1)} per 1,000 population
          </label>
          <div className="space-y-2">
            <input
              type="range"
              min="0"
              max="20"
              step="0.1"
              value={parameters.nurse_density}
              onChange={(e) => handleParameterChange('nurse_density', parseFloat(e.target.value))}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
              disabled={isLoading}
            />
            <div className="flex justify-between text-sm text-gray-600">
              <span>0</span>
              <span>20</span>
            </div>
          </div>
        </div>

        {/* Health Spending */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <DollarSign className="w-4 h-4 inline mr-2" />
            Government Health Spending: {parameters.health_spending.toFixed(1)}% of GDP
          </label>
          <div className="space-y-2">
            <input
              type="range"
              min="0"
              max="15"
              step="0.1"
              value={parameters.health_spending}
              onChange={(e) => handleParameterChange('health_spending', parseFloat(e.target.value))}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
              disabled={isLoading}
            />
            <div className="flex justify-between text-sm text-gray-600">
              <span>0%</span>
              <span>15%</span>
            </div>
          </div>
        </div>
      </div>

      <div className="card-footer">
        <div className="flex space-x-3 w-full">
          <button
            onClick={handleRunSimulation}
            disabled={isLoading || !selectedCountry}
            className="btn-primary flex-1 inline-flex items-center justify-center space-x-2"
          >
            {isLoading ? (
              <>
                <div className="loading-spinner w-4 h-4" />
                <span>Running Simulation...</span>
              </>
            ) : (
              <>
                <Play className="w-4 h-4" />
                <span>Run Simulation</span>
              </>
            )}
          </button>
          
          <button
            onClick={handleReset}
            disabled={isLoading}
            className="btn-outline inline-flex items-center justify-center space-x-2"
          >
            <RotateCcw className="w-4 h-4" />
            <span>Reset</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default SimulationCardNew;
