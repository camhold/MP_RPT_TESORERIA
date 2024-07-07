from odoo import models, fields, _
from datetime import datetime


class AccountJournalEntriesDateWizard(models.TransientModel):
    _name = 'account.journal.entries.wizard'
    _description = 'Asistente para selección de fechas para apuntes de diario'

    initial_date = fields.Date(string="Fecha Inicio", default=datetime.today())
    final_date = fields.Date(string="Fecha Fin", default=datetime.today())

    def action_confirm(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Libro de diario'),
            'res_model': 'account.move.line',
            'view_mode': 'tree',
            'view_id': self.env.ref('account_journal_entries_report.view_account_journal_entries_tree').id,
            'target': 'main',
            'context': {'search_default_move_name': 1,
                        'group_by': 'date',
                        'expand': 1,
                        'initial_date': self.initial_date,
                        'final_date': self.final_date}
        }
