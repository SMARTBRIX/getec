# -*- coding: utf-8 -*-

{
    'name': 'Property Documents',
    'category': 'General',
    'summary': 'Property Documents',
    'description': 'Property Documents',
    'depends': [
        'documents',
        'property_management',
    ],
    'data': [
        'views/property_document.xml',
        'views/property_view.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'property_documents/static/src/js/documents_view_mixin.js',
            'property_documents/static/src/js/documents_inspector.js',
        ],
    }
}