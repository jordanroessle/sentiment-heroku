d3.json("http://127.0.0.1:5000/data").then(function(data) {
    console.log(data)
    xplotData = []
    yplotData = []

    var data2 = Object.entries(data)
    data2.forEach(function([key]) {
      console.log(data2[key][1]);
    //   if (data2[key][1]['predicted_sentiments'] < .5) {
    //     xplotData.push(0)
    // } else {
    //     xplotData.push(1)

    // }
        xplotData.push(data2[key][1]['predicted_sentiments'])
        yplotData.push(data2[key][1]['sentiments'])



    });



    var trace1 = {
        x: xplotData,
        y: yplotData,
        mode: 'markers',
        type: "scatter"
      };

      var trace2 = {
        x: [.5,.5],
        y: [0,1],
        mode: 'line',
        type: "scatter"
      };
      var trace3 = {
        x: [0,1],
        y: [.5,.5],
        mode: 'line',
        type: "scatter"
      };
      var layout = {
        title: {
          text:'Confusion',
          font: {
            family: 'Courier New, monospace',
            size: 24
          },
          xref: 'paper',
          x: 0.05,
        },
        xaxis: {
          title: {
            text: 'Predicted Values',
            font: {
              family: 'Courier New, monospace',
              size: 18,
              color: '#7f7f7f'
            }
          },
        },
        yaxis: {
          title: {
            text: 'Actual Values',
            font: {
              family: 'Courier New, monospace',
              size: 18,
              color: '#7f7f7f'
            }
          }
        }
      };
      var traceData = [trace1,trace2,trace3]

      Plotly.newPlot("scatter", traceData,layout);
   
console.log(xplotData)
console.log(yplotData)








})