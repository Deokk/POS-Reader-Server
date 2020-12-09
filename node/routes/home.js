const { func } = require("prop-types");

module.exports = function(app) {
    app.get('/', function(req, res) {
        res.render('welcome.ejs')
    });

    app.get('/list', function(req, res) {
        res.render('list.ejs');
    });
}