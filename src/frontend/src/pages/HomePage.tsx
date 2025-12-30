import React from 'react'
import { Link } from 'react-router-dom'
import { 
  ArrowRight, 
  BarChart3, 
  Brain, 
  Shield, 
  Zap,
  Users,
  Globe,
  TrendingUp,
  Target,
  FileText
} from 'lucide-react'
import { Helmet } from 'react-helmet-async'

const HomePage: React.FC = () => {
  const features = [
    {
      icon: Target,
      title: 'Policy Simulation Engine',
      description: 'Interactive what-if scenarios for workforce and spending changes with gender filtering',
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
      link: '/simulation'
    },
    {
      icon: BarChart3,
      title: 'Health Benchmark Dashboard',
      description: 'Compare countries, detect anomalies, and analyze peer group performance',
      color: 'text-green-600',
      bgColor: 'bg-green-100',
      link: '/benchmark'
    },
    {
      icon: FileText,
      title: 'Narrative Insight Generator',
      description: 'AI-powered policy narratives with citations and actionable recommendations',
      color: 'text-purple-600',
      bgColor: 'bg-purple-100',
      link: '/narrative'
    },
    {
      icon: Shield,
      title: 'Data Quality Assurance',
      description: '98.4/100 quality score with comprehensive validation and monitoring',
      color: 'text-orange-600',
      bgColor: 'bg-orange-100',
      link: null
    }
  ]

  const stats = [
    { label: 'Countries Covered', value: '9+', icon: Globe },
    { label: 'Health Metrics', value: '8', icon: BarChart3 },
    { label: 'Data Quality Score', value: '98.4%', icon: Shield },
    { label: 'Response Time', value: '<5s', icon: Zap }
  ]

  return (
    <>
      <Helmet>
        <title>Policy Simulation Assistant - GenAI Healthcare Analytics</title>
        <meta name="description" content="Transform global health data into predictive policy insights with AI-powered simulations for healthcare policy makers." />
      </Helmet>

      <div className="min-h-screen">
        {/* Hero Section */}
        <section className="relative bg-gradient-to-br from-primary-50 to-blue-50 pt-12 pb-8">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center">
              <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-4">
                Policy Simulation
                <span className="text-primary-600 block">Assistant</span>
              </h1>
              <p className="text-xl text-gray-600 mb-6 max-w-3xl mx-auto">
                GenAI-powered healthcare policy simulation tool that transforms global health data 
                into predictive insights for policy makers, ministries, and NGOs.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link
                  to="/simulation"
                  className="btn-primary btn-lg inline-flex items-center space-x-2"
                >
                  <span>Start Simulation</span>
                  <ArrowRight className="w-5 h-5" />
                </Link>
                <Link
                  to="/benchmark"
                  className="btn-outline btn-lg inline-flex items-center space-x-2"
                >
                  <span>View Benchmark</span>
                  <BarChart3 className="w-5 h-5" />
                </Link>
              </div>
            </div>
          </div>
        </section>

        {/* Video Walkthrough Section */}
        <section className="pt-8 pb-12 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-6">
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-2">
                See It In Action
              </h2>
              <p className="text-lg text-gray-600 max-w-3xl mx-auto">
                Watch a complete walkthrough of the Policy Simulator and learn how to use all features
              </p>
            </div>
            
            <div className="max-w-4xl mx-auto">
              <div className="relative aspect-video rounded-lg overflow-hidden shadow-xl">
                <iframe
                  className="absolute top-0 left-0 w-full h-full"
                  src="https://www.youtube.com/embed/ezAhlVTMoWU"
                  title="Policy Simulator Walkthrough"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                  allowFullScreen
                />
              </div>
            </div>
          </div>
        </section>

        {/* Stats Section */}
        <section className="py-16 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
              {stats.map((stat, index) => {
                const Icon = stat.icon
                return (
                  <div key={index} className="text-center">
                    <div className="inline-flex items-center justify-center w-12 h-12 bg-primary-100 rounded-lg mb-4">
                      <Icon className="w-6 h-6 text-primary-600" />
                    </div>
                    <div className="text-3xl font-bold text-gray-900 mb-2">
                      {stat.value}
                    </div>
                    <div className="text-sm text-gray-600">
                      {stat.label}
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-20 bg-gray-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
                Powerful Features for Policy Makers
              </h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Built using the ADAPT framework with comprehensive data quality validation 
                and AI-powered insights for informed decision making.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
              {features.map((feature, index) => {
                const Icon = feature.icon
                const CardContent = (
                  <div className="card p-6 text-center hover:shadow-medium transition-shadow">
                    <div className={`inline-flex items-center justify-center w-16 h-16 ${feature.bgColor} rounded-xl mb-6`}>
                      <Icon className={`w-8 h-8 ${feature.color}`} />
                    </div>
                    <h3 className="text-xl font-semibold text-gray-900 mb-3">
                      {feature.title}
                    </h3>
                    <p className="text-gray-600">
                      {feature.description}
                    </p>
                  </div>
                )
                
                return feature.link ? (
                  <Link key={index} to={feature.link} className="block">
                    {CardContent}
                  </Link>
                ) : (
                  <div key={index}>
                    {CardContent}
                  </div>
                )
              })}
            </div>
          </div>
        </section>

        {/* How It Works Section */}
        <section className="py-20 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
                How It Works
              </h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Simple three-step process to generate policy insights with AI-powered analysis.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-600 text-white rounded-full text-2xl font-bold mb-6">
                  1
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  Select Country
                </h3>
                <p className="text-gray-600">
                  Choose from 9+ countries with comprehensive health indicator data 
                  including life expectancy, workforce density, and spending metrics.
                </p>
              </div>

              <div className="text-center">
                <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-600 text-white rounded-full text-2xl font-bold mb-6">
                  2
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  Adjust Parameters
                </h3>
                <p className="text-gray-600">
                  Use interactive sliders to model changes in doctor density, 
                  nurse density, and government health spending.
                </p>
              </div>

              <div className="text-center">
                <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-600 text-white rounded-full text-2xl font-bold mb-6">
                  3
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  Get AI Insights
                </h3>
                <p className="text-gray-600">
                  Receive predictive outcomes with confidence intervals, 
                  AI-generated narratives, and policy recommendations.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Target Users Section */}
        <section className="py-20 bg-gray-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
                Built for Policy Makers
              </h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Designed specifically for healthcare policy professionals who need 
                data-driven insights for informed decision making.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="card p-6 text-center">
                <Users className="w-12 h-12 text-primary-600 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  Health Ministry Planners
                </h3>
                <p className="text-gray-600">
                  Forecast workforce needs and budget allocations with predictive 
                  modeling and scenario analysis.
                </p>
              </div>

              <div className="card p-6 text-center">
                <Globe className="w-12 h-12 text-primary-600 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  Development Analysts
                </h3>
                <p className="text-gray-600">
                  Compare countries and evaluate funding impact with cross-national 
                  benchmarking and trend analysis.
                </p>
              </div>

              <div className="card p-6 text-center">
                <TrendingUp className="w-12 h-12 text-primary-600 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  Policy Researchers
                </h3>
                <p className="text-gray-600">
                  Access clean, validated datasets for academic research and 
                  policy evaluation studies.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20 bg-primary-600">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
              Ready to Transform Health Policy?
            </h2>
            <p className="text-xl text-primary-100 mb-8 max-w-3xl mx-auto">
              Start exploring policy scenarios with our GenAI-powered simulation tool. 
              Get insights in seconds, not weeks.
            </p>
            <Link
              to="/simulation"
              className="btn bg-white text-primary-600 hover:bg-gray-100 btn-lg inline-flex items-center space-x-2"
            >
              <span>Start Your First Simulation</span>
              <ArrowRight className="w-5 h-5" />
            </Link>
          </div>
        </section>
      </div>
    </>
  )
}

export default HomePage
