import React,{useState} from "react"
import SearchForm from "./components/SearchForm"
import Graphs from "./components/Graphs"





export default function App(){

    const [recievedData,setRecievedData] = useState(null)

    // callback function passed to SearchForm
    const handleDataFromSearchForm = (data) => {
        console.log('Recieved Data in app:', data)
        setRecievedData(data)
    }


    return(
        <SearchForm onDataSubmit={handleDataFromSearchForm}/>
        <Graphs/>
    )
}