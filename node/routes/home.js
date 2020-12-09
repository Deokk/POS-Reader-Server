const { func } = require("prop-types");
const  db_config = require(__dirname + '../config/database.js');
var conn = db_config.init();

db_config.connect(conn);

module.exports = function(app) {
    app.get('/', function(req, res) {
        res.render('welcome.ejs')
    });

    app.get('/list', function(req, res) {
        var sql = 'SELECT * FROM store_info'
        conn.query(sql, function(err, rows, fields) {
            if(err) console.log('query is not excuted. select fail...\n' + err);
            else res.render('list.ejs');
        });
    });
}