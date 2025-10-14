import React from 'react'
import { Helmet } from 'react-helmet-async'
import BenchmarkDashboard from '@/components/benchmark/BenchmarkDashboard'

const BenchmarkPage: React.FC = () => {
  return (
    <>
      <Helmet>
        <title>Health Benchmark Dashboard - Policy Simulation Assistant</title>
        <meta name="description" content="Compare countries across health indicators, detect anomalies, and perform peer benchmarking analysis." />
      </Helmet>

      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <BenchmarkDashboard />
        </div>
      </div>
    </>
  )
}

export default BenchmarkPage
