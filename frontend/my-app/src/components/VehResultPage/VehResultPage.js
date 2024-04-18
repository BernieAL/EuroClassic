import React,{useState,useEffect} from "react"

import Graphs from "../Graphs/Graphs"
import EmailCollector from "../EmailCollector/EmailCollector"
import Navbar from "../UI/Navbar/Navbar"
import ListingCard from "../UI/ListingCard/ListingCard"
// import module_css from './Navbar.module.css'


export default function VehResultPage({recievedData,ROOT_API_URL}){

    // store recieved props data in state
    const [dataForGraphs, setDataForGraphs] = useState(null);
    const [userEmailReqd, setUserEmailReqd] = useState(false);
    const [user_uuid, setUserUUID] = useState(null)

    useEffect(()=>{
        setDataForGraphs(recievedData);
        console.log(recievedData);

        // Check if the data status is 'Not Found'
        if (recievedData['status'] === 'Not Found') {
            // Set graph data to an empty object
            setDataForGraphs({
                all_sales_records: [0], 
                current_records: [0], 
                sold_stats: [0], 
                current_stats: [0]
            });
        
        // Set userEmailReqd to true
        setUserEmailReqd(true);   
        
        
        // get user uuid off API response, send as prop to EmailCollector component
        setUserUUID(recievedData['uuid'])
        console.log("UUID:" + recievedData['uuid'])

        }
    }, [recievedData]);


    

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
