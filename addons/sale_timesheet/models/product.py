# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    service_policy = fields.Selection([
        ('ordered_timesheet', 'Ordered quantities'),
        ('delivered_timesheet', 'Timesheets on tasks'),
        ('delivered_manual', 'Milestones (manually set quantities on order)')
    ], string="Service Invoicing Policy", compute='_compute_service_policy', inverse='_inverse_service_policy')
    service_type = fields.Selection(selection_add=[
        ('timesheet', 'Timesheets on project (one fare per SO/Project)'),
<<<<<<< HEAD
    ])
    service_tracking = fields.Selection([
        ('no', 'Don\'t create task'),
        ('task_global_project', 'Create a task in an existing project'),
        ('task_in_project', 'Create a task in sales order\'s project'),
        ('project_only', 'Create a new project but no task'),
        ], string="Service Tracking", default="no",
        help="On Sales order confirmation, this product can generate a project and/or task. \
        From those, you can track the service you are selling.\n \
        'In sale order\'s project': Will use the sale order\'s configured project if defined or fallback to \
        creating a new project based on the selected template.")
    project_id = fields.Many2one(
        'project.project', 'Project', company_dependent=True, domain=[('billable_type', '=', 'no')],
        help='Select a non billable project on which tasks can be created. This setting must be set for each company.')
    project_template_id = fields.Many2one(
        'project.project', 'Project Template', company_dependent=True, domain=[('billable_type', '=', 'no')], copy=True,
        help='Select a non billable project to be the skeleton of the new created project when selling the current product. Its stages and tasks will be duplicated.')
=======
    ], ondelete={'timesheet': 'set default'})
    # override domain
    project_id = fields.Many2one(domain="[('billable_type', '=', 'no'), ('allow_timesheets', 'in', [service_policy == 'delivered_timesheet' or '', True])]")
    project_template_id = fields.Many2one(domain="[('billable_type', '=', 'no'), ('allow_timesheets', 'in', [service_policy == 'delivered_timesheet' or '', True])]")

    def _default_visible_expense_policy(self):
        visibility = self.user_has_groups('project.group_project_user')
        return visibility or super(ProductTemplate, self)._default_visible_expense_policy()

>>>>>>> f0a66d05e70e432d35dc68c9fb1e1cc6e51b40b8

    def _default_visible_expense_policy(self):
        visibility = self.user_has_groups('project.group_project_user')
        return visibility or super(ProductTemplate, self)._default_visible_expense_policy()


    def _compute_visible_expense_policy(self):
        super(ProductTemplate, self)._compute_visible_expense_policy()

        visibility = self.user_has_groups('project.group_project_user')
        for product_template in self:
            if not product_template.visible_expense_policy:
                product_template.visible_expense_policy = visibility

    @api.depends('invoice_policy', 'service_type')
    def _compute_service_policy(self):
        for product in self:
            policy = None
            if product.invoice_policy == 'delivery':
                policy = 'delivered_manual' if product.service_type == 'manual' else 'delivered_timesheet'
            elif product.invoice_policy == 'order' and (product.service_type == 'timesheet' or product.type == 'service'):
                policy = 'ordered_timesheet'
            product.service_policy = policy

    def _inverse_service_policy(self):
        for product in self:
            policy = product.service_policy
            if not policy and not product.invoice_policy =='delivery':
                product.invoice_policy = 'order'
                product.service_type = 'manual'
            elif policy == 'ordered_timesheet':
                product.invoice_policy = 'order'
                product.service_type = 'timesheet'
            else:
                product.invoice_policy = 'delivery'
                product.service_type = 'manual' if policy == 'delivered_manual' else 'timesheet'

    @api.onchange('type')
    def _onchange_type(self):
        res = super(ProductTemplate, self)._onchange_type()
        if self.type == 'service' and not self.invoice_policy:
            self.invoice_policy = 'order'
            self.service_type = 'timesheet'
        elif self.type == 'service' and self.invoice_policy == 'order':
            self.service_policy = 'ordered_timesheet'
        elif self.type == 'consu' and not self.invoice_policy and self.service_policy == 'ordered_timesheet':
            self.invoice_policy = 'order'
        return res


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _is_delivered_timesheet(self):
        """ Check if the product is a delivered timesheet """
        self.ensure_one()
        return self.type == 'service' and self.service_policy == 'delivered_timesheet'
