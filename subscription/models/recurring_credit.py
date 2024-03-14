from odoo import api, fields, models


class RecurringCredit(models.Model):
    _name = 'recurring.credit'
    _description = 'Recurring Credit'
    _rec_name = 'recurring_subscription_id'
    _inherit = 'mail.thread'

    recurring_subscription_id = fields.Many2one(comodel_name='recurring.subscription',
                                                help='Select recurring subscription order')
    establishment_id = fields.Char(related="recurring_subscription_id.establishment_id")
    due_date = fields.Date(related="recurring_subscription_id.due_date")
    partner_id = fields.Many2one(related="recurring_subscription_id.customer_id")
    company_id = fields.Many2one(related="recurring_subscription_id.company_id")
    recurring_amount = fields.Float(related="recurring_subscription_id.recurring_amount")
    credit_amount = fields.Float(help="Enter the credit amount", string="Credit Amount")
    period_date = fields.Date(help="enter the date", string="Period Date")
    state = fields.Selection(
        selection=[('pending', 'Pending'),
                   ('confirm', 'Confirm'),
                   ('first_approved', 'First Approved'),
                   ('fully_approved', 'Fully Approved'),
                   ('rejected', 'Rejected')], default='pending', tracking=True)

    @api.onchange('credit_amount')
    def _onchange_credit_amount(self):
        if self.credit_amount == 0:
            self.recurring_subscription_id = ''
        elif self.credit_amount > self.recurring_amount:
            self.recurring_subscription_id = ''
