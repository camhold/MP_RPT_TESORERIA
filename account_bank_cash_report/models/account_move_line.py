from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    user_type_id = fields.Many2one(related="account_id.user_type_id")
    is_bank_cash = fields.Boolean(related="account_id.is_bank_cash", store=True)
