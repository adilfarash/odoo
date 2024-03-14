from odoo import api, fields, models, _, re
from odoo.exceptions import ValidationError


class RecurringSubscription(models.Model):
    _name = 'recurring.subscription'
    _description = 'Recurring Subscription'
    _rec_name = 'order_id'
    _inherit = 'mail.thread'

    order_id = fields.Char(readonly=True, default=lambda self: _('New'))
    name = fields.Char(help="Enter the name", required=True)
    establishment_id = fields.Char(help="Enter the Establishment_id")
    date = fields.Date(default=fields.Date.today(), help="Enter the date")
    due_date = fields.Date(default=fields.Date.add(fields.Date.today(), days=15))
    company_id = fields.Many2one(comodel_name="res.company", help="Add company name",
                                 default=lambda self: self.env.company.id)
    next_billing = fields.Date(default=fields.Date.add(fields.Date.today(), days=90))
    is_lead = fields.Boolean(default="True", help="Is it a lead")
    customer_id = fields.Many2one(comodel_name='res.partner', help="Enter customer")
    description = fields.Text(help="Add description")
    terms_and_conditions = fields.Html()
    billing_schedule = fields.Many2many(comodel_name='billing.schedule')
    product_id = fields.Many2one('product.template', help="Name the product")
    recurring_amount = fields.Float(help="The amount that must be paid")
    state = fields.Selection(selection=[('draft', 'Draft'),
                                        ('confirm', 'Confirm'),
                                        ('done', 'Done'),
                                        ('cancel', 'Cancel')], default="draft", tracking=True)
    recurring_credit_ids = fields.Many2many(comodel_name='recurring.credit')
    recurring_credit_a_ids = fields.Many2many(comodel_name='recurring.credit', compute='_compute_recurring_credit_ids')

    _sql_constraints = [
        ('establishment_id',
         'unique(establishment_id)',
         'Choose another value - it has to be unique!')
    ]

    # validate Establishment field
    @api.constrains('establishment_id')
    def _check_establishment_id(self):
        pattern = r'^(?=.*[a-zA-Z]{3})(?=.*[0-9]{3})(?=.*[\W_]{3}).{9,}$'
        if self.establishment_id == 0:
            raise ValidationError("Your establishment_id should contain 3alphabet,3numbers,3special characters: %s"
                                  % self.establishment_id)
        elif not re.match(pattern, self.establishment_id):
            raise ValidationError("Your establishment_id should contain 3alphabet,3numbers,3special characters: %s"
                                  % self.establishment_id)

    # """Sequence_id"""
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('order_id', _('New')) == _('New'):
                vals['order_id'] = self.env['ir.sequence'].next_by_code(
                    'recurring.subscription') or _('New')
        return super(RecurringSubscription, self).create(vals_list)

    @api.depends('recurring_credit_ids')
    def _compute_recurring_credit_ids(self):
        for rec in self:
            records_credit = self.env['recurring.credit'].search([('period_date',
                                                                   '<', rec.due_date)]).ids
            rec.recurring_credit_a_ids = [fields.Command.set(records_credit)]

    # add  button and changing 'state' while clicking it
    def button_confirm(self):
        self.write({
            'state': "confirm"
        })

    def button_cancel(self):
        self.write({
            'state': "cancel"
        })
