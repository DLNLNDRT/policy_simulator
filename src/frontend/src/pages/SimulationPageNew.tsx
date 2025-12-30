import React, { useState } from 'react';
import { Helmet } from 'react-helmet-async';
import { 
  Play, 
  RotateCcw, 
  Download, 
  Info,
  AlertTriangle,
  CheckCircle,
  Clock
} from 'lucide-react';
import SimulationCardNew from '../components/simulation/SimulationCardNew';
import ResultsCardNew from '../components/simulation/ResultsCardNew';
import NarrativeCard from '../components/simulation/NarrativeCard';
import ChartCard from '../components/simulation/ChartCard';

interface SimulationParameters {
  doctor_density: number;
  nurse_density: number;
  health_spending: number;
}

interface SimulationResults {
  simulation_id: string;
  country: string;
  timestamp: string;
  baseline: {
    life_expectancy: number;
    doctor_density: number;
    nurse_density: number;
    health_spending: number;
    year: number;
  };
  parameters: {
    doctor_density: number;
    nurse_density: number;
    health_spending: number;
  };
  prediction: {
    life_expectancy: number;
    change: number;
    change_percentage: number;
    confidence_interval: {
      lower: number;
      upper: number;
      margin_of_error: number;
    };
    feature_contributions: {
      doctor_density: number;
      nurse_density: number;
      health_spending: number;
      intercept: number;
    };
  };
  model_metrics: {
    r2_score: number;
    mse: number;
    rmse: number;
    training_samples: number;
    test_samples: number;
  };
  metadata: {
    model_version: string;
    execution_time: number;
    data_quality: number;
  };
}

const SimulationPageNew: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState<SimulationResults | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleRunSimulation = async (country: string, parameters: SimulationParameters) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await fetch('/api/simulations/run', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          country,
          parameters
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      console.error('Error running simulation:', err);
      setError(err instanceof Error ? err.message : 'An error occurred while running the simulation');
    } finally {
      setIsLoading(false);
    }
  };

  const handleExport = (format: 'pdf' | 'csv' | 'image') => {
    if (!results) return;
    
    // TODO: Implement export functionality
    console.log(`Exporting results as ${format}`, results);
    alert(`Export functionality for ${format} will be implemented in the next phase.`);
  };

  const handleReset = () => {
    setResults(null);
    setError(null);
  };

  return (
    <>
      <Helmet>
        <title>Policy Simulation - Policy Simulation Assistant</title>
        <meta name="description" content="Run interactive policy simulations to predict the impact of healthcare workforce and spending changes on life expectancy outcomes." />
      </Helmet>

      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Policy Simulation
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Explore the potential impact of healthcare workforce and spending changes 
              on life expectancy outcomes using our AI-powered simulation engine.
            </p>
          </div>

          {/* Error Display */}
          {error && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
              <div className="flex">
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-red-800">Simulation Error</h3>
                  <div className="mt-2 text-sm text-red-700">
                    <p>{error}</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Simulation Controls */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
            {/* Simulation Parameters */}
            <div className="lg:col-span-1">
              <SimulationCardNew 
                onRunSimulation={handleRunSimulation}
                isLoading={isLoading}
              />
            </div>

            {/* Results */}
            <div className="lg:col-span-2 space-y-6">
              {results ? (
                <>
                  <ResultsCardNew 
                    results={results}
                    onExport={handleExport}
                  />
                  <ChartCard 
                    baseline={results.baseline.life_expectancy} 
                    predicted={results.prediction.life_expectancy}
                    confidenceInterval={[results.prediction.confidence_interval.lower, results.prediction.confidence_interval.upper]}
                  />
                  <NarrativeCard 
                    narrative={`Based on the simulation for ${results.country}, the predicted life expectancy change of ${results.prediction.change >= 0 ? '+' : ''}${results.prediction.change.toFixed(2)} years represents a ${results.prediction.change_percentage >= 0 ? 'positive' : 'negative'} impact from the proposed policy changes.`}
                    disclaimers={[
                      'This is a statistical prediction based on historical data correlations',
                      'Results should not be considered as clinical recommendations',
                      'Actual outcomes may vary due to numerous factors not included in this model',
                      'Please consult with healthcare professionals for policy decisions'
                    ]}
                    citations={[
                      'WHO Global Health Observatory 2023',
                    ]}
                  />
                </>
              ) : (
                <div className="card p-8 text-center">
                  <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Play className="w-8 h-8 text-gray-400" />
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    Ready to Run Simulation
                  </h3>
                  <p className="text-gray-600">
                    Select a country and adjust the parameters, then click "Run Simulation" to see predicted outcomes 
                    for your policy changes.
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Info Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="card p-6">
              <div className="flex items-center space-x-3 mb-4">
                <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                  <Info className="w-5 h-5 text-blue-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900">
                  How It Works
                </h3>
              </div>
              <p className="text-gray-600 text-sm">
                Our simulation engine uses regression models trained on WHO data 
                to predict life expectancy changes based on workforce and spending modifications.
              </p>
            </div>

            <div className="card p-6">
              <div className="flex items-center space-x-3 mb-4">
                <div className="w-10 h-10 bg-yellow-100 rounded-lg flex items-center justify-center">
                  <AlertTriangle className="w-5 h-5 text-yellow-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900">
                  Important Disclaimers
                </h3>
              </div>
              <p className="text-gray-600 text-sm">
                Results are statistical predictions for exploratory analysis only. 
                Not intended for clinical decision-making or policy implementation without expert review.
              </p>
            </div>

            <div className="card p-6">
              <div className="flex items-center space-x-3 mb-4">
                <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                  <CheckCircle className="w-5 h-5 text-green-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900">
                  Data Quality
                </h3>
              </div>
              <p className="text-gray-600 text-sm">
                All simulations use validated data with 98.4% quality score. 
                Sources include WHO Global Health Observatory datasets.
              </p>
            </div>
          </div>

          {/* Reset Button */}
          {results && (
            <div className="mt-8 text-center">
              <button
                onClick={handleReset}
                className="btn-outline btn-lg inline-flex items-center space-x-2"
              >
                <RotateCcw className="w-5 h-5" />
                <span>Run New Simulation</span>
              </button>
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default SimulationPageNew;
