$(function() {
  /* ChartJS
   * -------
   * Data and config for chartjs
   */
  'use strict';

  var AirQualityIndexData = {
        labels: Date_,
        datasets: [{
            label: 'AQI',
            data: AQI,
            borderColor: ['rgba(0, 0, 255, 1)'],
            backgroundColor: ['rgba(0, 0, 255, 1)'],
            borderWidth: 2,
            fill: false
        }
        ]
    };

    var HistoryOptions = {
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


  if ($("#Air-Quality-Index-History-Data").length) {
      var AirQualityIndexDataCanvas = $("#Air-Quality-Index-History-Data").get(0).getContext("2d");
      var AirQualityIndexDataChart = new Chart(AirQualityIndexDataCanvas, {
          type: 'line',
          data: AirQualityIndexData,
          options: HistoryOptions
      });
  }

});