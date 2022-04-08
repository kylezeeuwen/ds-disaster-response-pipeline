import React, { useState } from 'react';
import MessageClassifier from './MessageClassifier'
import ModelContext from './context/ModelContext'
import ModelInfo from './ModelInfo'
import ModelPerformance from './ModelPerformance'
import './App.css';

// pull from env somehow or from server
const defaultModelName = 'W_PARAMS'

const App = () => {
  const [modelName, setSelectedModel] = useState(defaultModelName)
  const modelContext = { modelName, setSelectedModel }

  return (
    <ModelContext.Provider value={modelContext}>
      <MessageClassifier></MessageClassifier>
      <ModelPerformance></ModelPerformance>
      <ModelInfo></ModelInfo>
    </ModelContext.Provider>
  )
}

export default App

