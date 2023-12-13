
import React from "react"
import {Line} from "react-chartjs-2"
import "../styles.css"


export default function LineChart({chartData}){

    return(
        <div className="chartSize">
            <div className="chart-container">
                <h2 style={{textAlign:"center"}}>Line Chart</h2>
                <Line
                    data = {chartData}
                    options={{
                        plugins:{
                            title:{
                                display: true,
                                text: "users gained between 2016-2020"
                            },
                            lineTension: 0.5
                        }
                    }}
                />
            </div>
        </div>
    )
}