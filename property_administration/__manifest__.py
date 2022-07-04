# -*- coding: utf-8 -*-

{
    'name': 'Property Administration',
    'category': 'General',
    'summary': 'Property Administration',
    'description': 'Property Administration',
    'depends': [
        'property_management', 'account'
    ],
    'data': ['views/cost_type.xml',
             'views/tenancy.xml',
             'views/rent.xml',
             'views/expenditure.xml',
             'views/journal.xml',
             'views/managed_objects.xml',
             'views/account_view.xml',
             # 'views/product_view.xml',
             'views/property_view.xml',
             'views/res_users_view.xml',
             'views/portal_template.xml',
             'security/ir.model.access.csv',
             'wizard/split_cost.xml',
             'wizard/utility_bill.xml',
             'wizard/expenditure.xml',
             'wizard/landlord_certificate.xml',
             'data/rent_invoice.xml',
             'reports/landlord_certificate_report.xml',
             'reports/tenancy_contract_report.xml'
             ],
    'demo': ['demo/demo.xml'],
    'installable': True,
    'application': False,
}
