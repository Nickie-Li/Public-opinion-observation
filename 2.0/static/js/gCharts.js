// googlecharts
// var dayColor = ["#FF2626", "#f39c13", "#ffd000", "#86ff42", "#00ff97", "#3db4ff", "#3d46ff", "#9c3dff", "#ff57f9", "#ff579e"];
var dayColor = ["#580c0d","#701112","#851516","#9b191c","#b11d22","#c22028","#d32730","#e72e3b","#ff3949","#ff505f"];
var monthColor=["#313131","#424242","#505050","#636363","#747474","#888888","#979696","#acacac","#bdbdbd","#cfcfcf"]
var weekColor=["rgb(63, 58, 46)", "rgb(78, 72, 57)", "rgb(92, 85, 66)", "rgb(104, 97, 75)", "rgb(117, 110, 85)", "rgb(129, 122, 95)", "rgb(146, 139, 108)", "rgb(161, 153, 120)", "#C5BD99", "rgb(214, 205, 163)"];

gchart(dayChart, weekChart, monthChart)


function gchart(dayChart, weekChart, monthChart) {
// function gchart(dayChart, weekChart) {
  // Load the Visualization API and the corechart package.
  google.charts.load('current', { 'packages': ['corechart'] });

  // Set a callback to run when the Google Visualization API is loaded.
  var daytb, weektb, monthtb;
  daytb = [["Element", "Density", { role: "style" }]];
  weektb = [["Element", "Density", { role: "style" }]];
  monthtb = [["Element", "Density", { role: "style" }]];

  for(var i=0;i<dayChart.length;i++){
    daytb.push([dayChart[i].words, dayChart[i].wordsCount, dayColor[i]]);
  }
  for(var i=0;i<weekChart.length;i++){
    weektb.push([weekChart[i].words, weekChart[i].wordsCount, weekColor[i]]);
  }
  for(var i=0;i<monthChart.length;i++){
    monthtb.push([monthChart[i].words, monthChart[i].wordsCount, monthColor[i]]);
  }
  // console.log(daytb);
  google.charts.setOnLoadCallback(
    function () {
      drawDayChart(daytb);
      drawWeekChart(weektb);
      drawMonthChart(monthtb);
    });
}


// Callback that creates and populates a data table,
// instantiates the column chart, passes in the data and
// draws it.


function drawDayChart(daytb) {

  // var arytb=[["Element", "Density", { role: "style" }]];
  // for(var i=0;i<10;i++){
  //   arytb.push([myObj[i].words,myObj[i].wordsCount,gColor[i]]);
  // }

  var data = google.visualization.arrayToDataTable(daytb);


  var view = new google.visualization.DataView(data);
  view.setColumns([0, 1,
    {
      calc: "stringify",
      sourceColumn: 1,
      type: "string",
      role: "annotation"
    },
    2]);

  var options = {
    title: "",
    width: 800,
    height: 400,
    bar: { groupWidth: "70%" },
    legend: { position: "none" },
  };
  var chart = new google.visualization.ColumnChart(document.getElementById("day_chart_div"));
  chart.draw(view, options);
}

function drawWeekChart(weektb) {
  var data = google.visualization.arrayToDataTable(weektb);


  var view = new google.visualization.DataView(data);
  view.setColumns([0, 1,
    {
      calc: "stringify",
      sourceColumn: 1,
      type: "string",
      role: "annotation"
    },
    2]);

  var options = {
    title: "",
    width: 800,
    height: 400,
    bar: { groupWidth: "70%" },
    legend: { position: "none" },
  };
  var chart = new google.visualization.ColumnChart(document.getElementById("week_chart_div"));
  chart.draw(view, options);

}

function drawMonthChart(monthtb) {
  var data = google.visualization.arrayToDataTable(monthtb);


  var view = new google.visualization.DataView(data);
  view.setColumns([0, 1,
    {
      calc: "stringify",
      sourceColumn: 1,
      type: "string",
      role: "annotation"
    },
    2]);

  var options = {
    title: "",
    width: 800,
    height: 400,
    bar: { groupWidth: "70%" },
    legend: { position: "none" },
  };
  var chart = new google.visualization.ColumnChart(document.getElementById("month_chart_div"));
  chart.draw(view, options);
}