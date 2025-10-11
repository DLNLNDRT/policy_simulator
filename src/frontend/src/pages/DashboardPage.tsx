import React from 'react'
import { Helmet } from 'react-helmet-async'
import { 
  BarChart3, 
  TrendingUp, 
  Users, 
  Globe,
  Shield,
  Clock,
  DollarSign,
  Activity
} from 'lucide-react'

const DashboardPage: React.FC = () => {
  // Mock data - in real app this would come from API
  const stats = {
    totalSimulations: 1247,
    countriesCovered: 9,
    avgResponseTime: 2.3,
    dataQualityScore: 98.4,
    totalCost: 89.50,
    successRate: 99.2
  }

  const recentSimulations = [
    { country: 'Portugal', change: 0.4, timestamp: '2 minutes ago' },
    { country: 'Spain', change: -0.2, timestamp: '5 minutes ago' },
    { country: 'Sweden', change: 0.6, timestamp: '8 minutes ago' },
    { country: 'Germany', change: 0.3, timestamp: '12 minutes ago' },
    { country: 'France', change: 0.1, timestamp: '15 minutes ago' }
  ]

  const countryStats = [
    { country: 'Portugal', simulations: 234, avgChange: 0.3 },
    { country: 'Spain', simulations: 198, avgChange: 0.2 },
    { country: 'Sweden', simulations: 156, avgChange: 0.4 },
    { country: 'Germany', simulations: 145, avgChange: 0.2 },
    { country: 'France', simulations: 132, avgChange: 0.1 }
  ]

  return (
    <>
      <Helmet>
        <title>Dashboard - Policy Simulation Assistant</title>
        <meta name="description" content="View analytics and insights from policy simulations across countries and time periods." />
      </Helmet>

      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Analytics Dashboard
            </h1>
            <p className="text-xl text-gray-600">
              Monitor simulation performance, usage patterns, and system health
            </p>
          </div>

          {/* Key Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-6 mb-8">
            <div className="card p-6">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                  <BarChart3 className="w-5 h-5 text-blue-600" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-gray-900">{stats.totalSimulations.toLocaleString()}</p>
                  <p className="text-sm text-gray-500">Total Simulations</p>
                </div>
              </div>
            </div>

            <div className="card p-6">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                  <Globe className="w-5 h-5 text-green-600" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-gray-900">{stats.countriesCovered}</p>
                  <p className="text-sm text-gray-500">Countries</p>
                </div>
              </div>
            </div>

            <div className="card p-6">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-yellow-100 rounded-lg flex items-center justify-center">
                  <Clock className="w-5 h-5 text-yellow-600" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-gray-900">{stats.avgResponseTime}s</p>
                  <p className="text-sm text-gray-500">Avg Response</p>
                </div>
              </div>
            </div>

            <div className="card p-6">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                  <Shield className="w-5 h-5 text-purple-600" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-gray-900">{stats.dataQualityScore}%</p>
                  <p className="text-sm text-gray-500">Data Quality</p>
                </div>
              </div>
            </div>

            <div className="card p-6">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center">
                  <DollarSign className="w-5 h-5 text-red-600" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-gray-900">${stats.totalCost}</p>
                  <p className="text-sm text-gray-500">Total Cost</p>
                </div>
              </div>
            </div>

            <div className="card p-6">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-indigo-100 rounded-lg flex items-center justify-center">
                  <Activity className="w-5 h-5 text-indigo-600" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-gray-900">{stats.successRate}%</p>
                  <p className="text-sm text-gray-500">Success Rate</p>
                </div>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Recent Simulations */}
            <div className="card">
              <div className="card-header">
                <h2 className="card-title">Recent Simulations</h2>
                <p className="card-description">
                  Latest policy simulation results
                </p>
              </div>
              <div className="card-content">
                <div className="space-y-4">
                  {recentSimulations.map((sim, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <div className="flex items-center space-x-3">
                        <div className={`w-2 h-2 rounded-full ${
                          sim.change > 0 ? 'bg-green-500' : 'bg-red-500'
                        }`} />
                        <div>
                          <p className="font-medium text-gray-900">{sim.country}</p>
                          <p className="text-sm text-gray-500">{sim.timestamp}</p>
                        </div>
                      </div>
                      <div className={`text-sm font-medium ${
                        sim.change > 0 ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {sim.change > 0 ? '+' : ''}{sim.change.toFixed(1)} years
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Country Statistics */}
            <div className="card">
              <div className="card-header">
                <h2 className="card-title">Country Statistics</h2>
                <p className="card-description">
                  Simulation activity by country
                </p>
              </div>
              <div className="card-content">
                <div className="space-y-4">
                  {countryStats.map((country, index) => (
                    <div key={index} className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <div className="w-8 h-8 bg-primary-100 rounded-lg flex items-center justify-center">
                          <span className="text-sm font-medium text-primary-600">
                            {country.country.charAt(0)}
                          </span>
                        </div>
                        <div>
                          <p className="font-medium text-gray-900">{country.country}</p>
                          <p className="text-sm text-gray-500">{country.simulations} simulations</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="text-sm font-medium text-gray-900">
                          {country.avgChange > 0 ? '+' : ''}{country.avgChange.toFixed(1)} years
                        </p>
                        <p className="text-xs text-gray-500">avg change</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Performance Metrics */}
          <div className="mt-8">
            <div className="card">
              <div className="card-header">
                <h2 className="card-title">System Performance</h2>
                <p className="card-description">
                  Real-time system health and performance metrics
                </p>
              </div>
              <div className="card-content">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                  <div className="text-center">
                    <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-3">
                      <TrendingUp className="w-8 h-8 text-green-600" />
                    </div>
                    <p className="text-2xl font-bold text-gray-900">99.9%</p>
                    <p className="text-sm text-gray-500">Uptime</p>
                  </div>

                  <div className="text-center">
                    <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-3">
                      <Clock className="w-8 h-8 text-blue-600" />
                    </div>
                    <p className="text-2xl font-bold text-gray-900">1.8s</p>
                    <p className="text-sm text-gray-500">Avg Latency</p>
                  </div>

                  <div className="text-center">
                    <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-3">
                      <Users className="w-8 h-8 text-purple-600" />
                    </div>
                    <p className="text-2xl font-bold text-gray-900">47</p>
                    <p className="text-sm text-gray-500">Active Users</p>
                  </div>

                  <div className="text-center">
                    <div className="w-16 h-16 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-3">
                      <Activity className="w-8 h-8 text-yellow-600" />
                    </div>
                    <p className="text-2xl font-bold text-gray-900">0.1%</p>
                    <p className="text-sm text-gray-500">Error Rate</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}

export default DashboardPage
