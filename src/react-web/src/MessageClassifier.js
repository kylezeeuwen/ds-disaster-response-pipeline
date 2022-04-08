import React, { Fragment, useContext, useEffect, useState, useCallback } from 'react';
import ModelContext from './context/ModelContext'

const ClassifiedMessage = ({message, classifications}) => {
  return (<li>{message} : {classifications.join(',')}</li>)
}

const MessageClassifier = () => {
  const [classifiedMessages, setClassifiedMessages] = useState([])
  const addClassifiedMessage = useCallback(classifiedMessage => {
    setClassifiedMessages(classifiedMessages.concat(classifiedMessage))
  }, [classifiedMessages, setClassifiedMessages])

  const modelContext = useContext(ModelContext)

  const [message, setMessage] = useState('message goes here')

  const onMessageChange = useCallback(event => {
    setMessage(event.target.value)
  }, [setMessage])

 const classifyMessage = useCallback(() => {
    const url = "http://localhost:5000/api/classify"

    const fetchData = async () => {
      try {
        const response = await fetch(url, {
          method: 'POST',
          body: JSON.stringify({
            message,
            model: modelContext.modelName
          }),
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
    classifyMessage()
    event.preventDefault()
  }, [classifyMessage])

  const classifiedMessageComponents = classifiedMessages.map(({ message, classifications }) => {
    return <ClassifiedMessage key={message} message={message} classifications={classifications}/>
  })

  return (
    <Fragment>
      <form onSubmit={onSubmit}>
        <label>
          Message to Classify:
          <textarea value={message} onChange={onMessageChange} />
        </label>
        <input type="submit" value="Classify" />
      </form>
      <ul>{classifiedMessageComponents}</ul>
    </Fragment>
  )
}

export default MessageClassifier