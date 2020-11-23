const mysql = require('mysql');
const express = require('express');
const cors = require('cors');
var bodyParser = require('body-parser')

const connection = mysql.createPool({
  host     : 'project-dsci551-ranks.c8u9e3pxnupz.us-east-1.rds.amazonaws.com',
  user     : 'mbrennan6',
  password : 'songdsci551',
  database : 'songRanks'
});

const app = express();
app.use(cors());
app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json())
app.options('*', cors());

app.get('/ranks', function (req, res) {
    connection.getConnection(function (err, connection) {
    connection.query('SELECT Distinct(song) FROM ranks order by RAND() LIMIT 1', (error, results) => {
      if (error) throw error;

      console.log(results[0].song)
      res.send(results[0])
    });
  });
});

app.post('/ranks/posts', function (req, res) {
      res.send({ status: 'SUCCESS' });
      connection.getConnection(function (err, connection) {
        connection.query('INSERT INTO ranks SET ?', req.body, (error, results) => {
          if (error) throw error;

          if (!Object.keys(req.body).length === 0) {
            res.redirect('back')
          }
        });
      });
      return;
});


app.listen(8080, () => {
  console.log('Go to http://localhost:8080/ranks so you can see the data.');
 });