import React, { useState } from 'react';
import MessageClassifier from './MessageClassifier'
import ModelInfo from './ModelInfo'
import ModelPerformance from './ModelPerformance'
import './App.css'

import Grid from '@mui/material/Grid'
import Typography from '@mui/material/Typography'

const App = () => (
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
)

export default App

