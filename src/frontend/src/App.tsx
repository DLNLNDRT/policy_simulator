import React from 'react'
import { Routes, Route } from 'react-router-dom'
import { Helmet } from 'react-helmet-async'

import Layout from '@/components/Layout'
import HomePage from '@/pages/HomePage'
import SimulationPage from '@/pages/SimulationPage'
import DashboardPage from '@/pages/DashboardPage'
import AboutPage from '@/pages/AboutPage'
import NotFoundPage from '@/pages/NotFoundPage'

function App() {
  return (
    <>
      <Helmet>
        <title>Policy Simulation Assistant</title>
        <meta name="description" content="GenAI-powered healthcare policy simulation tool for policy makers" />
      </Helmet>
      
      <Layout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/simulation" element={<SimulationPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </Layout>
    </>
  )
}

export default App
