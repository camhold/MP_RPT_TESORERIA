# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Reporte de 8 columnas',
    'summary': 'View and create reports',
    'category': '',
    'description': """
Reporte de  8 columnas
    """,
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/report_export_wizard.xml',
        'data/account_financial_report_data.xml',
        'views/report_financial.xml',
        'views/search_template_view.xml',

    ],
    'auto_install': True,
    'installable': True,
    'license': 'OEEL-1',
    'assets': {
        'custom_account_reports.assets_financial_report': [
            ('include', 'web._assets_helpers'),
            'web/static/lib/bootstrap/scss/_variables.scss',
            ('include', 'web._assets_bootstrap'),
            'web/static/fonts/fonts.scss',
            'custom_account_reports/static/src/scss/account_financial_report.scss',
            'custom_account_reports/static/src/scss/account_report_print.scss',
        ],
        'web.assets_backend': [
            'custom_account_reports/static/src/js/mail_activity.js',
            'custom_account_reports/static/src/js/account_reports.js',
            'custom_account_reports/static/src/js/action_manager_account_report_dl.js',
            'custom_account_reports/static/src/scss/account_financial_report.scss',
        ],
        'web.qunit_suite_tests': [
            'custom_account_reports/static/tests/action_manager_account_report_dl_tests.js',
            'custom_account_reports/static/tests/account_reports_tests.js',
        ],
        'web.assets_tests': [
            'custom_account_reports/static/tests/tours/**/*',
        ],
        'web.assets_qweb': [
            'custom_account_reports/static/src/xml/**/*',
        ],
    }
}
