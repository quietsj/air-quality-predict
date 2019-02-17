$(function() {
  /* ChartJS
   * -------
   * Data and config for chartjs
   */
  'use strict';

  var KNearestNeighborsData = {
    labels: knnLabel,
    datasets: [{
        label: 'Real',
        data: knnReal,
        borderColor: ['rgba(255, 0, 0, 1)'],
        backgroundColor: ['rgba(255, 0, 0, 1)'],
        borderWidth: 2,
        fill: false
      },
      {
        label: 'Predict',
        data: knnPredict,
        borderColor: ['rgba(0, 0, 255, 1)'],
        backgroundColor: ['rgba(0, 0, 255, 1)'],
        borderWidth: 2,
        fill: false
      }
    ]
  };

  var GradientTreeBoostingData = {
        labels: gbtLabel,
        datasets: [{
            label: 'Real',
            data: gbtReal,
            borderColor: ['rgba(255, 0, 0, 1)'],
            backgroundColor: ['rgba(255, 0, 0, 1)'],
            borderWidth: 2,
            fill: false
        },
        {
            label: 'Predict',
            data: gbtPredict,
            borderColor: ['rgba(0, 0, 255, 1)'],
            backgroundColor: ['rgba(0, 0, 255, 1)'],
            borderWidth: 2,
            fill: false
        }
        ]
    };

    var CompareOptions = {
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
                    display: true
                }
            }],
            yAxes: [{
                gridLines: {
                    display: true
                }
            }]
        }
    };


    if ($("#K-Nearest-Neighbors").length) {
    var KNearestNeighborsCanvas = $("#K-Nearest-Neighbors").get(0).getContext("2d");
    var KNearestNeighborsChart = new Chart(KNearestNeighborsCanvas, {
      type: 'line',
      data: KNearestNeighborsData,
      options: CompareOptions
    });
  }


  if ($("#Gradient-Tree-Boosting").length) {
      var GradientTreeBoostingCanvas = $("#Gradient-Tree-Boosting").get(0).getContext("2d");
      var GradientTreeBoostingChart = new Chart(GradientTreeBoostingCanvas, {
          type: 'line',
          data: GradientTreeBoostingData,
          options: CompareOptions
      });
  }

});