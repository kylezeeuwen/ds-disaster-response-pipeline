import React, {Fragment, useEffect, useMemo, useState} from 'react'
import Plot from 'react-plotly.js'

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
      <Fragment>
        <Plot
          data={[{ x: categories, y: chartData['ACC'], type: 'bar', }]}
          layout={{ width: 1000, height: 400, title: 'Accuracy' }}
        />
        <Plot
          data={[{ x: categories, y: chartData['PPV'], type: 'bar', }]}
          layout={{ width: 1000, height: 400, title: 'Positive predictive value (PPV)' }}
        />
        <Plot
          data={[{ x: categories, y: chartData['NPV'], type: 'bar', }]}
          layout={{ width: 1000, height: 400, title: 'Negative predictive value (NPV)' }}
        />
        <Plot
          data={[{ x: categories, y: chartData['TPR'], type: 'bar', }]}
          layout={{ width: 1000, height: 400, title: 'true positive rate (TPR)' }}
        />
        <Plot
          data={[{ x: categories, y: chartData['TNR'], type: 'bar', }]}
          layout={{ width: 1000, height: 400, title: 'true negative rate (TNR)' }}
        />
        <Plot
          data={[{ x: categories, y: chartData['P'], type: 'bar', }]}
          layout={{ width: 1000, height: 400, title: 'positive samples' }}
        />
        <Plot
          data={[{ x: categories, y: chartData['N'], type: 'bar', }]}
          layout={{ width: 1000, height: 400, title: 'negative samples' }}
        />
      </Fragment>
  ) : null
}

export default ModelPerformance



