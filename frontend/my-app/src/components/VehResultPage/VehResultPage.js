import React,{useState,useEffect} from "react"

import Graphs from "../Graphs/Graphs"
import Navbar from "../UI/Navbar/Navbar"
import ListingCard from "../UI/ListingCard/ListingCard"
// import module_css from './Navbar.module.css'





export default function VehResultPage({recievedData}){

    // store recieved props data in state
    const [dataForGraphs,setDataForGraphs] = useState(null)

    useEffect(()=>{
        setDataForGraphs(recievedData)
        console.log(recievedData)
    },[recievedData])

    /* check status of recievedData obj 
       If not found, create obj with empty array and pass to graph component. Graphs will display but will be empty   
    */
    let graphData;
    if (recievedData['status'] == 'Not Found'){
        graphData = {'all_sales_records': [0], 
                     'current_records': [0], 
                     'sold_stats': [0], 
                     'current_stats': [0]
                    }
         }
         
         recievedData = graphData
         

    return (
        <div className="main_content_wrapper">
            <Navbar />
            
            <div className="jumbotron">test</div>
            <Graphs recievedData={recievedData}/>
            
        </div>
    )    
    }