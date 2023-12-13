

// import "Utils"



window.onload = ()=>{


  fetch('/get_data')
      .then(response => response.json())
      .then(data=>{
       

        years = data.map((el)=>{
          return el['Year']
        })
        avg_Sale_Price = data.map((el)=>{
          return el['Avg Sale Price']
        })
        
        max_sale_price_by_year = data.map((el)=>{
          return el['max_sale_price_by_year']
        })
       
        /* READ ME
        avg sale price data coming back as object
        looks like:
          [{"Year":"1200","Avg Sale Price":61943.0,"max_sale_price_by_year":106111.0},{"Year":"1300","Avg Sale Price":65194.0,"max_sale_price_by_year":109888.0},{"Year":"2003","Avg Sale Price":21931.8181818182,"max_sale_price_by_year":34500.0},{"Year":"2021","Avg Sale Price":117625.0,"max_sale_price_by_year":127500.0},{"Year":"2022","Avg Sale Price":134940.0,"max_sale_price_by_year":134940.0},{"Year":"2023","Avg Sale Price":105000.0,"max_sale_price_by_year":105000.0}]*/

      //  for each obj in data 
      //  extract year from it, and put it in a new Array
      
        GRAPH_avg_sale_price(years,avg_Sale_Price)
      })


}

// const ctx = document.getElementById('myChart');
// const DATA_COUNT = 7;
// const NUMBER_CFG = {count: DATA_COUNT, min: -100, max: 100};

// const labels = ['2018','2019','2020'];
// const data = {
//   labels: labels,
//   datasets: [{
//     label: 'My First Dataset',
//     data: [65, 59, 80, 81, 56, 55, 40],
//     fill: false,
//     borderColor: 'rgb(75, 192, 192)',
//     tension: 0.1
//   }]
// };

//   const config = {
//     type: 'line',
//     data: data,
//     options: {
//       responsive: true,
//       plugins: {
//         legend: {
//           position: 'top',
//         },
//         title: {
//           display: true,
//           text: 'Chart.js Line Chart'
//         }
//       }
//     },
//   };

// const scatter_plot = new Chart(ctx,config)

function  GRAPH_avg_sale_price(years,avg_Sale_Price){
  
  // 
  const ctx = document.getElementById('myChart');
  const DATA_COUNT = years.length;
  const NUMBER_CFG = {count: DATA_COUNT, min: -100, max: 100};
  
  const labels = years;
  const data = {
    labels: labels,
    datasets: [{
      label: 'Amount in thousands USD',
      data: avg_Sale_Price,
      fill: false,
      borderColor: 'rgb(75, 192, 192)',
      backgroundColor: [
        'rgba(255, 99, 132)',
      ],
      // tension: 0.1
    }]
  };
  
    const config = {
      type: 'bar',
      data: data,
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'top',
          },
          title: {
            display: true,
            text: 'Avg Sale Price For Each Model Year'
          }
        }
      },
    };
  
  const line_chart= new Chart(ctx,config)
    
}



// function PLOT_create_scatter(){
//   // 
//   const ctx = document.getElementById('myChart');
//   const DATA_COUNT = years.length;
//   const NUMBER_CFG = {count: DATA_COUNT, min: -100, max: 100};
  
//   const labels = years;
//   const data = {
//     labels: labels,
//     datasets: [{
//       label: 'My First Dataset',
//       data: avg_Sale_Price,
//       fill: false,
//       borderColor: 'rgb(75, 192, 192)',
//       tension: 0.1
//     }]
//   };
  
//     const config = {
//       type: 'line',
//       data: data,
//       options: {
//         responsive: true,
//         plugins: {
//           legend: {
//             position: 'top',
//           },
//           title: {
//             display: true,
//             text: 'Chart.js Line Chart'
//           }
//         }
//       },
//     };
  
//   const line_chart = new Chart(ctx,config)
    
// }
