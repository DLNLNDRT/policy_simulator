/**
 * Tests for SimulationCard component
 */

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import SimulationCardNew from '../components/simulation/SimulationCardNew';

// Mock fetch
global.fetch = jest.fn();

const mockCountries = [
  {
    code: 'PRT',
    name: 'Portugal',
    baseline: {
      life_expectancy: 81.2,
      doctor_density: 2.1,
      nurse_density: 5.2,
      health_spending: 5.8,
      year: 2022
    },
    data_quality: 98.4
  },
  {
    code: 'ESP',
    name: 'Spain',
    baseline: {
      life_expectancy: 83.1,
      doctor_density: 2.8,
      nurse_density: 6.1,
      health_spending: 7.2,
      year: 2022
    },
    data_quality: 98.4
  }
];

describe('SimulationCardNew', () => {
  beforeEach(() => {
    (fetch as jest.Mock).mockResolvedValue({
      ok: true,
      json: async () => ({ countries: mockCountries })
    });
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('renders simulation card with loading state', async () => {
    const mockOnRunSimulation = jest.fn();
    
    render(
      <SimulationCardNew 
        onRunSimulation={mockOnRunSimulation}
        isLoading={false}
      />
    );

    await waitFor(() => {
      expect(screen.getByText('Policy Simulation')).toBeInTheDocument();
    });

    expect(screen.getByText('Select Country')).toBeInTheDocument();
    expect(screen.getByText('Run Simulation')).toBeInTheDocument();
  });

  it('loads countries on mount', async () => {
    const mockOnRunSimulation = jest.fn();
    
    render(
      <SimulationCardNew 
        onRunSimulation={mockOnRunSimulation}
        isLoading={false}
      />
    );

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith('/api/simulations/countries');
    });

    await waitFor(() => {
      expect(screen.getByDisplayValue('Portugal (Baseline: 81.2 years)')).toBeInTheDocument();
    });
  });

  it('displays baseline data for selected country', async () => {
    const mockOnRunSimulation = jest.fn();
    
    render(
      <SimulationCardNew 
        onRunSimulation={mockOnRunSimulation}
        isLoading={false}
      />
    );

    await waitFor(() => {
      expect(screen.getByText('Baseline Data (2022)')).toBeInTheDocument();
    });

    expect(screen.getByText('81.2 years')).toBeInTheDocument();
    expect(screen.getByText('2.1/1k')).toBeInTheDocument();
    expect(screen.getByText('5.2/1k')).toBeInTheDocument();
    expect(screen.getByText('5.8% GDP')).toBeInTheDocument();
  });

  it('updates parameters when sliders are moved', async () => {
    const mockOnRunSimulation = jest.fn();
    
    render(
      <SimulationCardNew 
        onRunSimulation={mockOnRunSimulation}
        isLoading={false}
      />
    );

    await waitFor(() => {
      expect(screen.getByText('Doctor Density: 2.1 per 1,000 population')).toBeInTheDocument();
    });

    const doctorSlider = screen.getByDisplayValue('2.1');
    fireEvent.change(doctorSlider, { target: { value: '3.0' } });

    expect(screen.getByText('Doctor Density: 3.0 per 1,000 population')).toBeInTheDocument();
  });

  it('calls onRunSimulation when run button is clicked', async () => {
    const mockOnRunSimulation = jest.fn();
    
    render(
      <SimulationCardNew 
        onRunSimulation={mockOnRunSimulation}
        isLoading={false}
      />
    );

    await waitFor(() => {
      expect(screen.getByText('Run Simulation')).toBeInTheDocument();
    });

    const runButton = screen.getByText('Run Simulation');
    fireEvent.click(runButton);

    expect(mockOnRunSimulation).toHaveBeenCalledWith('PRT', {
      doctor_density: 2.1,
      nurse_density: 5.2,
      health_spending: 5.8
    });
  });

  it('resets parameters when reset button is clicked', async () => {
    const mockOnRunSimulation = jest.fn();
    
    render(
      <SimulationCardNew 
        onRunSimulation={mockOnRunSimulation}
        isLoading={false}
      />
    );

    await waitFor(() => {
      expect(screen.getByText('Doctor Density: 2.1 per 1,000 population')).toBeInTheDocument();
    });

    // Change a parameter
    const doctorSlider = screen.getByDisplayValue('2.1');
    fireEvent.change(doctorSlider, { target: { value: '3.0' } });

    expect(screen.getByText('Doctor Density: 3.0 per 1,000 population')).toBeInTheDocument();

    // Reset
    const resetButton = screen.getByText('Reset');
    fireEvent.click(resetButton);

    expect(screen.getByText('Doctor Density: 2.1 per 1,000 population')).toBeInTheDocument();
  });

  it('disables controls when loading', async () => {
    const mockOnRunSimulation = jest.fn();
    
    render(
      <SimulationCardNew 
        onRunSimulation={mockOnRunSimulation}
        isLoading={true}
      />
    );

    await waitFor(() => {
      expect(screen.getByText('Running Simulation...')).toBeInTheDocument();
    });

    const runButton = screen.getByText('Running Simulation...');
    expect(runButton).toBeDisabled();

    const resetButton = screen.getByText('Reset');
    expect(resetButton).toBeDisabled();
  });

  it('handles country selection change', async () => {
    const mockOnRunSimulation = jest.fn();
    
    render(
      <SimulationCardNew 
        onRunSimulation={mockOnRunSimulation}
        isLoading={false}
      />
    );

    await waitFor(() => {
      expect(screen.getByDisplayValue('Portugal (Baseline: 81.2 years)')).toBeInTheDocument();
    });

    const countrySelect = screen.getByDisplayValue('Portugal (Baseline: 81.2 years)');
    fireEvent.change(countrySelect, { target: { value: 'ESP' } });

    await waitFor(() => {
      expect(screen.getByText('83.1 years')).toBeInTheDocument();
    });

    expect(screen.getByText('2.8/1k')).toBeInTheDocument();
    expect(screen.getByText('6.1/1k')).toBeInTheDocument();
    expect(screen.getByText('7.2% GDP')).toBeInTheDocument();
  });

  it('handles fetch error gracefully', async () => {
    (fetch as jest.Mock).mockRejectedValue(new Error('Network error'));
    
    const mockOnRunSimulation = jest.fn();
    
    render(
      <SimulationCardNew 
        onRunSimulation={mockOnRunSimulation}
        isLoading={false}
      />
    );

    await waitFor(() => {
      expect(screen.getByText('Policy Simulation')).toBeInTheDocument();
    });

    // Should still render the component even if countries fail to load
    expect(screen.getByText('Select Country')).toBeInTheDocument();
  });
});
