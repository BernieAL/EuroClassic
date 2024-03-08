import React,{useState} from "react"
import SearchForm from "./components/SearchForm"
import Graphs from "./components/Graphs"





export default function App(){

    const [recievedData,setRecievedData] = useState(null)

    // callback function passed to SearchForm
    const handleDataFromSearchForm = (data) => {
        console.log('Recieved Data in app:', data)
        
        // check if veh results are empty - meaning car is not in db
        const all_sales_records = data['all_sales_records'][0]
        console.log(all_sales_records)
        if (all_sales_records.length == 0){
            console.log('veh not in db ')
        }

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