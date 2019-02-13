$(function() {
  /* ChartJS
   * -------
   * Data and config for chartjs
   */
  'use strict';

  var KNearestNeighborsData = {
    labels: chartLabel,
    datasets: [{
        label: 'Real',
        data: chartReal,
        borderColor: ['rgba(255, 0, 0, 1)'],
        backgroundColor: ['rgba(255, 0, 0, 1)'],
        borderWidth: 2,
        fill: false
      },
      {
        label: 'Predict',
        data: chartPredict,
        borderColor: ['rgba(0, 0, 255, 1)'],
        backgroundColor: ['rgba(0, 0, 255, 1)'],
        borderWidth: 2,
        fill: false
      }
    ]
  };

  var KNearestNeighborsOptions = {
    plugins: {
      filler: {
        propagate: true
      }
    },
    elements: {
      point: {
        radius: 2
      }
    },
    scales: {
      xAxes: [{
        gridLines: {
          display: false
        }
      }],
      yAxes: [{
        gridLines: {
          display: false
        }
      }]
    }
  };

  var GradientTreeBoostingData = {
        labels: chartLabel,
        datasets: [{
            label: 'Real',
            data: chartReal,
            borderColor: ['rgba(255, 0, 0, 1)'],
            backgroundColor: ['rgba(255, 0, 0, 1)'],
            borderWidth: 2,
            fill: false
        },
            {
                label: 'Predict',
                data: chartPredict,
                borderColor: ['rgba(0, 0, 255, 1)'],
                backgroundColor: ['rgba(0, 0, 255, 1)'],
                borderWidth: 2,
                fill: false
            }
        ]
    };

  var GradientTreeBoostingOptions = {
        plugins: {
            filler: {
                propagate: true
            }
        },
        elements: {
            point: {
                radius: 2
            }
        },
        scales: {
            xAxes: [{
                gridLines: {
                    display: false
                }
            }],
            yAxes: [{
                gridLines: {
                    display: false
                }
            }]
        }
    };

  if ($("#K-Nearest-Neighbors").length) {
    var KNearestNeighborsCanvas = $("#K-Nearest-Neighbors").get(0).getContext("2d");
    var KNearestNeighborsChart = new Chart(KNearestNeighborsCanvas, {
      type: 'line',
      data: KNearestNeighborsData,
      options: KNearestNeighborsOptions
    });
  }


  if ($("#Gradient-Tree-Boosting").length) {
      var GradientTreeBoostingCanvas = $("#Gradient-Tree-Boosting").get(0).getContext("2d");
      var GradientTreeBoostingChart = new Chart(GradientTreeBoostingCanvas, {
          type: 'line',
          data: GradientTreeBoostingData,
          options: GradientTreeBoostingOptions
      });
  }

});