import React, { createContext, useContext, useState, ReactNode } from 'react'

interface SimulationData {
  country: string
  baseline: {
    life_expectancy: number
    doctor_density: number
    nurse_density: number
    health_spending: number
  }
  parameters: {
    doctor_density: number
    nurse_density: number
    health_spending: number
  }
  prediction: {
    change: number
    confidence_interval: {
      lower: number
      upper: number
    }
  }
  metadata?: any
}

interface SimulationContextType {
  simulationData: SimulationData | null
  setSimulationData: (data: SimulationData | null) => void
  clearSimulationData: () => void
}

const SimulationContext = createContext<SimulationContextType | undefined>(undefined)

export const useSimulation = () => {
  const context = useContext(SimulationContext)
  if (context === undefined) {
    throw new Error('useSimulation must be used within a SimulationProvider')
  }
  return context
}

interface SimulationProviderProps {
  children: ReactNode
}

export const SimulationProvider: React.FC<SimulationProviderProps> = ({ children }) => {
  const [simulationData, setSimulationData] = useState<SimulationData | null>(null)

  const clearSimulationData = () => {
    setSimulationData(null)
  }

  return (
    <SimulationContext.Provider value={{ simulationData, setSimulationData, clearSimulationData }}>
      {children}
    </SimulationContext.Provider>
  )
}
