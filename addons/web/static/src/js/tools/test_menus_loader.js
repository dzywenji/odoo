odoo.define('web.clickEverywhere', function (require) {
    "use strict";
    var ajax = require('web.ajax');
<<<<<<< HEAD
    function startClickEverywhere(menu_id) {
        ajax.loadJS('web/static/src/js/tools/test_menus.js').then(
            function() {
                clickEverywhere(menu_id);
=======
    function startClickEverywhere(xmlId, appsMenusOnly) {
        ajax.loadJS('web/static/src/js/tools/test_menus.js').then(
            function() {
                clickEverywhere(xmlId, appsMenusOnly);
>>>>>>> f0a66d05e70e432d35dc68c9fb1e1cc6e51b40b8
            }
        );
    }
    return startClickEverywhere;
});
