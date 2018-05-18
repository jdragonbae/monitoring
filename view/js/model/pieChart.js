class PieChart {
    constructor(_index, _type, _field, _selector, _text) {
        var index = _index;
        var type = _type;
        var field = _field;
        var text = _text;
        var data = [];
        var chart;
        var names = {
            Available : 'Available',
            Usage : 'Usage'
        };

        jui.ready(['chart.builder'], function (builder) {
            chart = builder('#' + _selector, {
                axis: {
                    data: [
                        { Available: 0, Usage: 0 }
                    ]
                },
                brush: {
                    type: 'donut',
                    showText: 'inside',
                    format: function (k, v) {
                        return v + '%';
                    }
                },
                widget: [{
                    type: 'title',
                    text: _text
                }, {
                    type: 'tooltip',
                    orient: 'left',
                    format: function (data, k) {
                        return {
                            key: names[k],
                            value: data[k]
                        }
                    }
                }, {
                    type: 'legend',
                    format: function (k) {
                        return names[k];
                    }
                }],
                style: {
                    titleFontSize: 15,
                    titleFontWeight: 700
                },
                render: false
            });

            updateData();
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

        function updateData() {
            var startTime, tookTime;

            var end = new Date(),
                start = new Date() - 1000 * 60 * 5,
                domain = [start, end];

            startTime = new Date().getTime();

            getRealtimeData(function (_realtimeData) {

                tookTime = new Date().getTime() - startTime;
                data.shift();
                data.push({
                    Usage: _realtimeData,
                    Available: 100 - _realtimeData
                });

                chart.axis(0).update(data);
                chart.render();

                setTimeout(function () {
                    updateData();
                }, 5000 - tookTime);
            });
        }
    }
};
