import React, {useState,useEffect  } from 'react'


export default function Graphs({recievedData}){
    
    // to hold graph/chart data recieved from parent - 
    const [dataForViz,setDataForViz] = useState(null)

    useEffect(()=>{
        setDataForViz(recievedData)
        console.log(recievedData)
    },[recievedData])

    /* 
        Destructure Rec'd Data obj
        into indiv variables
    */
   

    /*when destructuring like this, the var names MUST match exactly the keys in the object */
    const {all_sales_records,current_records,current_stats,sold_stats} = recievedData
    
    
    //get year,make,model,sale_price,sale_date from each sold record in all_sales_records array
    const sales_data_for_graph = all_sales_records.map((record)=>{
        return{
            year:record[1],
            make:record[2],
            model:record[3],
            sale_price:record[4],
            sale_date:record[5]
        }
    })
    console.log(sales_data_for_graph)

    const current_listing_data_for_graph = current_records((record)=>{
        return {}
    })

    // need to get indiv values off each record returned in each array
    // This means, get the 



    return (
        <div>
            
        </div>
    )
}


/*
-graphs recieves data from parent component app
-the data it recieves is the raw data meant for populating the different charts and graphs

*/