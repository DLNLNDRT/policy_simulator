import React, { useState } from 'react'
import { 
  BarChart3, 
  TrendingUp, 
  Activity, 
  PieChart, 
  Scatter,
  Grid3X3,
  Settings,
  Download,
  Eye,
  Plus
} from 'lucide-react'
import { 
  LineChart, 
  Line, 
  BarChart, 
  Bar, 
  ScatterChart, 
  Scatter as RechartsScatter,
  PieChart as RechartsPieChart, 
  Pie, 
  Cell,
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  Legend
} from 'recharts'
import { ChartType, VisualizationRequest } from '@/types/analytics'

interface AdvancedChartsProps {
  onCreate?: (config: VisualizationRequest) => void
}

const AdvancedCharts: React.FC<AdvancedChartsProps> = ({ onCreate }) => {
  const [selectedChartType, setSelectedChartType] = useState<ChartType>(ChartType.LINE)
  const [chartConfig, setChartConfig] = useState({
    title: 'Custom Chart',
    data: {
      labels: ['2020', '2021', '2022', '2023', '2024'],
      datasets: [{
        label: 'Sample Data',
        data: [65, 59, 80, 81, 56]
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      showLegend: true,
      showGrid: true,
      showTooltips: true
    },
    styling: {
      primaryColor: '#3498db',
      secondaryColor: '#2c3e50',
      backgroundColor: '#ffffff',
      textColor: '#333333'
    }
  })

  const [isCreating, setIsCreating] = useState(false)
  const [showPreview, setShowPreview] = useState(false)

  const chartTypes = [
    { type: ChartType.LINE, label: 'Line Chart', icon: TrendingUp, description: 'Show trends over time' },
    { type: ChartType.BAR, label: 'Bar Chart', icon: BarChart3, description: 'Compare values across categories' },
    { type: ChartType.SCATTER, label: 'Scatter Plot', icon: Scatter, description: 'Show relationships between variables' },
    { type: ChartType.PIE, label: 'Pie Chart', icon: PieChart, description: 'Show proportions of a whole' },
    { type: ChartType.HEATMAP, label: 'Heatmap', icon: Grid3X3, description: 'Show data density and patterns' },
    { type: ChartType.AREA, label: 'Area Chart', icon: Activity, description: 'Show cumulative values over time' }
  ]

  const sampleData = {
    line: [
      { year: '2020', value: 65, secondary: 45 },
      { year: '2021', value: 59, secondary: 52 },
      { year: '2022', value: 80, secondary: 48 },
      { year: '2023', value: 81, secondary: 55 },
      { year: '2024', value: 56, secondary: 62 }
    ],
    bar: [
      { category: 'Portugal', value: 81.2, secondary: 78.1 },
      { category: 'Spain', value: 83.1, secondary: 80.2 },
      { category: 'Sweden', value: 82.5, secondary: 80.8 },
      { category: 'Greece', value: 81.5, secondary: 78.8 }
    ],
    scatter: [
      { x: 2.1, y: 81.2, country: 'Portugal' },
      { x: 2.8, y: 83.1, country: 'Spain' },
      { x: 3.0, y: 82.5, country: 'Sweden' },
      { x: 2.4, y: 81.5, country: 'Greece' }
    ],
    pie: [
      { name: 'Portugal', value: 25, color: '#3498db' },
      { name: 'Spain', value: 30, color: '#e74c3c' },
      { name: 'Sweden', value: 25, color: '#2ecc71' },
      { name: 'Greece', value: 20, color: '#f39c12' }
    ]
  }

  const handleCreateChart = async () => {
    if (!onCreate) return

    setIsCreating(true)
    try {
      const config: VisualizationRequest = {
        chart_type: selectedChartType,
        title: chartConfig.title,
        data: chartConfig.data,
        config: chartConfig.options,
        chart_spec: {
          type: selectedChartType,
          title: chartConfig.title,
          styling: chartConfig.styling,
          data: chartConfig.data
        }
      }

      await onCreate(config)
    } finally {
      setIsCreating(false)
    }
  }

  const renderChartPreview = () => {
    const data = sampleData[selectedChartType as keyof typeof sampleData] || sampleData.line

    switch (selectedChartType) {
      case ChartType.LINE:
        return (
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="year" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="value" 
                stroke={chartConfig.styling.primaryColor} 
                strokeWidth={2}
                dot={{ fill: chartConfig.styling.primaryColor }}
              />
              <Line 
                type="monotone" 
                dataKey="secondary" 
                stroke={chartConfig.styling.secondaryColor} 
                strokeWidth={2}
                dot={{ fill: chartConfig.styling.secondaryColor }}
              />
            </LineChart>
          </ResponsiveContainer>
        )

      case ChartType.BAR:
        return (
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="category" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar 
                dataKey="value" 
                fill={chartConfig.styling.primaryColor}
                name="Primary"
              />
              <Bar 
                dataKey="secondary" 
                fill={chartConfig.styling.secondaryColor}
                name="Secondary"
              />
            </BarChart>
          </ResponsiveContainer>
        )

      case ChartType.SCATTER:
        return (
          <ResponsiveContainer width="100%" height={300}>
            <ScatterChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="x" name="X Value" />
              <YAxis dataKey="y" name="Y Value" />
              <Tooltip cursor={{ strokeDasharray: '3 3' }} />
              <RechartsScatter 
                dataKey="y" 
                fill={chartConfig.styling.primaryColor}
              />
            </ScatterChart>
          </ResponsiveContainer>
        )

      case ChartType.PIE:
        return (
          <ResponsiveContainer width="100%" height={300}>
            <RechartsPieChart>
              <Pie
                data={data}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </RechartsPieChart>
          </ResponsiveContainer>
        )

      case ChartType.HEATMAP:
        return (
          <div className="heatmap-preview">
            <div className="heatmap-grid">
              {[0, 1, 2, 3].map(row => (
                <div key={row} className="heatmap-row">
                  {[0, 1, 2, 3].map(col => (
                    <div
                      key={col}
                      className="heatmap-cell"
                      style={{
                        backgroundColor: `rgba(52, 152, 219, ${0.2 + (row + col) * 0.2})`,
                        color: (row + col) > 3 ? 'white' : 'black'
                      }}
                    >
                      {Math.round((row + col) * 25)}
                    </div>
                  ))}
                </div>
              ))}
            </div>
          </div>
        )

      default:
        return (
          <div className="chart-placeholder">
            <BarChart3 className="w-16 h-16 text-gray-400" />
            <p>Chart preview will appear here</p>
          </div>
        )
    }
  }

  return (
    <div className="advanced-charts">
      <div className="charts-header">
        <div className="header-content">
          <h2 className="charts-title">Advanced Charts</h2>
          <p className="charts-description">
            Create sophisticated visualizations for complex data analysis
          </p>
        </div>
        <div className="header-actions">
          <button
            onClick={() => setShowPreview(!showPreview)}
            className="btn-outline inline-flex items-center space-x-2"
          >
            <Eye className="w-4 h-4" />
            <span>{showPreview ? 'Hide' : 'Show'} Preview</span>
          </button>
          <button
            onClick={handleCreateChart}
            disabled={isCreating}
            className="btn-primary inline-flex items-center space-x-2"
          >
            <Plus className="w-4 h-4" />
            <span>{isCreating ? 'Creating...' : 'Create Chart'}</span>
          </button>
        </div>
      </div>

      <div className="charts-content">
        <div className="charts-main">
          {/* Chart Type Selection */}
          <div className="chart-type-section">
            <h3>Chart Type</h3>
            <div className="chart-type-grid">
              {chartTypes.map(chartType => {
                const Icon = chartType.icon
                return (
                  <button
                    key={chartType.type}
                    onClick={() => setSelectedChartType(chartType.type)}
                    className={`chart-type-card ${selectedChartType === chartType.type ? 'selected' : ''}`}
                  >
                    <Icon className="w-8 h-8" />
                    <h4>{chartType.label}</h4>
                    <p>{chartType.description}</p>
                  </button>
                )
              })}
            </div>
          </div>

          {/* Chart Configuration */}
          <div className="chart-config-section">
            <h3>Chart Configuration</h3>
            <div className="config-form">
              <div className="form-row">
                <div className="form-group">
                  <label>Chart Title</label>
                  <input
                    type="text"
                    value={chartConfig.title}
                    onChange={(e) => setChartConfig({ ...chartConfig, title: e.target.value })}
                    className="form-input"
                    placeholder="Enter chart title"
                  />
                </div>
                <div className="form-group">
                  <label>Primary Color</label>
                  <input
                    type="color"
                    value={chartConfig.styling.primaryColor}
                    onChange={(e) => setChartConfig({
                      ...chartConfig,
                      styling: { ...chartConfig.styling, primaryColor: e.target.value }
                    })}
                    className="color-input"
                  />
                </div>
                <div className="form-group">
                  <label>Secondary Color</label>
                  <input
                    type="color"
                    value={chartConfig.styling.secondaryColor}
                    onChange={(e) => setChartConfig({
                      ...chartConfig,
                      styling: { ...chartConfig.styling, secondaryColor: e.target.value }
                    })}
                    className="color-input"
                  />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Background Color</label>
                  <input
                    type="color"
                    value={chartConfig.styling.backgroundColor}
                    onChange={(e) => setChartConfig({
                      ...chartConfig,
                      styling: { ...chartConfig.styling, backgroundColor: e.target.value }
                    })}
                    className="color-input"
                  />
                </div>
                <div className="form-group">
                  <label>Text Color</label>
                  <input
                    type="color"
                    value={chartConfig.styling.textColor}
                    onChange={(e) => setChartConfig({
                      ...chartConfig,
                      styling: { ...chartConfig.styling, textColor: e.target.value }
                    })}
                    className="color-input"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Chart Options */}
          <div className="chart-options-section">
            <h3>Chart Options</h3>
            <div className="options-grid">
              <div className="option-item">
                <label>
                  <input
                    type="checkbox"
                    checked={chartConfig.options.showLegend}
                    onChange={(e) => setChartConfig({
                      ...chartConfig,
                      options: { ...chartConfig.options, showLegend: e.target.checked }
                    })}
                  />
                  Show Legend
                </label>
              </div>
              <div className="option-item">
                <label>
                  <input
                    type="checkbox"
                    checked={chartConfig.options.showGrid}
                    onChange={(e) => setChartConfig({
                      ...chartConfig,
                      options: { ...chartConfig.options, showGrid: e.target.checked }
                    })}
                  />
                  Show Grid
                </label>
              </div>
              <div className="option-item">
                <label>
                  <input
                    type="checkbox"
                    checked={chartConfig.options.showTooltips}
                    onChange={(e) => setChartConfig({
                      ...chartConfig,
                      options: { ...chartConfig.options, showTooltips: e.target.checked }
                    })}
                  />
                  Show Tooltips
                </label>
              </div>
              <div className="option-item">
                <label>
                  <input
                    type="checkbox"
                    checked={chartConfig.options.responsive}
                    onChange={(e) => setChartConfig({
                      ...chartConfig,
                      options: { ...chartConfig.options, responsive: e.target.checked }
                    })}
                  />
                  Responsive
                </label>
              </div>
            </div>
          </div>
        </div>

        {/* Preview Panel */}
        {showPreview && (
          <div className="preview-panel">
            <div className="preview-header">
              <h3>Chart Preview</h3>
              <button
                onClick={() => setShowPreview(false)}
                className="btn-icon"
              >
                ×
              </button>
            </div>
            <div className="preview-content">
              <div className="preview-chart">
                {renderChartPreview()}
              </div>
              <div className="preview-info">
                <h4>{chartConfig.title}</h4>
                <p>Type: {chartTypes.find(t => t.type === selectedChartType)?.label}</p>
                <p>Colors: {chartConfig.styling.primaryColor}, {chartConfig.styling.secondaryColor}</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default AdvancedCharts
