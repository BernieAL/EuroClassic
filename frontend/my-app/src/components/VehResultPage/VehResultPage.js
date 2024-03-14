import React,{useState,useEffect} from "react"

import Graphs from "../Graphs/Graphs"
import Navbar from "../UI/Navbar/Navbar"
import ListingCard from "../UI/ListingCard/ListingCard"
// import module_css from './Navbar.module.css'





export default function VehResultPage({recievedData}){

    // store recieved props data in state
    const [dataForViz,setDataForViz] = useState(null)

    useEffect(()=>{
        setDataForViz(recievedData)
        console.log(recievedData)
    },[recievedData])

    return (
        <div className="main_content_wrapper">
            <Navbar />
            
            <div className="jumbotron">test</div>
            <Graphs recievedData={recievedData}/>
            
        </div>
    )    
    }