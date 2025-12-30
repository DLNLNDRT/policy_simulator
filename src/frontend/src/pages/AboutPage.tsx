import React from 'react'
import { Helmet } from 'react-helmet-async'
import { 
  Brain, 
  Shield, 
  Zap, 
  Globe,
  Users,
  BarChart3,
  CheckCircle,
  ExternalLink
} from 'lucide-react'

const AboutPage: React.FC = () => {
  const features = [
    {
      icon: BarChart3,
      title: 'Policy Simulation Engine',
      description: 'Interactive what-if scenarios for workforce and spending changes with regression-based predictions'
    },
    {
      icon: Brain,
      title: 'AI-Powered Narratives',
      description: 'GPT-4 generated explanations with citations, disclaimers, and policy context'
    },
    {
      icon: Shield,
      title: 'Data Quality Assurance',
      description: '98.4/100 quality score with comprehensive validation and monitoring'
    },
    {
      icon: Zap,
      title: 'High Performance',
      description: 'Sub-5 second response times with intelligent caching and optimization'
    }
  ]

  const dataSources = [
    { name: 'WHO Global Health Observatory', description: 'Life expectancy, workforce density, mortality data' },
    { name: 'World Bank Data', description: 'Government health spending, economic indicators' }
  ]

  const methodology = [
    {
      step: 1,
      title: 'Data Collection & Validation',
      description: 'Aggregate health indicators from multiple sources with automated quality checks'
    },
    {
      step: 2,
      title: 'Statistical Modeling',
      description: 'Apply regression analysis to identify correlations between workforce, spending, and outcomes'
    },
    {
      step: 3,
      title: 'Simulation Engine',
      description: 'Generate predictions based on parameter changes with confidence intervals'
    },
    {
      step: 4,
      title: 'AI Narrative Generation',
      description: 'Create contextual explanations with appropriate disclaimers and citations'
    }
  ]

  return (
    <>
      <Helmet>
        <title>About - Policy Simulation Assistant</title>
        <meta name="description" content="Learn about the Policy Simulation Assistant, built using the ADAPT framework for healthcare policy makers." />
      </Helmet>

      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="text-center mb-16">
            <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              About Policy Simulation Assistant
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              A GenAI-powered platform that transforms global health data into predictive 
              policy insights for healthcare decision makers worldwide.
            </p>
          </div>

          {/* Mission Statement */}
          <div className="card p-8 mb-16 text-center">
            <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <Brain className="w-8 h-8 text-primary-600" />
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Our Mission</h2>
            <p className="text-lg text-gray-600 max-w-4xl mx-auto">
              To democratize access to healthcare policy insights by combining high-quality global health data 
              with advanced AI technology, enabling policy makers to make informed decisions that improve 
              health outcomes for populations worldwide.
            </p>
          </div>

          {/* Key Features */}
          <div className="mb-16">
            <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">
              Key Features
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              {features.map((feature, index) => {
                const Icon = feature.icon
                return (
                  <div key={index} className="card p-6">
                    <div className="flex items-start space-x-4">
                      <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center flex-shrink-0">
                        <Icon className="w-6 h-6 text-primary-600" />
                      </div>
                      <div>
                        <h3 className="text-xl font-semibold text-gray-900 mb-2">
                          {feature.title}
                        </h3>
                        <p className="text-gray-600">
                          {feature.description}
                        </p>
                      </div>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>

          {/* Methodology */}
          <div className="mb-16">
            <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">
              Our Methodology
            </h2>
            <div className="space-y-8">
              {methodology.map((item, index) => (
                <div key={index} className="flex items-start space-x-6">
                  <div className="w-12 h-12 bg-primary-600 text-white rounded-full flex items-center justify-center font-bold text-lg flex-shrink-0">
                    {item.step}
                  </div>
                  <div className="flex-1">
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">
                      {item.title}
                    </h3>
                    <p className="text-gray-600">
                      {item.description}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Data Sources */}
          <div className="mb-16">
            <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">
              Data Sources
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {dataSources.map((source, index) => (
                <div key={index} className="card p-6">
                  <div className="flex items-start space-x-3">
                    <CheckCircle className="w-5 h-5 text-green-600 mt-1 flex-shrink-0" />
                    <div>
                      <h3 className="font-semibold text-gray-900 mb-1">
                        {source.name}
                      </h3>
                      <p className="text-sm text-gray-600">
                        {source.description}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Technology Stack */}
          <div className="mb-16">
            <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">
              Technology Stack
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="card p-6 text-center">
                <div className="w-16 h-16 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <Globe className="w-8 h-8 text-blue-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Frontend</h3>
                <p className="text-gray-600 text-sm">
                  React 18, TypeScript, Vite, Tailwind CSS, Recharts
                </p>
              </div>

              <div className="card p-6 text-center">
                <div className="w-16 h-16 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <Shield className="w-8 h-8 text-green-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Backend</h3>
                <p className="text-gray-600 text-sm">
                  Python 3.11, FastAPI, SQLite, Pandas, Scikit-learn
                </p>
              </div>

              <div className="card p-6 text-center">
                <div className="w-16 h-16 bg-purple-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <Brain className="w-8 h-8 text-purple-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">AI Integration</h3>
                <p className="text-gray-600 text-sm">
                  OpenAI GPT-4, Anthropic Claude, Custom prompt engineering
                </p>
              </div>
            </div>
          </div>

          {/* ADAPT Framework */}
          <div className="mb-16">
            <div className="card p-8">
              <div className="text-center mb-8">
                <h2 className="text-3xl font-bold text-gray-900 mb-4">
                  Built with the ADAPT Framework
                </h2>
                <p className="text-lg text-gray-600 max-w-3xl mx-auto">
                  Our development process follows the ADAPT framework methodology for 
                  systematic exploration and validation of AI-powered solutions.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-5 gap-6">
                {[
                  { letter: 'A', phase: 'Assess', description: 'Data quality and market analysis' },
                  { letter: 'D', phase: 'Discover', description: 'Pattern recognition and correlations' },
                  { letter: 'A', phase: 'Analyze', description: 'Statistical modeling and validation' },
                  { letter: 'P', phase: 'Prototype', description: 'MVP development and testing' },
                  { letter: 'T', phase: 'Test', description: 'User validation and iteration' }
                ].map((item, index) => (
                  <div key={index} className="text-center">
                    <div className="w-12 h-12 bg-primary-600 text-white rounded-full flex items-center justify-center font-bold text-lg mx-auto mb-3">
                      {item.letter}
                    </div>
                    <h3 className="font-semibold text-gray-900 mb-1">{item.phase}</h3>
                    <p className="text-sm text-gray-600">{item.description}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Target Users */}
          <div className="mb-16">
            <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">
              Built for Policy Makers
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="card p-6 text-center">
                <Users className="w-12 h-12 text-primary-600 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  Health Ministry Planners
                </h3>
                <p className="text-gray-600">
                  Forecast workforce needs and budget allocations with predictive modeling 
                  and scenario analysis for evidence-based policy planning.
                </p>
              </div>

              <div className="card p-6 text-center">
                <Globe className="w-12 h-12 text-primary-600 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  Development Analysts
                </h3>
                <p className="text-gray-600">
                  Compare countries and evaluate funding impact with cross-national 
                  benchmarking and trend analysis for international development work.
                </p>
              </div>

              <div className="card p-6 text-center">
                <BarChart3 className="w-12 h-12 text-primary-600 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  Policy Researchers
                </h3>
                <p className="text-gray-600">
                  Access clean, validated datasets for academic research and policy 
                  evaluation studies with comprehensive data quality assurance.
                </p>
              </div>
            </div>
          </div>

          {/* Contact & Links */}
          <div className="text-center">
            <h2 className="text-3xl font-bold text-gray-900 mb-8">
              Learn More
            </h2>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a
                href="https://github.com/DLNLNDRT/policy_simulator"
                className="btn-outline btn-lg inline-flex items-center space-x-2"
                target="_blank"
                rel="noopener noreferrer"
              >
                <ExternalLink className="w-5 h-5" />
                <span>GitHub</span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}

export default AboutPage
