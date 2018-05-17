class LineChart {
    constructor(_index, _type, _field, _selector, _text) {
        var index = _index;
        var type = _type;
        var field = _field;
        var text = _text;
        var data = [];
        var chart;

        jui.ready(['chart.builder'], function (builder) {
            chart = builder('#' + _selector, {
                width: 400,
                height: 100,
                axis: {
                    x: {
                        type: 'dateblock',
                        domain: [new Date() - 1000 * 60 * 5, new Date()],
                        interval: 1,
                        realtime: 'minutes',
                        format: 'hh:mm'
                    },
                    y: {
                        type: 'range',
                        domain: [0, 100]
                        //domain: function (d) {
                        //    return 1.1 * Math.max.apply(Math, data.map(function (o) { return o.latestData; }))
                        //}
                    }
                },
                brush: {
                    type: 'line',
                    target: ['RealtimeData', 'AverageData'],
                    colors: [2, 4]
                },
                widget: [{
                    type: 'cross',
                    yFormat: function (d) {
                        return d.toFixed(3);
                    },
                }, {
                    type: 'title',
                    text: text
                }, {
                    type: 'legend',
                    filter: true
                }],
                style: {
                    axisBorderColor: '#dcdcdc',
                    axisBorderWidth: 2.5,
                    titleFontSize: 15,
                    titleFontWeight: 700
                },

                render: false
            });

            initData(100);
        });

        function getRealtimeData(callback) {
            client.search({
                index: index,
                type: type,
                body: {
                    'query': { 'match_all': {} },
                    '_source': [field, '@timestamp'],
                    'size': 1,
                    'sort': [
                        {
                            '@timestamp': {
                                'order': 'desc'
                            }
                        }
                    ]
                }
            }).then(function (resp) {
                callback(eval('resp.hits.hits[0]._source.' + field).toFixed(3) * 100);
            }, function (err) {
                console.trace(err.message);
                callback(0);
            });
        }

        function getAverageData(callback) {
            client.search({
                index: index,
                type: type,
                body: {
                    'query': {
                        'range': {
                            '@timestamp': {
                                'gte': 'now-5m',
                                'lt': 'now'
                            }
                        }
                    },
                    'size': 0,
                    'aggs': {
                        'avg_usage': {
                            'avg': {
                                'field': field
                            }
                        }
                    }
                }
            }).then(function (_resp) {
                callback( _resp.aggregations.avg_usage.value.toFixed(3) * 100);
            }, function (_err) {
                console.trace(_err.message);
                callback(0);
            });
        }

        function initData(_count) {
            getAverageData(function (_averageData) {
                for (var i = 0; i < _count; i++) {
                    data[i] = {
                        RealtimeData: _averageData,
                        AverageData: _averageData
                    };
                }
                updateData();
            });
        }

        function updateData() {

            var startTime, tookTime;

            var end = new Date(),
                start = new Date() - 1000 * 60 * 5,
                domain = [start, end];

            startTime = new Date().getTime();

            getRealtimeData(function (_realtimeData) {
                getAverageData(function (_averageData) {

                    tookTime = new Date().getTime() - startTime;

                    data.shift();
                    data.push({
                        RealtimeData: _realtimeData,
                        AverageData: _averageData
                    });

                    chart.axis(0).updateGrid('x', { domain: domain });
                    chart.axis(0).update(data);
                    chart.render();

                    setTimeout(function () {
                        updateData();
                    }, 3000 - tookTime);
                });
            });

        }

        function checkHealth(){
        }
    }
};
