import { useState, useEffect } from "react";
import axios from "axios";
import config from "./config"

function App() {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    axios.get(`${config.url}/event`).then(response => {
      setEvents(response.data.response);
    }).catch((reason) => console.error(reason)).finally(() => {})
  }, [events])

  return (
    <>
      <h1>Events</h1>
      <button onClick={() => {
        axios.post(`${config.url}/event`)
      }}>Generate an event</button>
      <table>
        <thead>
          <tr>
            <th>id</th>
            <th>name</th>
            <th>state</th>
          </tr>
        </thead>
        <tbody>
          {events.map((event, index) => {
            return <tr key={index}>
              {Object.values(event).map((value, i) => {
                return <td key={i}>{value}</td>
              })}
            </tr>
          })}
        </tbody>
      </table>
    </>
  );
}

export default App;
