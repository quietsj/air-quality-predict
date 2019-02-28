$(function() {
    /* ChartJS
     * -------
     * Data and config for chartjs
     */
    'use strict';

    var AirQualityIndexHistory = {
        labels: dateHistory,
        datasets: [{
            label: 'Air Quality Index History data',
            data: aqiHistory,
            borderColor: ['rgba(255, 0, 0, 1)'],
            backgroundColor: ['rgba(255, 0, 0, 1)'],
            borderWidth: 2,
            fill: false
        }
        ]
    };


    var AirQualityIndexFuture = {
        labels: dateFuture,
        datasets: [{
            label: 'knn predict',
            data: knnFuture,
            borderColor: ['rgba(0, 0, 255, 1)'],
            backgroundColor: ['rgba(0, 0, 255, 1)'],
            borderWidth: 2,
            fill: false
        },
        {
            label: 'gbdt predict',
            data: gbdtFuture,
            borderColor: ['rgba(0, 255, 0, 1)'],
            backgroundColor: ['rgba(0, 255, 0, 1)'],
            borderWidth: 2,
            fill: false
        },
        {
            label: 'nn predict',
            data: nnFuture,
            borderColor: ['rgba(255, 255, 0, 1)'],
            backgroundColor: ['rgba(255, 255, 0, 1)'],
            borderWidth: 2,
            fill: false
        }
        ]
    };


    var IndexOptions = {
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


    if ($("#Air-Quality-Index-History").length) {
        var AirQualityIndexCanvas = $("#Air-Quality-Index-History").get(0).getContext("2d");
        var AirQualityIndexChartH = new Chart(AirQualityIndexCanvas, {
            type: 'line',
            data: AirQualityIndexHistory,
            options: IndexOptions
        });
    }

    if ($("#Air-Quality-Index-Future").length) {
        var AirQualityIndexCanvas = $("#Air-Quality-Index-Future").get(0).getContext("2d");
        var AirQualityIndexChartF = new Chart(AirQualityIndexCanvas, {
            type: 'line',
            data: AirQualityIndexFuture,
            options: IndexOptions
        });
    }


});