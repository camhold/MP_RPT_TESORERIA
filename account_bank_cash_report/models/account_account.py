from odoo import models, fields, api


class AccountAccount(models.Model):
    _inherit = "account.account"

    is_bank_cash = fields.Boolean(string="Es banco y efectivo?")
