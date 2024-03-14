from odoo import fields, models


class SubscriptionCrm(models.Model):
    _inherit = 'crm.lead'

    order_id = fields.Char()
    _sql_constraints = [('order_id',
                         'unique(order_id)',
                         'Order_id must be a unique value')]
