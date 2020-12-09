const { func } = require("prop-types");
const  db_config = require(__dirname + '/../config/database.js');
var conn = db_config.init();

db_config.connect(conn);

module.exports = function(app) {
    app.get('/', function(req, res) {
        res.render('welcome.ejs')
    });

    app.get('/list', function(req, res) {
        var sql1 = 'SELECT * FROM store_info'
        var sql2 = 'SELECT * FROM store_status'
        conn.query(sql1, function(err1, rows1, fields1) {
            if(err1) console.log('query is not excuted. select fail...\n' + err1);
            else conn.query(sql2, function(err2, rows2, field2) {
                if(err2) console.log('query is not excuted. select fail...\n' + err2);
                else res.render('list.ejs', {list1 : rows1}, {list2 : rows2});
            });
        });
    });
}