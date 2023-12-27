import React, {useState,useEffect  } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';


/* READ ME - RECIEVED DATA STRUCTURE

Values Recieved from server encapsulated in an object 
  {all_sales_records:[()],current_records[()],current_stats,sold_stats}

Then each value is itself an array of objects


all_sales_records ex. 

    'all_sales_records': [('645cc521-1bb4-46e6-bef4-f46ac68a1d99', 2012, 'AUDI', 'R8', 116115.34, datetime.date(2022, 8, 15)), ('80cdc5d7-76b8-48f0-bd4b-b5f5dcda6b65', 2018, 'AUDI', 'R8', 97146.08, datetime.date(2023, 5, 9)), ('c179d769-0894-4734-b8b8-016313fe61c9', 2014, 'AUDI', 'R8', 86057.47, datetime.date(2022, 2, 3)), ('b654b01d-f43e-4a80-a652-a3154bfda639', 2018, 'AUDI', 'R8', 86289.72, datetime.date(2022, 12, 5)), ('f1bca6b9-29ed-4c9c-bf1c-4ffb93d80dab', 2011, 'AUDI', 'R8', 82695.55, datetime.date(2022, 7, 27)), ('e8624243-ce92-48dd-b388-6df32eefee75', 2012, 'AUDI', 'R8', 110575.06, datetime.date(2022, 12, 17))


current_records ex. 

    'current_records': [('3f491d30-f178-4623-b93a-f04e73be33d7', 2014, 'AUDI', 'R8', 86339.0), ('a655730e-c6d8-496b-8cbd-887f21c1fb52', 2015, 'AUDI', 'R8', 104611.0), ('f47b266b-c77c-4745-8e00-ca71e3819ff6', 2019, 'AUDI', 'R8', 100867.0), ('ff59e8b7-1b1d-4ab5-bdc4-fabc09656dbc', 2013, 'AUDI', 'R8', 99298.0), ('a3db917a-c0ce-4ae5-96b3-570c84789a1b', 2019, 'AUDI', 'R8', 112348.0), 

*/

export default function Graphs({recievedData}){
    
    // to hold graph/chart data recieved from parent - 
    const [dataForViz,setDataForViz] = useState(null)

    useEffect(()=>{
        setDataForViz(recievedData)
        console.log(recievedData)
    },[recievedData])

    /* Destructure Rec'd Data obj into indiv variables

        returned obj looks like this:
        
        {'all_sales_records': [('4c9f93d8-2be1-4f60-b80b-f7eeb96b8f6e', 2010, 'AUDI', 'R8', 108846.48, datetime.date(2023, 10, 27))], 'current_records': [('ece9ef7d-b2de-4548-b84b-ddda25bc0bd9', 2010, 'AUDI', 'R8', 85484.0), ('54b95bd7-e161-482b-ad5f-729f33b68761', 2010, 'AUDI', 'R8', 91654.0)], 'sold_stats': [], 'current_stats': []} 

        
    */
    /*when destructuring like this, the var names MUST match exactly the keys in the object */
    const {all_sales_records,current_records,current_stats,sold_stats} = recievedData
    
    /* SORT all_sales_records by sale date ascending
       sale_date is last index in each record -> idx 5
       sort() takes a custom compare function
       compare function compares elements based on sale_date
       for 2 records a,b, determine which sale_date comes first by subtracting
       if negative result, then a comes before b
       if positive result, a comes after b
       if result is 0, no change in order needed
       
    */

    //get year,make,model,sale_price,sale_date from each sold record in all_sales_records array
    const GRAPH_sales_data = all_sales_records.map((record)=>{
        return{
            year:record[1],
            make:record[2],
            model:record[3],
            sale_price:record[4],
            sale_date: new Date(record[5]).toLocaleDateString('en-US',{
                day: 'numeric',
                month: 'short',
                year: 'numeric',
            }),
        }
    })

    /*SORT into ascending sale dates

     */

    const GRAPH_sales_data_DATE_SORTED = GRAPH_sales_data.sort((a, b) => new Date(a.sale_date) - new Date(b.sale_date));
    console.log(GRAPH_sales_data_DATE_SORTED)

    

    const GRAPH_current_listing_data = current_records.map((record)=>{
        return {
            year:record[1],
            make:record[2],
            model:record[3],
            list_price:record[4]
        }
    })
    const GRAPH_current_listing_data_YEAR_SORTED = GRAPH_current_listing_data.sort((a,b)=>(a.year - b.year))
    console.log(GRAPH_current_listing_data)

    // const GRAPH_sold_stats = current_records.map((record)=>{
    //     return {
    //         avg_sale_price:
    //         max_sale_price:
    //         min_sale_price:

    //     }
    
    // const GRAPH_current_stats = current_records.map((record)=>{
    //     return {
    //         avg_list_price:
    //         max_list_price:
    //         min_list_price:
            
    //     }
    // })
    

    return (
        <div>
            
            <br></br>
                {/* SOLD LISTINGS */}
                <LineChart
                    width={600}
                    height={500}
                    data={GRAPH_sales_data}
                    margin={{
                        top: 5,
                        right: 30,
                        left: 20,
                        bottom: 15,
                    }}
                >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="sale_date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="sale_price" stroke="#8884d8" activeDot={{ r: 8 }} />
                    
                </LineChart>
                    
                <br></br>
                {/* CURRENT LISTINGS */}
                <LineChart
                    width={600}
                    height={500}
                    data={GRAPH_current_listing_data}
                    margin={{
                        top: 5,
                        right: 30,
                        left: 20,
                        bottom: 5,
                    }}
                >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="year" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="list_price" stroke="#8884d8" activeDot={{ r: 8 }} />
                    
                </LineChart>

                
                
        </div>
        
      );
}


/*
-graphs recieves data from parent component app
-the data it recieves is the raw data meant for populating the different charts and graphs

*/