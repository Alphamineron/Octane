console.log("Server is Starting");

const dataHub = require('./dataHub');


const express = require('express');
const bodyParser = require('body-parser');

const PORT = 3000;
const app = express();

const server = app.listen(PORT, listening);
function listening() {
    console.log(`Server is listening on port: ${PORT}`);
}

app.use(express.static('FrontEnd'));

app.get("/all", api_getAll);

function api_getAll(req, res) {
    res.send(dataHub.chips);
}



































// app.get('/import', (req, res) => {
//
//     const { spawn } = require('child_process');
//     const pyProg = spawn('python', ['./main.py']);
//
//     pyProg.stdout.on('data', function(data) {
//
//         console.log(data.toString());
//         res.write(data);
//         res.end('end');
//     });
// })
