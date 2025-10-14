import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import '@testing-library/jest-dom'
import AnalyticsDashboard from '../components/analytics/AnalyticsDashboard'

// Mock fetch
global.fetch = jest.fn()

// Mock environment variable
Object.defineProperty(import.meta, 'env', {
  value: {
    VITE_API_BASE_URL: 'http://localhost:8000'
  }
})

const mockDashboardData = {
  dashboard_id: 'test-dashboard',
  title: 'Test Dashboard',
  layout: 'grid',
  components: [
    {
      component_id: 'comp1',
      type: 'trend_analysis',
      title: 'Trend Analysis',
      data_source: 'trends',
      data: {
        indicator: 'life_expectancy',
        country: 'PRT',
        trend_direction: 'increasing',
        trend_strength: 0.85
      },
      position: { x: 0, y: 0 },
      size: { width: 400, height: 300 },
      styling: {},
      filters: []
    }
  ],
  filters: [],
  refresh_interval: 300,
  metadata: {
    created_at: '2024-01-01T00:00:00Z',
    version: '1.0'
  }
}

describe('AnalyticsDashboard', () => {
  beforeEach(() => {
    (fetch as jest.Mock).mockClear()
  })

  it('renders correctly with initial state', () => {
    render(<AnalyticsDashboard />)
    
    expect(screen.getByText('Advanced Analytics Dashboard')).toBeInTheDocument()
    expect(screen.getByText('Comprehensive health policy analytics and insights')).toBeInTheDocument()
    expect(screen.getByText('Overview')).toBeInTheDocument()
    expect(screen.getByText('Trends')).toBeInTheDocument()
    expect(screen.getByText('Correlations')).toBeInTheDocument()
    expect(screen.getByText('Forecasts')).toBeInTheDocument()
    expect(screen.getByText('Reports')).toBeInTheDocument()
    expect(screen.getByText('Charts')).toBeInTheDocument()
    expect(screen.getByText('Comparisons')).toBeInTheDocument()
  })

  it('displays performance metrics in overview tab', () => {
    render(<AnalyticsDashboard />)
    
    expect(screen.getByText('87.3%')).toBeInTheDocument()
    expect(screen.getByText('Simulation Accuracy')).toBeInTheDocument()
    expect(screen.getByText('92.1%')).toBeInTheDocument()
    expect(screen.getByText('User Adoption')).toBeInTheDocument()
    expect(screen.getByText('$0.08')).toBeInTheDocument()
    expect(screen.getByText('Cost per Simulation')).toBeInTheDocument()
    expect(screen.getByText('2.3s')).toBeInTheDocument()
    expect(screen.getByText('Avg Response Time')).toBeInTheDocument()
  })

  it('switches between tabs correctly', () => {
    render(<AnalyticsDashboard />)
    
    // Click on Trends tab
    fireEvent.click(screen.getByText('Trends'))
    expect(screen.getByText('Trend Analysis')).toBeInTheDocument()
    
    // Click on Reports tab
    fireEvent.click(screen.getByText('Reports'))
    expect(screen.getByText('Report Builder')).toBeInTheDocument()
    
    // Click on Charts tab
    fireEvent.click(screen.getByText('Charts'))
    expect(screen.getByText('Advanced Charts')).toBeInTheDocument()
  })

  it('handles filter changes correctly', async () => {
    render(<AnalyticsDashboard />)
    
    // Mock successful API response
    ;(fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ dashboard: mockDashboardData })
    })
    
    // Change country filter
    const countrySelect = screen.getByLabelText('Countries')
    fireEvent.change(countrySelect, { target: { value: 'PRT' } })
    
    // Wait for API call
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/analytics/dashboard',
        expect.objectContaining({
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          }
        })
      )
    })
  })

  it('handles time period filter changes', async () => {
    render(<AnalyticsDashboard />)
    
    // Mock successful API response
    ;(fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ dashboard: mockDashboardData })
    })
    
    // Change start year
    const startYearInput = screen.getByDisplayValue('2020')
    fireEvent.change(startYearInput, { target: { value: '2019' } })
    
    // Wait for debounced API call
    await waitFor(() => {
      expect(fetch).toHaveBeenCalled()
    }, { timeout: 1000 })
  })

  it('handles refresh button click', async () => {
    render(<AnalyticsDashboard />)
    
    // Mock successful API response
    ;(fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ dashboard: mockDashboardData })
    })
    
    // Click refresh button
    const refreshButton = screen.getByText('Refresh')
    fireEvent.click(refreshButton)
    
    // Wait for API call
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/analytics/dashboard',
        expect.objectContaining({
          method: 'POST'
        })
      )
    })
  })

  it('handles export functionality', async () => {
    const mockOnExport = jest.fn()
    render(<AnalyticsDashboard onExport={mockOnExport} />)
    
    // Mock successful export response
    ;(fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      blob: async () => new Blob(['test'], { type: 'application/pdf' })
    })
    
    // Click export button
    const exportButton = screen.getByText('Export')
    fireEvent.click(exportButton)
    
    // Click on PNG export option
    const pngOption = screen.getByText('Export as PNG')
    fireEvent.click(pngOption)
    
    // Wait for export to complete
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/analytics/visualizations/export/dashboard/png'),
        expect.objectContaining({
          method: 'POST'
        })
      )
    })
  })

  it('displays loading state during data fetch', async () => {
    // Mock delayed API response
    ;(fetch as jest.Mock).mockImplementationOnce(
      () => new Promise(resolve => setTimeout(() => resolve({
        ok: true,
        json: async () => ({ dashboard: mockDashboardData })
      }), 100))
    )
    
    render(<AnalyticsDashboard />)
    
    // Should show loading state initially
    expect(screen.getByText('Loading analytics data...')).toBeInTheDocument()
    
    // Wait for loading to complete
    await waitFor(() => {
      expect(screen.queryByText('Loading analytics data...')).not.toBeInTheDocument()
    })
  })

  it('handles API errors gracefully', async () => {
    // Mock API error
    ;(fetch as jest.Mock).mockRejectedValueOnce(new Error('API Error'))
    
    render(<AnalyticsDashboard />)
    
    // Should not crash and should handle error gracefully
    await waitFor(() => {
      expect(screen.getByText('Advanced Analytics Dashboard')).toBeInTheDocument()
    })
  })

  it('opens and closes settings panel', () => {
    render(<AnalyticsDashboard />)
    
    // Click settings button
    const settingsButton = screen.getByText('Settings')
    fireEvent.click(settingsButton)
    
    // Should show settings panel
    expect(screen.getByText('Dashboard Settings')).toBeInTheDocument()
    expect(screen.getByText('Refresh Interval (seconds)')).toBeInTheDocument()
    expect(screen.getByText('Show Performance Metrics')).toBeInTheDocument()
    expect(screen.getByText('Show Interactive Charts')).toBeInTheDocument()
  })

  it('updates dashboard configuration in settings', () => {
    render(<AnalyticsDashboard />)
    
    // Open settings
    fireEvent.click(screen.getByText('Settings'))
    
    // Change refresh interval
    const refreshInput = screen.getByDisplayValue('300')
    fireEvent.change(refreshInput, { target: { value: '600' } })
    
    // Toggle show metrics
    const metricsCheckbox = screen.getByLabelText('Show Performance Metrics')
    fireEvent.click(metricsCheckbox)
    
    // Settings should be updated
    expect(refreshInput).toHaveValue(600)
    expect(metricsCheckbox).not.toBeChecked()
  })

  it('displays correct content for each tab', () => {
    render(<AnalyticsDashboard />)
    
    // Overview tab (default)
    expect(screen.getByText('Trend Analysis')).toBeInTheDocument()
    expect(screen.getByText('Correlation Matrix')).toBeInTheDocument()
    
    // Switch to Trends tab
    fireEvent.click(screen.getByText('Trends'))
    expect(screen.getByText('Analyze trends in health indicators over time')).toBeInTheDocument()
    
    // Switch to Correlations tab
    fireEvent.click(screen.getByText('Correlations'))
    expect(screen.getByText('CorrelationMatrix')).toBeInTheDocument()
    
    // Switch to Forecasts tab
    fireEvent.click(screen.getByText('Forecasts'))
    expect(screen.getByText('ForecastChart')).toBeInTheDocument()
    
    // Switch to Reports tab
    fireEvent.click(screen.getByText('Reports'))
    expect(screen.getByText('Create professional reports with customizable templates')).toBeInTheDocument()
    
    // Switch to Charts tab
    fireEvent.click(screen.getByText('Charts'))
    expect(screen.getByText('Create sophisticated visualizations for complex data analysis')).toBeInTheDocument()
    
    // Switch to Comparisons tab
    fireEvent.click(screen.getByText('Comparisons'))
    expect(screen.getByText('Compare countries, time periods, and scenarios for comprehensive analysis')).toBeInTheDocument()
  })

  it('handles initial data prop correctly', () => {
    render(<AnalyticsDashboard initialData={mockDashboardData} />)
    
    // Should not make API call if initial data is provided
    expect(fetch).not.toHaveBeenCalled()
    
    // Should display the dashboard with initial data
    expect(screen.getByText('Advanced Analytics Dashboard')).toBeInTheDocument()
  })

  it('calls onDataUpdate callback when data is updated', async () => {
    const mockOnDataUpdate = jest.fn()
    render(<AnalyticsDashboard onDataUpdate={mockOnDataUpdate} />)
    
    // Mock successful API response
    ;(fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ dashboard: mockDashboardData })
    })
    
    // Trigger data update
    fireEvent.click(screen.getByText('Refresh'))
    
    // Wait for callback to be called
    await waitFor(() => {
      expect(mockOnDataUpdate).toHaveBeenCalledWith(mockDashboardData)
    })
  })

  it('handles multiple indicator selection in filters', async () => {
    render(<AnalyticsDashboard />)
    
    // Mock successful API response
    ;(fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ dashboard: mockDashboardData })
    })
    
    // Select multiple indicators
    const indicatorSelect = screen.getByLabelText('Indicators')
    fireEvent.change(indicatorSelect, { 
      target: { 
        value: ['life_expectancy', 'doctor_density'],
        selectedOptions: [
          { value: 'life_expectancy' },
          { value: 'doctor_density' }
        ]
      } 
    })
    
    // Wait for API call
    await waitFor(() => {
      expect(fetch).toHaveBeenCalled()
    })
  })

  it('displays error state when API fails', async () => {
    // Mock API failure
    ;(fetch as jest.Mock).mockRejectedValueOnce(new Error('Network error'))
    
    render(<AnalyticsDashboard />)
    
    // Should handle error gracefully and still show the dashboard
    await waitFor(() => {
      expect(screen.getByText('Advanced Analytics Dashboard')).toBeInTheDocument()
    })
  })
})
