import React,{useState,useEffect} from "react"
import {useLocation} from 'react-router-dom'

import Graphs from "../Graphs/Graphs"
import EmailCollector from "../EmailCollector/EmailCollector"
import Navbar from "../UI/Navbar/Navbar"
import ListingCard from "../UI/ListingCard/ListingCard"
// import module_css from './Navbar.module.css'


export default function VehResultPage({recievedData,ROOT_API_URL}){

    const location = useLocation();
    // store recieved props data in state
    const [dataForGraphs, setDataForGraphs] = useState(null);
    const [userEmailReqd, setUserEmailReqd] = useState(false);
    const [user_uuid, setUserUUID] = useState(null)
    const [vehicleDetails,setVehicleDetails] = useState(null)


    useEffect((recievedData)=>{


        const response = await fetch(fullURL,{
            method:'POST',
            headers:{
                'Content-Type':'application/json',
            },
            // body:JSON.stringify(formData)
            body:JSON.stringify(entered_data)
        })
        

        //defining function to call api if url params provided 
        const fetchData = async(params) =>{
            const response = await fetch (`${ROOT_API_URL}?${params}`)
            const data = await response.json()
            setVehicleData(data);
        }


        
        // check if query params provided - this means the component was routed to through url request
        const params = new URLSearchParams(location.search);
        if(params.toString()){
            fetchData(params.toString());
        } else {
            setVehicleData(searchData);
        }
    },[location.search,searchData]);


        // if props status is 'NOT FOUND', then set defaults for graph
        if (recievedData['status'] === 'Not Found'){
            setDataForGraphs({
                all_sales_records: [0], 
                current_records: [0], 
                sold_stats: [0], 
                current_stats: [0]
            });
        } else {
            // else pass props data to graphs component
            setDataForGraphs(recievedData);
            // console.log(recievedData);
        }

         // Set userEmailReqd to true
         setUserEmailReqd(true);   

         setUserUUID(recievedData['uuid'])
         console.log("UUID:" + recievedData['uuid'])
 
    },[recievedData])


  
    
    

    return (
        <div className="main_content_wrapper">
            <Navbar />
            
            <div className="jumbotron">test</div>
            <Graphs recievedData={dataForGraphs}/> {/* Use dataForGraphs state variable */}

            {/* Conditionally render EmailCollector component if userEmailReqd is set to True */}
            {userEmailReqd && <EmailCollector user_uuid_prop={user_uuid} ROOT_API_URL = {ROOT_API_URL}/>}
        </div>
    );
}
