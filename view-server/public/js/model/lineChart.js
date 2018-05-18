class LineChart {
    constructor(_index, _type, _field, _selector, _text, _baseValue = 0) {
        var index = _index;
        var type = _type;
        var field = _field;
        var seletor = _selector;
        var text = _text;
        var baseValue = _baseValue;
        var data = [];
        var chart;

        jui.ready(['chart.builder'], function (builder) {
            chart = builder('#' + seletor, {
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
                        //domain: [0, 100]
                        domain: function (d) {
                            return Math.max(100,Math.max.apply(Math, data.map(function (o) { return o.RealtimeData; })));
                        }
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

            if (!baseValue) {
                initData(100);
            } else {
                getRealtimeData(index, type, baseValue, function (_resp) {
                    baseValue = _resp;
                    initData(100);
                });
            }
        });

        function getRealtimeData(_index, _type, _field, callback) {
            client.search({
                index: _index,
                type: _type,
                body: {
                    'query': { 'match_all': {} },
                    '_source': [_field, '@timestamp'],
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
                if(!baseValue)
                    callback(eval('resp.hits.hits[0]._source.' + _field).toFixed(3) * 100);
                else
                    callback(eval('resp.hits.hits[0]._source.' + _field));
            }, function (err) {
                console.trace(err.message);
                callback(0);
            });
        }

        function getAverageData(_index, _type, _field, callback) {
            client.search({
                index: _index,
                type: _type,
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
                                'field': _field
                            }
                        }
                    }
                }
            }).then(function (_resp) {
                if(!baseValue)
                    callback(_resp.aggregations.avg_usage.value.toFixed(3) * 100);
                else
                    callback(_resp.aggregations.avg_usage.value);
            }, function (_err) {
                console.trace(_err.message);
                callback(0);
            });
        }

        function initData(_count) {
            getAverageData(index, type, field, function (_averageData) {
                for (var i = 0; i < _count; i++) {
                    if(baseValue)
                        _averageData = 0;
                    data[i] = {
                        RealtimeData: _averageData,
                        AverageData: _averageData
                    };
                }
                updateData();
                checkHealth();
            });
        }

        function updateData() {

            var startTime, tookTime;

            var end = new Date(),
                start = new Date() - 1000 * 60 * 5,
                domain = [start, end];

            startTime = new Date().getTime();

            getRealtimeData(index, type, field, function (_realtimeData) {
                getAverageData(index, type, field, function (_averageData) {

                    if(baseValue){
                        _realtimeData = getPercentage(baseValue, _realtimeData);
                        _averageData = getPercentage(baseValue, _averageData);
                    }

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
                    }, 5000 - tookTime);
                });
            });

        }

        function checkHealth() {
            setInterval(function () {
                var realtimeData = data[data.length - 1]['RealtimeData'];
                var averageData = data[data.length - 1]['AverageData'];
                var diff = realtimeData - averageData;

                if (diff >= 30 || realtimeData >= 90 || realtimeData == 0) {
                    $('#' + _selector + ' > svg').css('background-color', 'red');
                } else if (diff >= 20 || realtimeData >= 80) {
                    $('#' + _selector + ' > svg').css('background-color', 'red');
                }
            }, 4000);
        }

        function getPercentage(base, per) {
            return ((per / base * 100).toFixed(3));
        }
    }
};
