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
        <div>
            <SearchForm onDataSubmit={handleDataFromSearchForm}/>
            
            {/* if recievedData not null, render the graphs and pass them the data */}
            {recievedData !== null && (
                <Graphs recievedData={recievedData}/> 
            )}
        </div>
    )
}