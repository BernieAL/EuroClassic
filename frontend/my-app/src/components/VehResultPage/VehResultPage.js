import React,{useState,useEffect} from "react"

import Graphs from "../Graphs/Graphs"
// import module_css from './Navbar.module.css'





export default function VehResultPage({recievedData}){

    // store recieved props data in state
    const [dataForViz,setDataForViz] = useState(null)

    useEffect(()=>{
        setDataForViz(recievedData)
        console.log(recievedData)
    },[recievedData])

    return (
      
        <Graphs recievedData={recievedData}/>
    )    
    }