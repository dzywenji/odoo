# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SMSTemplatePreview(models.TransientModel):
    _name = "sms.template.preview"
    _description = "SMS Template Preview"

    @api.model
    def _selection_target_model(self):
        models = self.env['ir.model'].search([])
        return [(model.model, model.name) for model in models]

    @api.model
    def _selection_languages(self):
        return self.env['res.lang'].get_installed()

    @api.model
    def default_get(self, fields):
        result = super(SMSTemplatePreview, self).default_get(fields)
        sms_template_id = self.env.context.get('default_sms_template_id')
        if not sms_template_id or 'resource_ref' not in fields:
            return result
        sms_template = self.env['sms.template'].browse(sms_template_id)
        res = self.env[sms_template.model_id.model].search([], limit=1)
        if res:
            result['resource_ref'] = '%s,%s' % (sms_template.model_id.model, res.id)
        return result

<<<<<<< HEAD
    sms_template_id = fields.Many2one('sms.template') # NOTE This should probably be required

    lang = fields.Selection(_selection_languages, string='Template Preview Language')
    model_id = fields.Many2one('ir.model', related="sms_template_id.model_id")
    res_id = fields.Integer(string='Record ID')
    resource_ref = fields.Reference(string='Record reference', selection='_selection_target_model', compute='_compute_resource_ref', inverse='_inverse_resource_ref')

    @api.depends('model_id', 'res_id')
    def _compute_resource_ref(self):
        for preview in self:
            if preview.model_id:
                preview.resource_ref = '%s,%s' % (preview.model_id.model, preview.res_id or 0)
            else:
                preview.resource_ref = False
=======
    sms_template_id = fields.Many2one('sms.template', required=True, ondelete='cascade')
    lang = fields.Selection(_selection_languages, string='Template Preview Language')
    model_id = fields.Many2one('ir.model', related="sms_template_id.model_id")
    body = fields.Char('Body', compute='_compute_sms_template_fields')
    resource_ref = fields.Reference(string='Record reference', selection='_selection_target_model')
    no_record = fields.Boolean('No Record', compute='_compute_no_record')
>>>>>>> f0a66d05e70e432d35dc68c9fb1e1cc6e51b40b8

    @api.depends('model_id')
    def _compute_no_record(self):
        for preview in self:
<<<<<<< HEAD
            if preview.resource_ref:
                preview.res_id = preview.resource_ref.id

    @api.onchange('lang', 'resource_ref')
    def on_change_resource_ref(self):
        # Update res_id and body depending of the resource_ref
        if self.resource_ref:
            self.res_id = self.resource_ref.id
        if self.sms_template_id:
            template = self.sms_template_id.with_context(lang=self.lang)
            self.body = template._render_template(template.body, template.model, self.res_id or 0) if self.resource_ref else template.body
=======
            preview.no_record = (self.env[preview.model_id.model].search_count([]) == 0) if preview.model_id else True

    @api.depends('lang', 'resource_ref')
    def _compute_sms_template_fields(self):
        for wizard in self:
            if wizard.sms_template_id and wizard.resource_ref:
                wizard.body = wizard.sms_template_id._render_field('body', [wizard.resource_ref.id], set_lang=wizard.lang)[wizard.resource_ref.id]
            else:
                wizard.body = wizard.sms_template_id.body
>>>>>>> f0a66d05e70e432d35dc68c9fb1e1cc6e51b40b8
