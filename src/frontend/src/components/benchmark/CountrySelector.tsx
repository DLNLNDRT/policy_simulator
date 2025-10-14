import React from 'react'
import { Globe, Users, CheckCircle } from 'lucide-react'

interface Country {
  code: string
  name: string
}

interface CountrySelectorProps {
  countries: Country[]
  selectedCountries: string[]
  onSelectionChange: (countries: string[]) => void
  maxSelection?: number
}

const CountrySelector: React.FC<CountrySelectorProps> = ({
  countries,
  selectedCountries,
  onSelectionChange,
  maxSelection = 5
}) => {
  const handleCountryToggle = (countryCode: string) => {
    if (selectedCountries.includes(countryCode)) {
      // Remove country
      onSelectionChange(selectedCountries.filter(code => code !== countryCode))
    } else {
      // Add country (if under limit)
      if (selectedCountries.length < maxSelection) {
        onSelectionChange([...selectedCountries, countryCode])
      }
    }
  }

  const isSelected = (countryCode: string) => selectedCountries.includes(countryCode)
  const canSelectMore = selectedCountries.length < maxSelection

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-900 flex items-center">
          <Globe className="w-5 h-5 mr-2 text-blue-600" />
          Select Countries
        </h3>
        <span className="text-sm text-gray-500">
          {selectedCountries.length}/{maxSelection} selected
        </span>
      </div>

      <div className="grid grid-cols-1 gap-3 max-h-64 overflow-y-auto">
        {countries.map((country) => (
          <label
            key={country.code}
            className={`flex items-center p-3 border rounded-lg cursor-pointer transition-colors ${
              isSelected(country.code)
                ? 'border-blue-500 bg-blue-50'
                : canSelectMore
                ? 'border-gray-200 hover:bg-gray-50'
                : 'border-gray-200 opacity-50 cursor-not-allowed'
            }`}
          >
            <input
              type="checkbox"
              checked={isSelected(country.code)}
              onChange={() => handleCountryToggle(country.code)}
              disabled={!isSelected(country.code) && !canSelectMore}
              className="sr-only"
            />
            <div className="flex items-center space-x-3 flex-1">
              <div className={`w-5 h-5 rounded border-2 flex items-center justify-center ${
                isSelected(country.code)
                  ? 'border-blue-500 bg-blue-500'
                  : 'border-gray-300'
              }`}>
                {isSelected(country.code) && (
                  <CheckCircle className="w-3 h-3 text-white" />
                )}
              </div>
              <div className="flex-1">
                <div className="font-medium text-gray-900">{country.name}</div>
                <div className="text-sm text-gray-500">{country.code}</div>
              </div>
            </div>
          </label>
        ))}
      </div>

      {selectedCountries.length > 0 && (
        <div className="p-3 bg-blue-50 rounded-lg">
          <div className="flex items-center space-x-2 mb-2">
            <Users className="w-4 h-4 text-blue-600" />
            <span className="text-sm font-medium text-blue-900">Selected Countries</span>
          </div>
          <div className="flex flex-wrap gap-2">
            {selectedCountries.map((code) => {
              const country = countries.find(c => c.code === code)
              return (
                <span
                  key={code}
                  className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                >
                  {country?.name || code}
                  <button
                    onClick={() => handleCountryToggle(code)}
                    className="ml-1 text-blue-600 hover:text-blue-800"
                  >
                    ×
                  </button>
                </span>
              )
            })}
          </div>
        </div>
      )}

      {!canSelectMore && selectedCountries.length === maxSelection && (
        <div className="p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
          <p className="text-sm text-yellow-800">
            Maximum {maxSelection} countries selected. Remove a country to select another.
          </p>
        </div>
      )}
    </div>
  )
}

export default CountrySelector