import React, { useEffect, useState } from 'react'
import _ from 'lodash'
import Container from '@mui/material/Container'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'

const ModelInfoItem = ({field, value}) => {
  const valueDisplay = (field.match(/PARAMETERS/))
    ? (<pre>{value}</pre>)
    : value

  return (<div>{field} : {valueDisplay}</div>)
}

const ModelSelector = () => {
  const [modelInfo, setModelInfo] = useState([])

  useEffect(() => {
    const url = "http://localhost:5000/api/get-model-info"

    const fetchData = async () => {
      try {
        const response = await fetch(url)
        const json = await response.json()
        const fieldsArray = _(json)
          .map((value, field) => ({ value, field }))
          .map(({field, value }) => {
            if (field === 'MODEL_PARAMETERS') {
              return { field: 'CHOSEN_PARAMETERS', value: JSON.stringify(value.parameters, {}, 2) }
            }
            if (field === 'MODEL_TIMESTAMP') {
              return { field: 'MODEL_TIMESTAMP', value: (new Date(value * 1000)).toISOString() }
            }
            return { field, value}
          })
          .filter(({field}) => field != 'MODEL_PARAMETERS')
          .value()

        setModelInfo(fieldsArray)
      } catch (error) {
        console.log("error", error)
      }
    };

    fetchData()
  }, [setModelInfo])

  const modelListItems = modelInfo.map(({ field, value}) => {
    return <ModelInfoItem key={field} field={field} value={value}/>
  })

  return (
    <Container>
      <Typography variant="body">Model Info:</Typography>
      <Stack spacing={2}>{modelListItems}</Stack>
    </Container>
  )
}

export default ModelSelector
