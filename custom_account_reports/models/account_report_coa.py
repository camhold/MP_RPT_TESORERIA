# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from copy import deepcopy

from odoo import models, api, _, fields
from odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT


class AccountChartOfAccountReport(models.AbstractModel):
    _name = "account.coa.report"
    _description = "Chart of Account Report"
    _inherit = "account.report"

    filter_date = {'mode': 'range', 'filter': 'this_month'}
    filter_comparison = {'date_from': '', 'date_to': '', 'filter': 'no_comparison', 'number_period': 1}
    filter_all_entries = False
    filter_journals = True
    filter_analytic = True
    filter_unfold_all = False
    filter_cash_basis = None
    filter_hierarchy = False
    MAX_LINES = None

    @api.model
    def _get_templates(self):
        templates = super(AccountChartOfAccountReport, self)._get_templates()
        templates['main_template'] = 'custom_account_reports.main_template_with_filter_input_accounts'
        return templates

    @api.model
    def _get_columns(self, options):
        # header1 = [
        #     {'name': '', 'style': 'width: 100%'},
        #     {'name': _('Initial Balance'), 'class': 'number', 'colspan': 2},
        # ] + [
        #     {'name': period['string'], 'class': 'number', 'colspan': 2}
        #     for period in reversed(options['comparison'].get('periods', []))
        # ] + [
        #     {'name': options['date']['string'], 'class': 'number', 'colspan': 2},
        #     {'name': _('End Balance'), 'class': 'number', 'colspan': 2},
        # ]
        header2 = [
            {'name': '', 'style': 'width:40%'},
            {'name': _('Débito'), 'class': 'number o_account_coa_column_contrast'},
            {'name': _('Crédito'), 'class': 'number o_account_coa_column_contrast'},
        ]
        # if options.get('comparison') and options['comparison'].get('periods'):
        #     header2 += [
        #         {'name': _('Debit'), 'class': 'number o_account_coa_column_contrast'},
        #         {'name': _('Credit'), 'class': 'number o_account_coa_column_contrast'},
        #     ] * len(options['comparison']['periods'])
        header2 += [
            {'name': _('Deudor'), 'class': 'number o_account_coa_column_contrast'},
            {'name': _('Acreedor'), 'class': 'number o_account_coa_column_contrast'},
            {'name': _('Activo'), 'class': 'number o_account_coa_column_contrast'},
            {'name': _('Pasivo'), 'class': 'number o_account_coa_column_contrast'},
            {'name': _('Pérdida'), 'class': 'number o_account_coa_column_contrast'},
            {'name': _('Ganancia'), 'class': 'number o_account_coa_column_contrast'},
        ]
        # return [header1, header2]
        return [header2]

    @api.model
    def _get_lines(self, options, line_id=None):
        # Create new options with 'unfold_all' to compute the initial balances.
        # Then, the '_do_query' will compute all sums/unaffected earnings/initial balances for all comparisons.
        display_account = options.get('account_filter', 'all')
        new_options = options.copy()
        new_options['unfold_all'] = True

        # adding an end balance column computed over the entire period
        end_balance_date_to = new_options['date']['date_to']
        end_balance_date_from = new_options['comparison']['periods'][-1]['date_from'] if new_options['comparison']['periods'] else new_options['date']['date_from']
        period_options = new_options.copy()
        period_options['date'] = {
            'mode': 'range',
            'date_to': fields.Date.from_string(end_balance_date_to).strftime(DEFAULT_SERVER_DATE_FORMAT),
            'date_from': fields.Date.from_string(end_balance_date_from).strftime(DEFAULT_SERVER_DATE_FORMAT)
        }
        options_list = [period_options] + self._get_options_periods_list(new_options)

        accounts_results, taxes_results = self.env['account.general.ledger']._do_query(options_list, fetch_lines=False)

        lines = []
        # totals = [0.0] * (2 * (len(options_list) + 1))
        totals = [0.0] * 8

        # Add lines, one per account.account record.
        for account, periods_results in accounts_results:
            sums = []
            currency = account.currency_id and account.currency_id or account.company_id.currency_id
            period_values = periods_results[-1]
            account_sum = period_values.get('sum', {})
            def get_account(account=account, account_sum=account_sum, sums=sums, lines=lines):
                # for i, period_values in enumerate(reversed(periods_results[:1])):
                
                debito = account_sum.get('debit', 0.0)
                credito = account_sum.get('credit', 0.0)
                deudor = account_sum.get('balance', 0.0) if account_sum.get('balance', 0.0) > 0 else 0
                acreedor = account_sum.get('balance', 0.0)*-1 if account_sum.get('balance', 0.0) < 0 else 0
                activo = account_sum.get('balance', 0.0) if account_sum.get('balance', 0.0) > 0 and account.user_type_id.include_initial_balance else 0
                pasivo = account_sum.get('balance', 0.0)*-1 if account_sum.get('balance', 0.0) < 0 and account.user_type_id.include_initial_balance else 0
                perdida = account_sum.get('balance', 0.0) if account_sum.get('balance', 0.0) > 0 and not account.user_type_id.include_initial_balance else 0
                ganancia = account_sum.get('balance', 0.0)*-1 if account_sum.get('balance', 0.0) < 0 and not account.user_type_id.include_initial_balance else 0
                sums += [
                    debito,
                    credito,
                    deudor,
                    acreedor,
                    activo,
                    pasivo,
                    perdida,
                    ganancia
                ]

                columns = []
                for i, value in enumerate(sums):
                    # Update totals.
                    totals[i] += value

                    # Create columns.
                    columns.append({'name': self.format_value(value, blank_if_zero=True), 'class': 'number', 'no_format_name': value})

                name = account.name_get()[0][1]

                lines.append({
                    'id': self._get_generic_line_id('account.account', account.id),
                    'name': name,
                    'code': account.code,
                    'title_hover': name,
                    'columns': columns,
                    'unfoldable': False,
                    'caret_options': 'account.account',
                    'class': 'o_account_searchable_line o_account_coa_column_contrast',
                })
            if display_account == 'all':
                get_account(account, account_sum, sums, lines)
            if display_account == 'not_zero' and not currency.is_zero(account_sum.get('balance', 0.0)):
                get_account(account, account_sum, sums, lines)
            if display_account == 'movement' and (not currency.is_zero(account_sum.get('debit', 0.0)) or not currency.is_zero(account_sum.get('credit', 0.0))):
                get_account(account, account_sum, sums, lines)
        totals1 = [0] * 8
        totals2 = [0] * 8
        a = totals[4] - totals[5]
        b = totals[6] - totals[7]
        if a < 0:
            totals1[4] = a*-1
        else:
            totals1[5] = a
        
        if b < 0:
            totals1[6] = b*-1
        else:
            totals1[7] = b
        
        totals2 = [totals[0], totals[1], totals[2], totals[3], totals[4] + totals1[4], totals[5] + totals1[5], totals[6] + totals1[6], totals[7] + totals1[7]]
            
        # Total report line.
        lines.append({
             'id': self._get_generic_line_id(None, None, markup='grouped_accounts_total'),
             'name': _('Total Acumulado'),
             'class': 'total o_account_coa_column_contrast',
             'columns': [{'name': self.format_value(total), 'class': 'number'} for total in totals],
             'level': 1,
        })
        lines.append({
             'id': self._get_generic_line_id(None, None, markup='grouped_accounts_total'),
             'name': _('Resultado del Ejercicio'),
             'class': 'total o_account_coa_column_contrast',
             'columns': [{'name': self.format_value(total), 'class': 'number'} for total in totals1],
             'level': 1,
        })
        lines.append({
             'id': self._get_generic_line_id(None, None, markup='grouped_accounts_total'),
             'name': _('Sumas iguales'),
             'class': 'total o_account_coa_column_contrast',
             'columns': [{'name': self.format_value(total), 'class': 'number'} for total in totals2],
             'level': 1,
        })

        return lines

    @api.model
    def _get_report_name(self):
        return _("Reporte de 8 columnas")
