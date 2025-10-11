import React from 'react';
import { TrendingUp, TrendingDown, Target, Download, BarChart3 } from 'lucide-react';

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

interface ResultsCardProps {
  results: SimulationResults | null;
  onExport: (format: 'pdf' | 'csv' | 'image') => void;
}

const ResultsCardNew: React.FC<ResultsCardProps> = ({ results, onExport }) => {
  if (!results) {
    return (
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Simulation Results</h2>
          <p className="card-description">
            Run a simulation to see predicted outcomes
          </p>
        </div>
        <div className="card-content">
          <div className="text-center py-12 text-gray-500">
            <BarChart3 className="w-12 h-12 mx-auto mb-4 text-gray-300" />
            <p>No simulation results yet</p>
            <p className="text-sm">Configure parameters and run a simulation to see results</p>
          </div>
        </div>
      </div>
    );
  }

  const formatChange = (change: number) => {
    const isPositive = change >= 0;
    const icon = isPositive ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />;
    const color = isPositive ? 'text-green-600' : 'text-red-600';
    const bgColor = isPositive ? 'bg-green-50' : 'bg-red-50';
    
    return (
      <div className={`inline-flex items-center space-x-1 px-2 py-1 rounded-full ${bgColor}`}>
        {icon}
        <span className={`text-sm font-medium ${color}`}>
          {isPositive ? '+' : ''}{change.toFixed(2)} years
        </span>
      </div>
    );
  };

  return (
    <div className="card">
      <div className="card-header">
        <h2 className="card-title">Simulation Results</h2>
        <p className="card-description">
          Predicted impact of policy changes on life expectancy
        </p>
      </div>
      
      <div className="card-content space-y-6">
        {/* Main Prediction */}
        <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-lg border border-blue-200">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-800">Predicted Life Expectancy</h3>
            <div className="flex items-center space-x-2">
              <Target className="w-5 h-5 text-blue-600" />
              <span className="text-sm text-gray-600">Model Confidence: {(results.model_metrics.r2_score * 100).toFixed(1)}%</span>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">
                {results.baseline.life_expectancy.toFixed(1)}
              </div>
              <div className="text-sm text-gray-600">Baseline (years)</div>
            </div>
            
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-600">
                {results.prediction.life_expectancy.toFixed(1)}
              </div>
              <div className="text-sm text-gray-600">Predicted (years)</div>
            </div>
            
            <div className="text-center">
              <div className="text-xl">
                {formatChange(results.prediction.change)}
              </div>
              <div className="text-sm text-gray-600">Change</div>
            </div>
          </div>
        </div>

        {/* Confidence Interval */}
        <div className="bg-gray-50 p-4 rounded-lg">
          <h4 className="font-medium text-gray-800 mb-2">Confidence Interval (95%)</h4>
          <div className="flex items-center space-x-4 text-sm">
            <span className="text-gray-600">Range:</span>
            <span className="font-medium">
              {results.prediction.confidence_interval.lower.toFixed(1)} - {results.prediction.confidence_interval.upper.toFixed(1)} years
            </span>
            <span className="text-gray-500">
              (±{results.prediction.confidence_interval.margin_of_error.toFixed(1)} years)
            </span>
          </div>
        </div>

        {/* Parameter Changes */}
        <div>
          <h4 className="font-medium text-gray-800 mb-3">Parameter Changes</h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-white p-4 rounded-lg border">
              <div className="text-sm text-gray-600">Doctor Density</div>
              <div className="text-lg font-semibold">
                {results.baseline.doctor_density.toFixed(1)} → {results.parameters.doctor_density.toFixed(1)}
              </div>
              <div className="text-xs text-gray-500">per 1,000 population</div>
            </div>
            
            <div className="bg-white p-4 rounded-lg border">
              <div className="text-sm text-gray-600">Nurse Density</div>
              <div className="text-lg font-semibold">
                {results.baseline.nurse_density.toFixed(1)} → {results.parameters.nurse_density.toFixed(1)}
              </div>
              <div className="text-xs text-gray-500">per 1,000 population</div>
            </div>
            
            <div className="bg-white p-4 rounded-lg border">
              <div className="text-sm text-gray-600">Health Spending</div>
              <div className="text-lg font-semibold">
                {results.baseline.health_spending.toFixed(1)}% → {results.parameters.health_spending.toFixed(1)}%
              </div>
              <div className="text-xs text-gray-500">of GDP</div>
            </div>
          </div>
        </div>

        {/* Feature Contributions */}
        <div>
          <h4 className="font-medium text-gray-800 mb-3">Feature Contributions</h4>
          <div className="space-y-2">
            <div className="flex justify-between items-center py-2 border-b border-gray-100">
              <span className="text-sm text-gray-600">Doctor Density Impact</span>
              <span className="font-medium">
                {results.prediction.feature_contributions.doctor_density >= 0 ? '+' : ''}
                {results.prediction.feature_contributions.doctor_density.toFixed(3)} years
              </span>
            </div>
            <div className="flex justify-between items-center py-2 border-b border-gray-100">
              <span className="text-sm text-gray-600">Nurse Density Impact</span>
              <span className="font-medium">
                {results.prediction.feature_contributions.nurse_density >= 0 ? '+' : ''}
                {results.prediction.feature_contributions.nurse_density.toFixed(3)} years
              </span>
            </div>
            <div className="flex justify-between items-center py-2 border-b border-gray-100">
              <span className="text-sm text-gray-600">Health Spending Impact</span>
              <span className="font-medium">
                {results.prediction.feature_contributions.health_spending >= 0 ? '+' : ''}
                {results.prediction.feature_contributions.health_spending.toFixed(3)} years
              </span>
            </div>
            <div className="flex justify-between items-center py-2">
              <span className="text-sm text-gray-600">Baseline (Intercept)</span>
              <span className="font-medium">
                {results.prediction.feature_contributions.intercept.toFixed(3)} years
              </span>
            </div>
          </div>
        </div>

        {/* Model Information */}
        <div className="bg-gray-50 p-4 rounded-lg">
          <h4 className="font-medium text-gray-800 mb-2">Model Information</h4>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span className="text-gray-600">Model Version:</span>
              <span className="ml-2 font-medium">{results.metadata.model_version}</span>
            </div>
            <div>
              <span className="text-gray-600">Data Quality:</span>
              <span className="ml-2 font-medium">{results.metadata.data_quality.toFixed(1)}/100</span>
            </div>
            <div>
              <span className="text-gray-600">R² Score:</span>
              <span className="ml-2 font-medium">{results.model_metrics.r2_score.toFixed(3)}</span>
            </div>
            <div>
              <span className="text-gray-600">Execution Time:</span>
              <span className="ml-2 font-medium">{results.metadata.execution_time.toFixed(2)}s</span>
            </div>
          </div>
        </div>
      </div>

      <div className="card-footer">
        <div className="flex space-x-3">
          <button
            onClick={() => onExport('pdf')}
            className="btn-outline inline-flex items-center space-x-2"
          >
            <Download className="w-4 h-4" />
            <span>Export PDF</span>
          </button>
          
          <button
            onClick={() => onExport('csv')}
            className="btn-outline inline-flex items-center space-x-2"
          >
            <Download className="w-4 h-4" />
            <span>Export CSV</span>
          </button>
          
          <button
            onClick={() => onExport('image')}
            className="btn-outline inline-flex items-center space-x-2"
          >
            <Download className="w-4 h-4" />
            <span>Export Image</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default ResultsCardNew;
