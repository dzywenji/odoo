odoo.define('test_website.json_auth', function (require) {
'use strict';

var tour = require('web_tour.tour');
var session = require('web.session')

tour.register('test_json_auth', {
    test: true,
}, [{
    trigger: 'body',
    run: async function () {
        await session.rpc('/test_get_dbname').then( function (result){
            return session.rpc("/web/session/authenticate", {
                db: result,
                login: 'admin',
                password: 'admin'
            });
        });
        window.location.href = window.location.origin;
    },
}, {
<<<<<<< HEAD
    trigger: 'span:contains(Mitchell Admin)',
=======
    trigger: 'span:contains(Mitchell Admin), span:contains(Administrator)',
>>>>>>> f0a66d05e70e432d35dc68c9fb1e1cc6e51b40b8
    run: function () {},
}
]);
});
