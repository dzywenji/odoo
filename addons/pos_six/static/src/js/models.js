odoo.define('pos_six.models', function (require) {

var models = require('point_of_sale.models');
var PaymentSix = require('pos_six.payment');

<<<<<<< HEAD
models.register_payment_method('six_tim', PaymentSix);
=======
models.register_payment_method('six', PaymentSix);
>>>>>>> f0a66d05e70e432d35dc68c9fb1e1cc6e51b40b8
models.load_fields('pos.payment.method', ['six_terminal_ip']);

});
