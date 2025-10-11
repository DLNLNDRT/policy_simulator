import React from 'react'
import { Link } from 'react-router-dom'
import { Helmet } from 'react-helmet-async'
import { Home, ArrowLeft, Search } from 'lucide-react'

const NotFoundPage: React.FC = () => {
  return (
    <>
      <Helmet>
        <title>Page Not Found - Policy Simulation Assistant</title>
        <meta name="description" content="The page you're looking for doesn't exist." />
      </Helmet>

      <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full text-center">
          {/* 404 Illustration */}
          <div className="mb-8">
            <div className="w-32 h-32 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <Search className="w-16 h-16 text-primary-600" />
            </div>
            <h1 className="text-6xl font-bold text-gray-900 mb-2">404</h1>
            <h2 className="text-2xl font-semibold text-gray-700 mb-4">
              Page Not Found
            </h2>
            <p className="text-gray-600 mb-8">
              Sorry, we couldn't find the page you're looking for. 
              It might have been moved, deleted, or you entered the wrong URL.
            </p>
          </div>

          {/* Action Buttons */}
          <div className="space-y-4">
            <Link
              to="/"
              className="btn-primary btn-lg w-full inline-flex items-center justify-center space-x-2"
            >
              <Home className="w-5 h-5" />
              <span>Go Home</span>
            </Link>
            
            <button
              onClick={() => window.history.back()}
              className="btn-outline btn-lg w-full inline-flex items-center justify-center space-x-2"
            >
              <ArrowLeft className="w-5 h-5" />
              <span>Go Back</span>
            </button>
          </div>

          {/* Helpful Links */}
          <div className="mt-12">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Popular Pages
            </h3>
            <div className="space-y-2">
              <Link
                to="/simulation"
                className="block text-primary-600 hover:text-primary-700 transition-colors"
              >
                Policy Simulation
              </Link>
              <Link
                to="/dashboard"
                className="block text-primary-600 hover:text-primary-700 transition-colors"
              >
                Analytics Dashboard
              </Link>
              <Link
                to="/about"
                className="block text-primary-600 hover:text-primary-700 transition-colors"
              >
                About the Project
              </Link>
            </div>
          </div>

          {/* Contact Info */}
          <div className="mt-8 pt-8 border-t border-gray-200">
            <p className="text-sm text-gray-500">
              Still can't find what you're looking for?{' '}
              <a
                href="mailto:support@policy-simulation.assistant"
                className="text-primary-600 hover:text-primary-700"
              >
                Contact our support team
              </a>
            </p>
          </div>
        </div>
      </div>
    </>
  )
}

export default NotFoundPage
