import React, {Fragment, useEffect, useMemo, useState} from 'react'
import Plot from 'react-plotly.js'

import Grid from '@mui/material/Grid'
import Container from '@mui/material/Container'

const ModelPerformance = () => {
  const [categories, setCategories] = useState(null)
  const [metrics, setMetrics] = useState(null)

  useEffect(() => {
    const url = "http://localhost:5000/api/get-categories"
    const fetchData = async () => {
      try {
        const response = await fetch(url)
        const json = await response.json()
        setCategories(json.categories)
      } catch (error) {
        console.log("error", error)
      }
    }
    fetchData()
  }, [setCategories])

  useEffect(() => {
    const url = "http://localhost:5000/api/get-model-performance"
    const fetchData = async () => {
      try {
        const response = await fetch(url)
        const json = await response.json()
        setMetrics(json.metrics)
      } catch (error) {
        console.log("error", error)

      }
    }
    fetchData()
  }, [setMetrics])

  // metrics: ('P', 'N', 'TP', 'FP', 'TN', 'FN', 'TPR', 'TNR', 'PPV', 'NPV', 'ACC', 'train_set_size', 'test_set_size')
  const chartData = useMemo(() => {
    if (!categories || !metrics) { return null }
    const chartData = {
      P: [],
      N: [],
      TP: [],
      FP: [],
      TN: [],
      FN: [],
      TPR: [],
      TNR: [],
      PPV: [],
      NPV: [],
      ACC: [],
    }
    metrics
      .filter(({ metric }) => metric != 'train_set_size' && metric != 'test_set_size')
      .forEach(({ category, metric, value}) => chartData[metric][categories.indexOf(category)] = value)

    return chartData
  }, [categories, metrics])

    return categories && chartData ? (
      <Container>
        <Grid container spacing={1}>
          <Grid item>
            <Plot
              data={[{ x: categories, y: chartData['ACC'], type: 'bar', }]}
              layout={{ width: 1160, height: 400, title: 'Accuracy' }}
              config={{ displayModeBar: false }}
            />
          </Grid>
          <Grid item>
            <Plot
              data={[{ x: categories, y: chartData['PPV'], type: 'bar', }]}
              layout={{ width: 1160, height: 400, title: 'Positive predictive value (PPV)' }}
              config={{ displayModeBar: false }}
            />
          </Grid>
          <Grid item>
            <Plot
              data={[{ x: categories, y: chartData['NPV'], type: 'bar', }]}
              layout={{ width: 1160, height: 400, title: 'Negative predictive value (NPV)' }}
              config={{ displayModeBar: false }}
            />
          </Grid>
          <Grid item>
            <Plot
              data={[{ x: categories, y: chartData['TPR'], type: 'bar', }]}
              layout={{ width: 1160, height: 400, title: 'true positive rate (TPR)' }}
              config={{ displayModeBar: false }}
            />
          </Grid>
          <Grid item>
            <Plot
              data={[{ x: categories, y: chartData['TNR'], type: 'bar', }]}
              layout={{ width: 1160, height: 400, title: 'true negative rate (TNR)' }}
              config={{ displayModeBar: false }}
            />
          </Grid>
          <Grid item>
            <Plot
              data={[{ x: categories, y: chartData['P'], type: 'bar', }]}
              layout={{ width: 1160, height: 400, title: 'positive samples' }}
              config={{ displayModeBar: false }}
            />
          </Grid>
          <Grid item>
            <Plot
              data={[{ x: categories, y: chartData['N'], type: 'bar', }]}
              layout={{ width: 1160, height: 400, title: 'negative samples' }}
              config={{ displayModeBar: false }}
            />
          </Grid>
        </Grid>
      </Container>
  ) : null
}

export default ModelPerformance



