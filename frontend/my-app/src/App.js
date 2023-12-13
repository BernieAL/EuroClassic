
// tutorial for react-chartjs 
// https://blog.logrocket.com/using-chart-js-react/#installing-chart-js-react-project
// https://www.positronx.io/how-to-create-and-embed-trend-lines-chart-in-react/

import Chart from "chart.js/auto";
import { CategoryScale } from "chart.js";
import { useState } from "react";
import { Data } from "./utils/Data";
import PieChart from "./components/PieChart";
import LineChart from "./components/LineChart"
import chartTrendline from 'chartjs-plugin-trendline';
import "./styles.css";

Chart.register(CategoryScale);
Chart.register(chartTrendline);

export default function App() {
  
  const [chartData, setChartData] = useState({
    labels: Data.map((data) => data.year), 
    datasets: [
      {
        label: "Users Gained ",
        data: Data.map((data) => data.userGain),
        backgroundColor: [
          "rgba(75,192,192,1)",
          "&quot;#ecf0f1",
          "#50AF95",
          "#f3ba2f",
          "#2a71d0"
        ],
        borderColor: "black",
        borderWidth: 2,
        fill: false,
        trendlineLinear: {
            colorMin: "#3e95cd",
            lineStyle: "line",
            width: 4,
            projection: true
        }
      },
        // {
        //   label: "Users Gained ",
        //   data: Data.map((data) => data.userGain),
        //   backgroundColor: [
        //     "rgba(75,192,192,1)",
        //     "&quot;#ecf0f1",
        //     "#50AF95",
        //     "#f3ba2f",
        //     "#2a71d0"
        //   ],
        //   borderColor: "black",
        //   borderWidth: 2,
        //   fill: false,
        //   trendlineLinear: {
        //       colorMin: "#3e95cd",
        //       lineStyle: "line",
        //       width: 1
        //   }
        // }


    ]
  });
 
  return (
    <div className="App">
      {/* <PieChart chartData={chartData}/> */}
      <LineChart chartData={chartData}/>
    </div>
  );
}