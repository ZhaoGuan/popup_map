var myChart = echarts.init(document.getElementById('main'));
var option;
var rawData = [];
getData();
var popPictureInterval;
setInterval(function () {
    getData();
}, 60 * 1000);

function getData() {
    $.ajax({
        url: 'http://52.26.206.94:8000/map/data',
        method: 'get',
        dataType: 'json',
        success: function (res) {
            console.log(res);
            if (res.status === 0) {
                rawData = res.data;
                updateChart(rawData);
            }
        }
    })
}

function makeMapData(rawData) {
    var mapData = [];
    for (var i = 0; i < rawData.length; i++) {
        var isShow = false;
        if (Math.random() > 0.999) {
            isShow = true;
        }
        var url = rawData[i][4];
        mapData.push({
            name: rawData[i][0],
            value: rawData[i].slice(1, 4),
            label: {
                normal: {
                    show: isShow,
                    formatter: function () {
                        return '{bg|}';
                    },
                    rich: {
                        bg: {
                            height: 50,
                            backgroundColor: {
                                image: url
                            },
                            position:'top'
                        }
                    }
                },
                emphasis: {
                    show: true
                }

            }
        });
    }
    return mapData;
};

function updateChart (rawData) {
    option = {
        backgroundColor: new echarts.graphic.RadialGradient(0.5, 0.5, 0.4, [{
            offset: 0,
//            color: '#4b5769'
            color: '#3b444b'
        }, {
            offset: 1,
//            color: '#404a59'
            color: '#3b444b'
        }]),
        title: {
            text: 'Popup',
            left: 'center',
            top: 30,
            itemGap: 0,
            textStyle: {
                color: '#eee'
            },
            z: 200
        },
        visualMap: {
            color: ['#d94e5d','#f2c96d','#49e413'],
//            color: ['#d94e5d','#ff66cc','#49e413'],
            textStyle: {
                color: '#555'
            },
            inverse: true,
            backgroundColor: '#fff',
            left: 20,
            bottom: 20,
            pieces: [
                {gt: 10, lt: 200, label:'10-200'},
                {gt: 200, lt: 500, label: '200-500'},
                {gt: 500, label:'500+'}
            ]
        },
        geo: {
            map: 'world',
            silent: true,
            label: {
                normal: {
                    show: false
                },
                emphasis: {
                    show: false,
                    areaColor: '#eee'
                }
            },
            itemStyle: {
                normal: {
                    borderWidth: 0.2,
//                    borderColor: '#404a59',
                    borderColor: '#778899',
//                    areaColor: '#a1bda3'
                    areaColor: '#000000'
                }
            },
            roam: true
            // regions: coldata
        },
        series: [
            {
                name: 'Prices and Earnings 2012',
                type: 'scatter',
                coordinateSystem: 'geo',
                symbolSize: 8,
                data: makeMapData(rawData),
                activeOpacity: 1,
                symbolSize: function (data) {
                    if (data[2] > 500) {
                        return Math.min(25, 9 + (data[2] - 500) / 100);
                    } else if (data[2] <= 500 && data[2] > 200) {
                        return 8;
                    } else if (data[2] <= 200 && data[2] > 10) {
                        return 4;
                    } else {
                        return 4;
                    }
                },
                itemStyle: {
                    normal: {
                        color: '#577ceb'
                    }
                }
            }
        ]
    };
    clearInterval(popPictureInterval);
    myChart.setOption(option);
    popPictureInterval = setInterval(function () {
        var data = makeMapData(rawData);
        option.series[0].data = data;
        myChart.setOption(option);
    }, 5 * 1000)
}
window.onresize = function () {
    if (myChart) {
        myChart.resize()
    }
};

