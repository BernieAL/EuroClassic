import React,{useState,useEffect} from "react"
import {useLocation} from 'react-router-dom'

import Graphs from "../Graphs/Graphs"
import EmailCollector from "../EmailCollector/EmailCollector"
import Navbar from "../UI/Navbar/Navbar"
import ListingCard from "../UI/ListingCard/ListingCard"
// import module_css from './Navbar.module.css'


export default function VehResultPage({receivedData,ROOT_API_URL}){

    const location = useLocation();
    // store received props data in state
    const [dataForGraphs, setDataForGraphs] = useState(null);
    const [userEmailReqd, setUserEmailReqd] = useState(false);
    const [user_uuid, setUserUUID] = useState(null)
    const [vehicleDetails,setVehicleData] = useState(null)


    /* when the component is routed to with query parameters in the URL and when it receives data as props - being rendered by other components

    If requested through URL - it will have url params, we check for these and handle accordingly - making an api request, attaching the params as the reqeust body

    If component rendered by other components - it will have received props
    we evaluate specific property ['status'] of receivedData prop to determine if data was found, 
        if found, we pass the received props to graphs component, 
        if not found, we set defaults as 0 and pass to graphs component 

    SUMMARY
    -Get Query Parameters from URL: You use location.search to extract the query parameters from the URL. This property contains the query string portion of the URL.

    -Convert to URLSearchParams Object: You pass location.search to the URLSearchParams constructor to create a URLSearchParams object (params). This object provides an interface for working with URL parameters.

    -Check if Query Parameters Exist: You use params.toString() to convert the params object to a string. If query parameters exist in the URL, this string will not be empty, and you proceed to make the API request. If it's empty, it means there are no query parameters in the URL, and you use the data received as props.

    -Make API Request: If query parameters exist (params.toString() is not empty), you call fetchData(params.toString()), passing the string representation of the query parameters to the fetchData function. Inside fetchData, you include these parameters in the request body using JSON.stringify(params).

    -Handle Data Retrieval: In fetchData, you make the API request with the provided query parameters. Upon receiving a response, you extract and set the data using setVehicleData.
    */
    useEffect(()=>{
        
      
        //defining function to call api if url params provided 
        const fetchData = async(vehQuery) =>{
        
            try {
                const response = await fetch (`${ROOT_API_URL}/vehicle-query`,{
                    method:'POST',
                    headers:{
                        'Content-Type':'application/json',
                    },
                    body:JSON.stringify(vehQuery)
                });
                
                // Check if response is successful
                if (!response.ok) {
                    throw new Error('Failed to fetch data');
                }
                const data = await response.json()
                setVehicleData(data);
                setDataForGraphs(data)
            } catch (error) {
                console.error('Error fetching data:', error);
                // Handle error state or display error message
            }
        }

        
        // check if query params provided - this means the component was routed to through url request
        // create new URLSearchParams obj
        const searchParams = new URLSearchParams(location.search);
        // if searchParams obj is not empty string, pass to fetchData
        if(searchParams.toString()){
            
            // getting params off searchParams obj
            const make = searchParams.get('vehMake')
            const model = searchParams.get('vehModel')
            
            // encapsulating as object to pass to fetchData
            const vehQuery = {'year': '0000','make':make,'model':model}

            fetchData(vehQuery);
        } else {
            // else if no params, means we rec'd props
            // evaluate props to see if they exist\

            

            if (receivedData && receivedData?.status === 'not found') {
                console.log("received Data is empty") 

                // set defaults for graph if empty props or receivedData['status'] == not found]
                setDataForGraphs({
                    all_sales_records: [0], 
                    current_records: [0], 
                    sold_stats: [0], 
                    current_stats: [0]
                });
                // set flag to collect user email
                setUserEmailReqd(true);   
                setUserUUID(receivedData['uuid'])
                console.log("UUID:" + receivedData['uuid'])
            } else {
                
                setVehicleData(receivedData);
                setDataForGraphs(receivedData)
                // setUserEmailReqd(true);   
                // setUserUUID(receivedData['uuid'])
                // console.log("UUID:" + receivedData['uuid'])
            }
        }
},[location.search,receivedData]);


    

  
    
    

    return (
        <div className="main_content_wrapper">
            <Navbar />
            
            <div className="jumbotron">test</div>
            {console.log(receivedData)}
            <Graphs receivedData={dataForGraphs}/> {/* Use dataForGraphs state variable */}

            {/* Conditionally render EmailCollector component if userEmailReqd is set to True */}
            {userEmailReqd && <EmailCollector user_uuid_prop={user_uuid} ROOT_API_URL = {ROOT_API_URL}/>}
        </div>
    );
}
