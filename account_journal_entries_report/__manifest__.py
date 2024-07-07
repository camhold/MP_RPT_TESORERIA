{
    'name': 'Journal Entries Report',
    'version': '15.0.0.0.0',
    'summary': """ Report about the journal entries module """,
    'author': 'Baruc Álvarez',
    'category': 'Accounting/Accounting',
    'depends': ['account'],
    "data": [
        "security/ir.model.access.csv",
        "wizard/account_journal_entries_date_wizard.xml",
        "views/account_journal_entries_report.xml",
        "views/account_journal_entries_menuitem.xml",
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}


