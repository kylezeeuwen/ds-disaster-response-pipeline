import React, { useState } from 'react';
import MessageClassifier from './MessageClassifier'
import ModelContext from './context/ModelContext'
import ModelInfo from './ModelInfo'
import ModelPerformance from './ModelPerformance'
import './App.css'

import Grid from '@mui/material/Grid'
import Typography from '@mui/material/Typography'

// pull from env somehow or from server
const defaultModelName = 'W_PARAMS'

const App = () => {
  const [modelName, setSelectedModel] = useState(defaultModelName)
  const modelContext = { modelName, setSelectedModel }

  return (
    <ModelContext.Provider value={modelContext}>
      <Grid
        container
        direction="column"
        justifyContent="center"
        alignItems="center"
      >
        <Typography variant={"h1"}>Disaster Response Project</Typography>
        <Typography variant={"h2"}>Analyzing message data for disaster response</Typography>
        <MessageClassifier></MessageClassifier>
        <ModelPerformance></ModelPerformance>
        <ModelInfo></ModelInfo>
      </Grid>
    </ModelContext.Provider>
  )
}

export default App

