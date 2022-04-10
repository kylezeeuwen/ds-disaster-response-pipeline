import React, { useEffect, useState } from 'react'
import _ from 'lodash'

import Container from '@mui/material/Container'
import Typography from '@mui/material/Typography'
import TableContainer from '@mui/material/TableContainer'
import Paper from '@mui/material/Paper'
import Table from '@mui/material/Table'
import TableHead from '@mui/material/TableHead'
import TableBody from '@mui/material/TableBody'
import TableRow from '@mui/material/TableRow'
import TableCell from '@mui/material/TableCell'

const ModelSelector = () => {
  const [modelInfo, setModelInfo] = useState([])

  useEffect(() => {
    const url = "http://localhost:5000/api/get-model-info"

    const fetchData = async () => {
      try {
        const response = await fetch(url)
        const json = await response.json()
        const fieldsArray = transformMetadata(json)
        setModelInfo(fieldsArray)
      } catch (error) {
        console.log("error", error)
      }
    };

    fetchData()
  }, [setModelInfo])

  return (
    <Container>
      <Typography variant={"h3"}>Model Info</Typography>
      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} size="small" aria-label="a dense table">
          <TableHead>
            <TableRow>
              <TableCell>Field</TableCell>
              <TableCell>Value</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {modelInfo.map(({ field, value}) => (
              <TableRow
                key={field}
                sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
              >
                <TableCell component="th" scope="row">{field}</TableCell>
                <TableCell><pre>{value}</pre></TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Container>
  )

}

const transformMetadata = metaDataInput => {
  const fieldsArray = _(metaDataInput)
    .map((value, field) => ({ value, field }))
    .map(({field, value }) => {
      if (field === 'CHOSEN_PARAMETERS') {
        return { field: 'CHOSEN_PARAMETERS', value: JSON.stringify(value, {}, 2) }
      }
      if (field === 'MODEL_TIMESTAMP') {
        return { field: 'MODEL_TIMESTAMP', value: (new Date(value * 1000)).toISOString() }
      }
      return { field, value}
    })
    .value()

  return fieldsArray
}

export default ModelSelector

