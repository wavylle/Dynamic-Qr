// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Pie Chart Example
fetch('http://127.0.0.1:8000/records/creditRecJsonAll').then(response => response.json()).then(data => {
  var total_paid = 0
  var total_unpaid = 0
  var total_received = 0
  var total_unreceived = 0
  for(let u = 0; u < data.length; u++) {
    if(data[u]['self_status'] === 'Paid') {
    total_paid += 1
  }
    else if(data[u]['self_status'] === 'Unpaid') {
      total_unpaid += 1
    }
    else if(data[u]['self_status'] === 'Received') {
      total_received += 1
    }
    else if(data[u]['self_status'] === 'Unreceived') {
      total_unreceived += 1
    }
  }
var ctx = document.getElementById("myPieChart");
var myPieChart = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: ["Paid", "Unpaid", "Received", "Unreceived"],
    datasets: [{
      data: [total_paid, total_unpaid, total_received, total_unreceived],
      backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc'],
      hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf'],
      hoverBorderColor: "rgba(234, 236, 244, 1)",
    }],
  },
  options: {
    maintainAspectRatio: false,
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
    },
    legend: {
      display: false
    },
    cutoutPercentage: 80,
  },
});

})
