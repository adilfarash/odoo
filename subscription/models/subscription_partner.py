from odoo import models, fields


class SubscriptionPartner(models.Model):
    _inherit = 'res.partner'

    establishment_id = fields.Char()
    account_id = fields.Many2one('partner.account.id', ondelete='cascade')

    _sql_constraints = [('establishment_id',
                         'unique(establishment_id)',
                         'Establishment_id must have a  unique value')]
