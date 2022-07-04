# -*- coding: utf-8 -*-

{
    'name': 'Property Project Enterprise',
    'description': 'Property Project Enterprise',
    'category': 'General',
    'summary': 'Property Project Enterprise',
    'depends': [
        'account_budget'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/property_budgetary_category.xml',
        'views/account_budget_post_view.xml',
        'views/account_move_view.xml',
        'views/account_crossovered_budget.xml',
        'views/project_view.xml'
    ],
    'demo': [],
    'installable': True,
    'application': False,
}
