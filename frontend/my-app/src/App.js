import React,{useState} from "react"
import {BrowserRouter as Router,Routes,Route, useNavigate,Link} from 'react-router-dom';
import "./styles.scss"

import SearchForm from "./components/SearchForm"
// import Graphs from "./components/Graphs/Graphs"
import VehNotFound from "./components/VehNotFound"
import Navbar from "./components/UI/Navbar/Navbar"
import ListingCard from "./components/UI/ListingCard/ListingCard"

import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { fab } from '@fortawesome/free-brands-svg-icons'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { far } from '@fortawesome/free-regular-svg-icons'


import mclarenp1 from './images/mclarenp1.jpg';
// import VehResultPage from "./components/VehResultPage/VehResultPage"

library.add(fab, fas, far)


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

        <Router>
            <Routes>
                <Route path="/" element={
                        <div className="main_content_wrapper">
                            <Navbar />
                            
                            <div className="jumbotron">test</div>
                            <div 
                                className="search_form_wrapper"><SearchForm onDataSubmit={handleDataFromSearchForm}/>
                            </div>
                            <div className="card_wrapper">
                                <ListingCard />
                            </div>
                            <div className="recently_requested">
                                <ListingCard />
                            </div>
                            {/* if vehExists_db == False, render VehNotFound component */}
                            {vehExists_db == false && <VehNotFound vehExists_db ={vehExists_db}/>}
                            
                        </div>
                }exact />
                
                
                
            
            </Routes>
        </Router>
        

    )
}