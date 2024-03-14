from odoo import fields, models


class BillingSchedule(models.Model):
    _name = 'billing.schedule'
    _description = 'Billing Schedule'
    _inherit = 'mail.thread'

    name = fields.Char(help='Add a name')
    simulation = fields.Boolean(default=True)
    period = fields.Date(help='Add period date')
    restrict_customer_ids = fields.Many2many(comodel_name='res.partner')
    active = fields.Boolean(default=False)
    recurring_subscription_ids = fields.Many2many(comodel_name='recurring.subscription',
                                                  help='Add recurring subscription ')
    subscription_count = fields.Integer(compute='_compute_subscription_count')

    def _compute_subscription_count(self):
        for record in self:
            record.subscription_count = len(record.recurring_subscription_ids)

    def action_get_record(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'subscription',
            'view_mode': 'tree',
            'res_model': 'recurring.subscription',
            'domain': [('id', 'in', self.recurring_subscription_ids.ids)],
        }
