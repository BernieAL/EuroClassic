import React,{useEffect, useState} from "react"
import {BrowserRouter as Router,Routes,Route, useNavigate,Link} from 'react-router-dom';
import "./styles.scss"

import SearchForm from "./components/SearchForm"
import Graphs from "./components/Graphs/Graphs"
import VehNotFound from "./components/VehNotFound"
import Navbar from "./components/UI/Navbar/Navbar"
import ListingCard from "./components/UI/ListingCard/ListingCard"

import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { fab } from '@fortawesome/free-brands-svg-icons'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { far } from '@fortawesome/free-regular-svg-icons'


import mclarenp1 from './images/mclarenp1.jpg';
import VehResultPage from "./components/VehResultPage/VehResultPage"

library.add(fab, fas, far)


export default function App(){

    const [receivedData,setreceivedData] = useState(null)
    const [user_uuid, setUserUUID] = useState(null)
    const [vehExists_db,setVehExists_DB] = useState(null)

    
    // ROOT URL FOR API to be passed down to chidlren and modified for more specific routes
    const ROOT_API_URL = "http://127.0.0.1:5000/api"

    // if recievedData is updated, do something
    useEffect (()=> {
        if (receivedData){
            console.log("Received Data:",receivedData);
        }
    },[receivedData])

    // callback function passed to SearchForm
    const handleDataFromSearchForm = (data) => {
        
        /** recieved data from backend api looks like:
         *      {
                    "VEH_EXISTS": True/False,
                    "all_sales_records": [],
                    "current_records": [],
                    "sold_stats": [],
                    "current_stats": []
                } 
                ***Note*** lists wont be empty if veh exists in db   
         */
        console.log('Received Data in app:', data)
        setreceivedData(data)
        
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
                                className="search_form_wrapper"><SearchForm handleDataFromSearchForm={handleDataFromSearchForm} ROOT_API_URL = {ROOT_API_URL}/>
                            </div>
                            <div className="card_wrapper">
                                <ListingCard vehMake={"bmw"} vehModel={"m3"} />
                            </div>
                            <div className="recently_requested">
                                <ListingCard />
                            </div>
                            {/* if vehExists_db == False, render VehNotFound component */}
                            {vehExists_db == false && <VehNotFound vehExists_db ={vehExists_db}/>}
                            
                        </div>
                }exact />
                <Route path="/results" element={
                    /* if receivedData not null, render vehResultPage component which renders graphs,stats, and info for selected vehicle dnd pass receivedData as prop*/
                  <VehResultPage receivedData={receivedData} ROOT_API_URL = {ROOT_API_URL} />
                } />
                
                
            
            </Routes>
        </Router>
        

    )
}