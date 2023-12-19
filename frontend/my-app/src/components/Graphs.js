import React, {useState,useEffect  } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const data = [
    {
      name: 'Page A',
      uv: 4000,
      pv: 2400,
      amt: 2400,
    },
    {
      name: 'Page B',
      uv: 3000,
      pv: 1398,
      amt: 2210,
    },
    {
      name: 'Page C',
      uv: 2000,
      pv: 9800,
      amt: 2290,
    },
    {
      name: 'Page D',
      uv: 2780,
      pv: 3908,
      amt: 2000,
    },
    {
      name: 'Page E',
      uv: 1890,
      pv: 4800,
      amt: 2181,
    },
    {
      name: 'Page F',
      uv: 2390,
      pv: 3800,
      amt: 2500,
    },
    {
      name: 'Page G',
      uv: 3490,
      pv: 4300,
      amt: 2100,
    },
  ];


export default function Graphs({recievedData}){
    
    // to hold graph/chart data recieved from parent - 
    const [dataForViz,setDataForViz] = useState(null)

    useEffect(()=>{
        setDataForViz(recievedData)
        // console.log(recievedData)
    },[recievedData])

    /* Destructure Rec'd Data obj into indiv variables

        returned obj looks like this:
        
        {'all_sales_records': [('4c9f93d8-2be1-4f60-b80b-f7eeb96b8f6e', 2010, 'AUDI', 'R8', 108846.48, datetime.date(2023, 10, 27))], 'current_records': [('ece9ef7d-b2de-4548-b84b-ddda25bc0bd9', 2010, 'AUDI', 'R8', 85484.0), ('54b95bd7-e161-482b-ad5f-729f33b68761', 2010, 'AUDI', 'R8', 91654.0)], 'sold_stats': [], 'current_stats': []} 

        
    */
    /*when destructuring like this, the var names MUST match exactly the keys in the object */
    const {all_sales_records,current_records,current_stats,sold_stats} = recievedData
    
    
    //get year,make,model,sale_price,sale_date from each sold record in all_sales_records array
    const GRAPH_sales_data = all_sales_records.map((record)=>{
        return{
            year:record[1],
            make:record[2],
            model:record[3],
            sale_price:record[4],
            sale_date:record[5]
        }
    })
    console.log(GRAPH_sales_data)

    const GRAPH_current_listing_data = current_records.map((record)=>{
        return {
            year:record[1],
            make:record[2],
            model:record[3],
            list_price:record[4]
        }
    })
    // console.log(GRAPH_current_listing_data)

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
            <p>test from graph component</p>
            
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
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="list_price" stroke="#8884d8" activeDot={{ r: 8 }} />
                    <Line type="monotone" dataKey="year" stroke="#82ca9d" />
                </LineChart>
                
        </div>
        
      );
}


/*
-graphs recieves data from parent component app
-the data it recieves is the raw data meant for populating the different charts and graphs

*/