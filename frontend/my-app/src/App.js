import React,{useState} from "react"
import "./styles.scss"

import SearchForm from "./components/SearchForm"
import Graphs from "./components/Graphs/Graphs"
import VehNotFound from "./components/VehNotFound"
import Navbar from "./components/UI/Navbar/Navbar"




export default function App(){

    const [recievedData,setRecievedData] = useState(null)
    const [vehExists_db,setVehExists_DB] = useState(null)

    // callback function passed to SearchForm
    const handleDataFromSearchForm = (data) => {
        
        /** recieved data from backend api looks like:
         *      {
                  "VEH_EXISTS": False,
                    "all_sales_records": [],
                    "current_records": [],
                    "sold_stats": [],
                    "current_stats": []
                } 
                ***Note*** lists wont be empty if veh exists in db   
         */
        
        console.log('Recieved Data in app:', data)
        setRecievedData(data)
        
        const VEH_EXISTS = data['VEH_EXISTS']
        setVehExists_DB(VEH_EXISTS)
    }


    return(
        <div className="main-wrapper">
            
            <Navbar/>
            <div className="jumbotron">test</div>
            <div className="search_form_wrapper"><SearchForm onDataSubmit={handleDataFromSearchForm}/></div>
            <div className="card_wrapper">
                <div className="listing_card">
                    test
                </div>
                <div className="listing_card">
                    test
                </div>
                <div className="listing_card">
                    test
                </div>
                <div className="listing_card">
                    test
                </div>
            </div>

            
            {/* if vehExists_db == False, render VehNotFound component */}
            {vehExists_db == false && ( <VehNotFound vehExists_db ={vehExists_db}/>
            )}
            
            {/* if recievedData not null, render Graphs component and pass recievedData as prop*/}
            {recievedData !== null && (
                <Graphs recievedData={recievedData}/> 
            )}
        </div>
    )
}