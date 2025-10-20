import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { 
  BarChart3, 
  Home, 
  Info, 
  Menu, 
  X,
  Brain,
  Shield,
  Zap,
  Target,
  FileText,
  CheckCircle,
  TrendingUp
} from 'lucide-react'
import { useState } from 'react'

interface LayoutProps {
  children: React.ReactNode
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  const location = useLocation()

  const navigation = [
    { name: 'Home', href: '/', icon: Home },
    { name: 'Simulation', href: '/simulation', icon: Target },
    { name: 'Benchmark', href: '/benchmark', icon: BarChart3 },
    { name: 'Narrative', href: '/narrative', icon: FileText },
    { name: 'Quality', href: '/quality', icon: CheckCircle },
    { name: 'Analytics', href: '/analytics', icon: TrendingUp },
    { name: 'About', href: '/about', icon: Info },
  ]

  const isActive = (href: string) => location.pathname === href

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-soft border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <div className="flex items-center">
              <Link to="/" className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
                  <Brain className="w-5 h-5 text-white" />
                </div>
                <span className="text-xl font-bold text-gray-900">
                  Policy Simulator
                </span>
              </Link>
            </div>

            {/* Desktop Navigation */}
            <nav className="hidden md:flex space-x-8">
              {navigation.map((item) => {
                const Icon = item.icon
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={`flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      isActive(item.href)
                        ? 'text-primary-600 bg-primary-50'
                        : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    <span>{item.name}</span>
                  </Link>
                )
              })}
            </nav>

            {/* Mobile menu button */}
            <div className="md:hidden">
              <button
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                className="p-2 rounded-md text-gray-600 hover:text-gray-900 hover:bg-gray-100"
              >
                {isMobileMenuOpen ? (
                  <X className="w-6 h-6" />
                ) : (
                  <Menu className="w-6 h-6" />
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMobileMenuOpen && (
          <div className="md:hidden border-t border-gray-200">
            <div className="px-2 pt-2 pb-3 space-y-1">
              {navigation.map((item) => {
                const Icon = item.icon
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    onClick={() => setIsMobileMenuOpen(false)}
                    className={`flex items-center space-x-2 px-3 py-2 rounded-md text-base font-medium transition-colors ${
                      isActive(item.href)
                        ? 'text-primary-600 bg-primary-50'
                        : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                    }`}
                  >
                    <Icon className="w-5 h-5" />
                    <span>{item.name}</span>
                  </Link>
                )
              })}
            </div>
          </div>
        )}
      </header>

      {/* Main Content */}
      <main className="flex-1">
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            {/* Brand */}
            <div className="col-span-1 md:col-span-2">
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-6 h-6 bg-primary-600 rounded-lg flex items-center justify-center">
                  <Brain className="w-4 h-4 text-white" />
                </div>
                <span className="text-lg font-bold text-gray-900">
                  Policy Simulator
                </span>
              </div>
              <p className="text-gray-600 text-sm max-w-md">
                GenAI-powered healthcare policy simulation tool for policy makers, 
                ministries, and NGOs. Transform health data into predictive insights.
              </p>
            </div>

            {/* Quick Links */}
            <div>
              <h3 className="text-sm font-semibold text-gray-900 mb-4">Quick Links</h3>
              <ul className="space-y-2">
                <li>
                  <Link to="/simulation" className="text-sm text-gray-600 hover:text-primary-600">
                    Policy Simulation
                  </Link>
                </li>
                <li>
                  <Link to="/benchmark" className="text-sm text-gray-600 hover:text-primary-600">
                    Health Benchmark
                  </Link>
                </li>
                <li>
                  <Link to="/narrative" className="text-sm text-gray-600 hover:text-primary-600">
                    Narrative Generator
                  </Link>
                </li>
                <li>
                  <Link to="/quality" className="text-sm text-gray-600 hover:text-primary-600">
                    Data Quality
                  </Link>
                </li>
                <li>
                  <Link to="/analytics" className="text-sm text-gray-600 hover:text-primary-600">
                    Advanced Analytics
                  </Link>
                </li>
                <li>
                  <Link to="/about" className="text-sm text-gray-600 hover:text-primary-600">
                    About
                  </Link>
                </li>
              </ul>
            </div>

            {/* Features */}
            <div>
              <h3 className="text-sm font-semibold text-gray-900 mb-4">Features</h3>
              <ul className="space-y-2">
                <li className="flex items-center space-x-2 text-sm text-gray-600">
                  <Shield className="w-4 h-4 text-green-500" />
                  <span>Data Quality 98.4%</span>
                </li>
                <li className="flex items-center space-x-2 text-sm text-gray-600">
                  <Zap className="w-4 h-4 text-blue-500" />
                  <span>&lt;5s Response Time</span>
                </li>
                <li className="flex items-center space-x-2 text-sm text-gray-600">
                  <Brain className="w-4 h-4 text-purple-500" />
                  <span>AI-Powered Insights</span>
                </li>
              </ul>
            </div>
          </div>

          <div className="border-t border-gray-200 mt-8 pt-8">
            <div className="flex flex-col md:flex-row justify-between items-center">
              <p className="text-sm text-gray-600">
                © 2024 Policy Simulator. Built with the ADAPT Framework.
              </p>
              <div className="flex space-x-6 mt-4 md:mt-0">
                <span className="text-xs text-gray-500">
                  This is a policy simulation tool for exploratory analysis.
                </span>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default Layout
