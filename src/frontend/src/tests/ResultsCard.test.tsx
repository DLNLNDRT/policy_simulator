/**
 * Tests for ResultsCard component
 */

import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import ResultsCardNew from '../components/simulation/ResultsCardNew';

const mockResults = {
  simulation_id: 'test-simulation-123',
  country: 'PRT',
  timestamp: '2025-10-11T10:00:00Z',
  baseline: {
    life_expectancy: 81.2,
    doctor_density: 2.1,
    nurse_density: 5.2,
    health_spending: 5.8,
    year: 2022
  },
  parameters: {
    doctor_density: 2.5,
    nurse_density: 5.8,
    health_spending: 6.2
  },
  prediction: {
    life_expectancy: 82.1,
    change: 0.9,
    change_percentage: 1.1,
    confidence_interval: {
      lower: 81.4,
      upper: 82.8,
      margin_of_error: 0.7
    },
    feature_contributions: {
      doctor_density: 0.3,
      nurse_density: 0.4,
      health_spending: 0.2,
      intercept: 80.0
    }
  },
  model_metrics: {
    r2_score: 0.78,
    mse: 0.5,
    rmse: 0.7,
    training_samples: 100,
    test_samples: 25
  },
  metadata: {
    model_version: 'v1.0',
    execution_time: 1.2,
    data_quality: 98.4
  }
};

describe('ResultsCardNew', () => {
  it('renders empty state when no results', () => {
    const mockOnExport = jest.fn();
    
    render(
      <ResultsCardNew 
        results={null}
        onExport={mockOnExport}
      />
    );

    expect(screen.getByText('Simulation Results')).toBeInTheDocument();
    expect(screen.getByText('No simulation results yet')).toBeInTheDocument();
    expect(screen.getByText('Configure parameters and run a simulation to see results')).toBeInTheDocument();
  });

  it('renders simulation results when provided', () => {
    const mockOnExport = jest.fn();
    
    render(
      <ResultsCardNew 
        results={mockResults}
        onExport={mockOnExport}
      />
    );

    expect(screen.getByText('Simulation Results')).toBeInTheDocument();
    expect(screen.getByText('Predicted impact of policy changes on life expectancy')).toBeInTheDocument();
    
    // Check main prediction display
    expect(screen.getByText('Predicted Life Expectancy')).toBeInTheDocument();
    expect(screen.getByText('81.2')).toBeInTheDocument(); // Baseline
    expect(screen.getByText('82.1')).toBeInTheDocument(); // Predicted
    expect(screen.getByText('+0.90 years')).toBeInTheDocument(); // Change
    
    // Check confidence interval
    expect(screen.getByText('Confidence Interval (95%)')).toBeInTheDocument();
    expect(screen.getByText('81.4 - 82.8 years')).toBeInTheDocument();
    expect(screen.getByText('(±0.7 years)')).toBeInTheDocument();
  });

  it('displays parameter changes correctly', () => {
    const mockOnExport = jest.fn();
    
    render(
      <ResultsCardNew 
        results={mockResults}
        onExport={mockOnExport}
      />
    );

    expect(screen.getByText('Parameter Changes')).toBeInTheDocument();
    
    // Check parameter changes
    expect(screen.getByText('2.1 → 2.5')).toBeInTheDocument(); // Doctor density
    expect(screen.getByText('5.2 → 5.8')).toBeInTheDocument(); // Nurse density
    expect(screen.getByText('5.8% → 6.2%')).toBeInTheDocument(); // Health spending
  });

  it('displays feature contributions', () => {
    const mockOnExport = jest.fn();
    
    render(
      <ResultsCardNew 
        results={mockResults}
        onExport={mockOnExport}
      />
    );

    expect(screen.getByText('Feature Contributions')).toBeInTheDocument();
    
    // Check feature contributions
    expect(screen.getByText('+0.300 years')).toBeInTheDocument(); // Doctor density impact
    expect(screen.getByText('+0.400 years')).toBeInTheDocument(); // Nurse density impact
    expect(screen.getByText('+0.200 years')).toBeInTheDocument(); // Health spending impact
    expect(screen.getByText('80.000 years')).toBeInTheDocument(); // Intercept
  });

  it('displays model information', () => {
    const mockOnExport = jest.fn();
    
    render(
      <ResultsCardNew 
        results={mockResults}
        onExport={mockOnExport}
      />
    );

    expect(screen.getByText('Model Information')).toBeInTheDocument();
    
    // Check model metrics
    expect(screen.getByText('v1.0')).toBeInTheDocument(); // Model version
    expect(screen.getByText('98.4/100')).toBeInTheDocument(); // Data quality
    expect(screen.getByText('0.780')).toBeInTheDocument(); // R² score
    expect(screen.getByText('1.20s')).toBeInTheDocument(); // Execution time
  });

  it('calls onExport with correct format when export buttons are clicked', () => {
    const mockOnExport = jest.fn();
    
    render(
      <ResultsCardNew 
        results={mockResults}
        onExport={mockOnExport}
      />
    );

    // Test PDF export
    const pdfButton = screen.getByText('Export PDF');
    fireEvent.click(pdfButton);
    expect(mockOnExport).toHaveBeenCalledWith('pdf');

    // Test CSV export
    const csvButton = screen.getByText('Export CSV');
    fireEvent.click(csvButton);
    expect(mockOnExport).toHaveBeenCalledWith('csv');

    // Test Image export
    const imageButton = screen.getByText('Export Image');
    fireEvent.click(imageButton);
    expect(mockOnExport).toHaveBeenCalledWith('image');
  });

  it('displays negative change correctly', () => {
    const negativeResults = {
      ...mockResults,
      prediction: {
        ...mockResults.prediction,
        life_expectancy: 80.5,
        change: -0.7,
        change_percentage: -0.9
      }
    };

    const mockOnExport = jest.fn();
    
    render(
      <ResultsCardNew 
        results={negativeResults}
        onExport={mockOnExport}
      />
    );

    expect(screen.getByText('80.5')).toBeInTheDocument(); // Predicted
    expect(screen.getByText('-0.70 years')).toBeInTheDocument(); // Negative change
  });

  it('displays model confidence percentage', () => {
    const mockOnExport = jest.fn();
    
    render(
      <ResultsCardNew 
        results={mockResults}
        onExport={mockOnExport}
      />
    );

    expect(screen.getByText('Model Confidence: 78.0%')).toBeInTheDocument();
  });
});
