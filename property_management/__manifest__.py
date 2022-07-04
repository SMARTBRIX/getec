# -*- coding: utf-8 -*-

{
    'name': 'Property Management',
    'category': 'General',
    'summary': 'Property Management',
    'description': 'Property Management',
    'depends': [
        'crm',
        'website',
        'base_geolocalize'
    ],
    'data': [
        'data/data.xml',
        # 'views/assets.xml',
        'views/property_view.xml',
        'views/res_partner_view.xml',
        'views/crm_view.xml',
        'views/misc.xml',
        'views/property_search_profile_view.xml',
        'views/mail_view.xml',
        'security/ir.model.access.csv',
        'data/cron.xml',
        'data/mail.xml',
        'data/sequence.xml',
        'data/crm_stage_data.xml',
        'data/property_contact_fields.xml',
        'views/portal_templates.xml',
        'views/res_company_views.xml',
        'views/res_config_settings_views.xml',
        'views/attachment_view.xml',
        'wizard/import_lead_wizard_view.xml',
        'report/property_management_report.xml',
        'report/expose_overview_report.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'property_management/static/src/scss/form_view.scss',
            'property_management/static/src/js/fields_widget.js',
            # 'theme_realestate/static/lib/leaflet/leaflet.css',
            # 'theme_realestate/static/lib/leaflet/leaflet.js'
        ],
        'web.report_assets_common': [
            'property_management/static/src/scss/property_booking_report.scss'],
        'web.assets_frontend': [
            'property_management/static/src/scss/portal.scss',
            'property_management/static/src/js/portal.js'],
        'web.assets_qweb': [
            'property_management/static/src/xml/*.xml',
        ],
    },
}