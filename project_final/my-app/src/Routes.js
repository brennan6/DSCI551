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

// Starting our app.
/*const song_rank = {song: "Top of the World", score: "4"}
connection.query('INSERT INTO ranks SET ?', song_rank, (error, results) => {
  // If some error occurs, we throw an error.
  if (error) throw error;

  // Getting the 'response' from the database and sending it to our route. This is were the data is.
  console.log(results)

});*/
const app = express();
app.use(cors());
app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json())
app.options('*', cors());
/*app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  next();
});*/

// Creating a GET route that returns data from the 'users' table.
app.get('/ranks', function (req, res) {
    var result;
    // Connecting to the database.
    connection.getConnection(function (err, connection) {

    // Executing the MySQL query (select all data from the 'users' table).
    connection.query('SELECT * FROM ranks LIMIT 1', (error, results) => {
      // If some error occurs, we throw an error.
      if (error) throw error;
      // Getting the 'response' from the database and sending it to our route. This is were the data is.
      console.log(results[0].song)
      res.send(results[0])
    });
  });
});

app.post('/ranks/posts', function (req, res) {
      res.send({ status: 'SUCCESS' });
      connection.getConnection(function (err, connection) {
        // Executing the MySQL query (select all data from the 'users' table).
        connection.query('INSERT INTO ranks SET ?', req.body, (error, results) => {
          // If some error occurs, we throw an error.
          if (error) throw error;

          if (!Object.keys(req.body).length === 0) {
            res.redirect('back')
          }
          // Getting the 'response' from the database and sending it to our route. This is were the data is.
        });
      });
      return;
        // use post['blah'], etc.
});


app.listen(8080, () => {
  console.log('Go to http://localhost:8080/ranks so you can see the data.');
 });