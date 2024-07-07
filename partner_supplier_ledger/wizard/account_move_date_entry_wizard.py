from odoo import models, fields, _
from datetime import datetime


class AccountMove(models.TransientModel):
    _name = 'account.move.dates.wizard.supplier'
    _description = 'Asistente de selección de fechas contables'

    initial_date = fields.Date(string='Fecha Inicial', default=datetime.today())
    final_date = fields.Date(string='Fecha Termino', default=datetime.today())

    def action_confirm(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Libro de compras'),
            'res_model': 'account.move.supplier.ledger',
            'view_mode': 'tree',
            'target': 'main',
            'context': {'search_default_l10n_latam_document_type_id': 1,
                        'group_by': 'date',
                        'initial_date': self.initial_date,
                        'final_date': self.final_date}
        }
