import React, {useState,useEffect  } from 'react'


export default function Graphs({recievedData}){
    
    // to hold graph/chart data recieved from parent - 
    const [dataForViz,setDataForViz] = useState(null)

    useEffect(()=>{
        setDataForViz(recievedData)
        // console.log(recievedData)
    },[recievedData])

    /* 
        Destructure Rec'd Data obj
        into indiv variables
    */


    /*when destructuring like this, the var names MUST match exactly the keys in the object */
    const {all_sales_records,current_records,current_stats,sold_stats} = recievedData

    console.log(JSON.stringify(all_sales_records))

    return (
        <div>
            {all_sales_records.map((record,index)=>{
                <p key={index}>{record}</p>
            })}
        </div>
    )
}


/*
-graphs recieves data from parent component app
-the data it recieves is the raw data meant for populating the different charts and graphs

*/