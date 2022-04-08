import React, { Fragment, useContext, useEffect, useState, useCallback } from 'react';
import ModelContext from './context/ModelContext'

import Button from '@mui/material/Button'
import Box from '@mui/material/Box'
import FormControl from '@mui/material/FormControl'
import Chip from '@mui/material/Chip'
import Divider from '@mui/material/Divider'
import Grid from '@mui/material/Grid'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import TextField from '@mui/material/TextField'
import Container from '@mui/material/Container'

const MessageClassifier = () => {
  const [classifiedMessages, setClassifiedMessages] = useState([])
  const addClassifiedMessage = useCallback(classifiedMessage => {
    setClassifiedMessages(classifiedMessages.concat(classifiedMessage))
  }, [classifiedMessages, setClassifiedMessages])

  const modelContext = useContext(ModelContext)

  const [message, setMessage] = useState('')

  const onMessageChange = useCallback(event => {
    setMessage(event.target.value)
  }, [setMessage])

  const classifyMessage = useCallback(() => {
    const url = "http://localhost:5000/api/classify"

    const fetchData = async () => {
      try {
        const response = await fetch(url, {
          method: 'POST',
          body: JSON.stringify({ message, model: modelContext.modelName }),
          headers: { 'Content-Type': 'application/json' }
        })
        const { message: classifiedMessage, classifications: classificationResults } = await response.json()
        const classifications = _(classificationResults)
          .map((value, field) => ({ field, value }))
          .filter(({value}) => value === 1)
          .map(({field}) => field)
          .value()

        addClassifiedMessage({ message: classifiedMessage, classifications })
      } catch (error) {
        console.log("error", error)
      }
    }

    fetchData()
  }, [message])

  const onSubmit = useCallback(event => {
    event.preventDefault()
    classifyMessage()
    setMessage('')
  }, [classifyMessage])

  useEffect(() => {
    const listener = event => {
      if (event.code === "Enter" || event.code === "NumpadEnter") {
        console.log("Enter key was pressed. Run your function.")
        event.preventDefault();
        classifyMessage()
        setMessage('')
      }
    }
    document.addEventListener("keydown", listener)
    return () => {
      document.removeEventListener("keydown", listener)
    }
  }, [classifyMessage])

  const classifiedMessageComponents = classifiedMessages.map(({ message, classifications }) => {
    let classificationChips = classifications.map(classification =>
      <Chip label={classification} color="success" size="small" style={{ width: '200px' }}/>
    )

    if (classificationChips.length === 0) {
      classificationChips = [<Chip label={'none'} color="error" size="small" style={{ width: '200px' }}/>]
    }

    return (
      <Grid container spacing={1}>
        <Grid item xs={4}><Typography variant="body">{message}</Typography></Grid>
        <Grid item xs={8}><Stack direction="row" justifyContent="flex-start" spacing={1}>{classificationChips}</Stack></Grid>
      </Grid>
    )
  })
  const classifiedMessageComponent = (
    <Stack spacing={2} divider={<Divider orientation="horizontal" flexItem/>}>{classifiedMessageComponents}</Stack>
  )

  return (
    <Container>
      <Box sx={{ marginBottom: "20px" }} component="form" onSubmit={onSubmit}>
          <FormControl fullWidth sx={{ m: 1 }} variant="standard">
            <TextField
              id="message-to-classify"
              placeholder="Enter a message to classify"
              value={message}
              onChange={onMessageChange}
            />
            <Button variant="contained" type="submit" primary="true" style={{ marginTop: '10px', width: '200px' }}>Classify</Button>
          </FormControl>

      </Box>
      <Container>
        {classifiedMessageComponent}
      </Container>
    </Container>
  )
}

export default MessageClassifier