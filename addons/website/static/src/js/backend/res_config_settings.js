odoo.define('website.settings', function (require) {

<<<<<<< HEAD
var BaseSettingController = require('base.settings').Controller;
var FormController = require('web.FormController');
=======
const BaseSettingController = require('base.settings').Controller;
const core = require('web.core');
const Dialog = require('web.Dialog');
const FieldBoolean = require('web.basic_fields').FieldBoolean;
const fieldRegistry = require('web.field_registry');
const FormController = require('web.FormController');

const QWeb = core.qweb;
const _t = core._t;
>>>>>>> f0a66d05e70e432d35dc68c9fb1e1cc6e51b40b8

BaseSettingController.include({

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * Bypasses the discard confirmation dialog when going to a website because
<<<<<<< HEAD
     * the target website will be the one selected.
=======
     * the target website will be the one selected and when selecting a theme
     * because the theme will be installed on the selected website.
>>>>>>> f0a66d05e70e432d35dc68c9fb1e1cc6e51b40b8
     *
     * Without this override, it is impossible to go to a website other than the
     * first because discarding will revert it back to the default value.
     *
<<<<<<< HEAD
     * @override
     */
    _onButtonClicked: function (ev) {
        if (ev.data.attrs.name === 'website_go_to') {
=======
     * Without this override, it is impossible to install a theme on a website
     * other than the first because discarding will revert it back to the
     * default value.
     *
     * @override
     */
    _onButtonClicked: function (ev) {
        if (ev.data.attrs.name === 'website_go_to'
                || ev.data.attrs.name === 'install_theme_on_current_website') {
>>>>>>> f0a66d05e70e432d35dc68c9fb1e1cc6e51b40b8
            FormController.prototype._onButtonClicked.apply(this, arguments);
        } else {
            this._super.apply(this, arguments);
        }
    },
});
<<<<<<< HEAD
=======

const WebsiteCookiesbarField = FieldBoolean.extend({
    xmlDependencies: ['/website/static/src/xml/website.res_config_settings.xml'],

    _onChange: function () {
        const checked = this.$input[0].checked;
        if (!checked) {
            return this._setValue(checked);
        }

        const cancelCallback = () => this.$input[0].checked = !checked;
        Dialog.confirm(this, null, {
            title: _t("Please confirm"),
            $content: QWeb.render('website.res_config_settings.cookies_modal_main'),
            buttons: [{
                text: 'Do not activate',
                classes: 'btn-primary',
                close: true,
                click: cancelCallback,
            },
            {
                text: 'Activate anyway',
                close: true,
                click: () => this._setValue(checked),
            }],
            cancel_callback: cancelCallback,
        });
    },
});

fieldRegistry.add('website_cookiesbar_field', WebsiteCookiesbarField);
>>>>>>> f0a66d05e70e432d35dc68c9fb1e1cc6e51b40b8
});
