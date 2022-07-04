# -*- coding: utf-8 -*-

{
    'name': 'Property Reports',
    'description': 'Property Reports',
    'category': 'General',
    'summary': 'Property Reports',
    'depends': [
        'property_management', 'property_administration', 'property_project_enterprise'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/portfolio_report_view.xml',
        'views/portfolio_report_graph_view.xml',
        'wizard/portfolio_report_wizard.xml',
        'wizard/portfolio_report_graph_wizard.xml'
    ],
    'demo': [],
    'installable': True,
    'application': False,
}
