var express = require('express');
var app = express();

app.use(express.static('public'));
app.use('/jquery', express.static(__dirname + '/node_modules/jquery/'));
app.use('/jui-core', express.static(__dirname + '/node_modules/jui-core/'));
app.use('/jui-chart', express.static(__dirname + '/node_modules/jui-chart/'));
app.use('/elasticsearch-browser', express.static(__dirname + '/node_modules/elasticsearch-browser/'));

app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');
app.engine('html', require('ejs').renderFile);

app.get('index/:index', function (req, res) {
  res.render('index.html', { index: req.params.index});
});

app.get('/cpu', function (req, res) {
  res.render('cpu.html');
});

app.get('/memory', function (req, res) {
  res.render('memory.html');
});

app.get('/disk', function (req, res) {
  res.render('disk.html');
});

app.listen(3000, function () {
  console.log('App listening on port 3000!');
});

