# -*- coding: utf-8 -*-

{
    'name': 'Realestate Theme',
    'description': 'Ecommerce Theme',
    'summary': 'Theme for Realestate',
    'category': 'Theme/eCommerce',
    'version': '15.0.0.0.1',
    'author': 'OBS',
    'depends': ['website_crm', 'property_management'],
    'data': [
        'data/data.xml',
        'data/website_form_data.xml',
        # 'views/assets.xml',
        'views/layout.xml',
        'views/snippets.xml',
        'views/images.xml',
        'views/customize_modal.xml',
        'views/components.xml',
        'views/headers/header_style_1.xml',
        'views/portal_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'theme_realestate/static/lib/OwlCarousel2-2.3.4/dist/assets/owl.carousel.css',
            'theme_realestate/static/lib/OwlCarousel2-2.3.4/dist/assets/owl.theme.default.css',
            'theme_realestate/static/lib/PhotoSwipe-4.1.3/dist/photoswipe.css',
            'theme_realestate/static/lib/leaflet/leaflet.css',
            'theme_realestate/static/src/scss/theme.scss',
            'theme_realestate/static/src/scss/theme_realestate.scss',
            'theme_realestate/static/src/scss/options/headers/header_style_1.scss',
            ('replace', 'web_editor/static/src/scss/web_editor.frontend.scss', 'theme_realestate/static/src/scss/web_editor.frontend.scss'),

            # 'theme_realestate/static/src/scss/primary_variables.scss',

            'theme_realestate/static/lib/OwlCarousel2-2.3.4/dist/owl.carousel.js',
            'theme_realestate/static/lib/ion.rangeSlider-2.3.0/js/ion.rangeSlider.js',
            'theme_realestate/static/lib/PhotoSwipe-4.1.3/dist/photoswipe.js',
            'theme_realestate/static/lib/PhotoSwipe-4.1.3/dist/photoswipe-ui-default.js',
            'theme_realestate/static/lib/leaflet/leaflet.js',
            'theme_realestate/static/src/js/theme_realestate_frontend.js',
            'theme_realestate/static/src/js/property_contact_form.js',
        ],

        'web._assets_primary_variables': [
            # 'theme_realestate/static/src/scss/primary_variables.scss',
            'theme_realestate/static/src/scss/mixins.scss',
        ],
        'web._assets_frontend_helpers': [
            'theme_realestate/static/src/scss/bootstrap_overridden.scss',
        ],
    }
}
