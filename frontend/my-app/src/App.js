import React,{useState} from "react"
import "./styles.scss"

import SearchForm from "./components/SearchForm"
import Graphs from "./components/Graphs/Graphs"
import VehNotFound from "./components/VehNotFound"
import Navbar from "./components/UI/Navbar/Navbar"

import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { fab } from '@fortawesome/free-brands-svg-icons'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { far } from '@fortawesome/free-regular-svg-icons'

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
        <div className="main_content_wrapper">

           
            <Navbar/>
            
           
            <div className="jumbotron">test</div>


            <div 
            className="search_form_wrapper"><SearchForm onDataSubmit={handleDataFromSearchForm}/></div>
            <div className="card_wrapper">
            
                <div className="listing_card">
                    <div className="listing_card_content">
                        <div className="listing_card_img">
                            <img src="" alt="" />
                        </div>
                        <button className="view_result">View Result Set</button>
                        <div className="listing_card_icon_stats">
                            <p className="listings_change_30 days">indicator, green or red, showing change num of listings over current 30 days compared to last 30 days
                               
                            </p>
                            <div className="bottom_icons"> 
                                <h2 className="icon"><FontAwesomeIcon icon={["fas", "arrow-up"]} /></h2>
                                <h2 className="literal_value _change">120</h2>
                            </div>
                           
                            {/* <p className="sold_change_30_days">change is sold transactions over last 30 days compared to last 30 days</p>
                            <p className="price_avg_30_days">numerical dollar value of change is avg listing price compared to last 30 days</p> */}
                        </div>
                    </div>
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
            <div className="recently_requested">
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