from odoo import api, fields, models, re
from odoo.exceptions import ValidationError


class PartnerAccountId(models.Model):
    _name = 'partner.account.id'
    _description = 'Partner Account Id'
    _rec_name = 'account_id'

    account_id = fields.Char(help='Add the account details')
    _sql_constraints = [
        ('account_id',
         'unique(account_id)',
         'Choose another value - it has to be unique!')
    ]

    @api.constrains('account_id')
    def _check_account_id(self):
        pattern = r'^(?=.*[a-zA-Z]{3})(?=.*[0-9]{3})(?=.*[\W_]{3}).{9,}$'
        if self.account_id == 0:
            raise ValidationError('your account is empty')
        elif not re.match(pattern, self.account_id):
            raise ValidationError('Account must contain 3character,3number and 3 special character')
