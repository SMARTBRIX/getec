# -*- coding: utf-8 -*-

from odoo import _, http
from odoo.addons.website.controllers.main import QueryURL
from odoo.http import request
from odoo.osv.expression import AND, OR


class RealEstate(http.Controller):

    _properties_per_page = 12
    _properties_sort_by = [
        (_('Published: Recent to Old'), 'published_date desc, create_date desc'),
        (_('Published: Old to Recent'), 'published_date asc, create_date asc'),
        (_('Name: A to Z'), 'external_headline asc, name asc'),
        (_('Name: Z to A'), 'external_headline desc, name desc'),
        (_('Price: High to Low'), 'purchase_price desc'),
        (_('Price: Low to High'), 'purchase_price asc'),
    ]

    def _get_search_domain(self):
        args = request.httprequest.args
        domains = ['&', ('website_published', '=', True), ('active', '=', True)]

        # Reference
        reference = args.get('reference')
        if reference:
            reference = reference.split(' ')

            if len(reference) > 1:
                custom_domain = []
                for ref in reference:
                    custom_domain += [('external_headline', 'ilike', ref)]
                domains = AND([domains, custom_domain])
            else:
                domains = AND([domains, ['|', ('external_headline', 'ilike', reference[0]), ('reference_id', '=', reference[0])]])

        # Sell Type
        sell_type = args.get('sell_type')
        if sell_type:
            # domains = AND(
            #     [domains, [('for_sale' if sell_type == 'buy' else 'for_rent', '=', True)]])

            if sell_type == 'buy':
                domains = AND(
                    [domains, [('for_sale', '=', True)]])
            elif sell_type == 'rent':
                domains = AND(
                    [domains, [('for_rent', '=', True)]])
            else:
                domains = AND(
                    [domains, [('for_lease', '=', True)]])
        # Property Type
        property_type = args.get('property_type')
        if property_type:
            domains = AND([domains, [('property_type_id', 'in', [int(i)
                                                                 for i in property_type.split(',')])]])

        # Location
        sublocation_id = args.get('property_sublocation')
        if sublocation_id:
            domains = AND([domains, [('sub_location_id', 'in', [int(i)
                                                                for i in sublocation_id.split(',')])]])

        # Price
        from_price = args.get('from_price')
        if from_price:
            domains = AND([domains, ['|', '&', ('for_sale', '=', True), ('purchase_price', '>=', int(
                from_price)), '&', ('for_rent', '=', True), ('rent_incl_heat', '>=', int(from_price))]])
        to_price = args.get('to_price')
        if to_price:
            domains = AND([domains, ['|', '&', ('for_sale', '=', True), ('purchase_price', '<=', int(
                to_price)), '&', ('for_rent', '=', True), ('rent_incl_heat', '<=', int(to_price))]])

        # Bedrooms
        bedrooms = args.get('bedrooms')
        if bedrooms:
            if bedrooms < '5':
                domains = AND([domains, [('bed_rooms', '=', int(bedrooms))]])
            else:
                domains = AND([domains, [('bed_rooms', '>=', int(bedrooms))]])

        # Bathrooms
        bathrooms = args.get('bathrooms')
        if bathrooms:
            if bathrooms < '5':
                domains = AND([domains, [('bath_rooms', '=', int(bathrooms))]])
            else:
                domains = AND(
                    [domains, [('bath_rooms', '>=', int(bathrooms))]])

        # Parkings
        parkings = args.get('parkings')
        if parkings:
            if parkings < '5':
                domains = AND(
                    [domains, [('no_of_parking', '=', int(parkings))]])
            else:
                domains = AND(
                    [domains, [('no_of_parking', '>=', int(parkings))]])

        # Garages
        garages = args.get('garages')
        if garages:
            if garages < '5':
                domains = AND(
                    [domains, [('no_of_garages', '=', int(garages))]])
            else:
                domains = AND(
                    [domains, [('no_of_garages', '>=', int(garages))]])

        # Living Space
        if args.get('property_living_space_from_value'):
            domains = AND([domains, [('living_space', '>=', int(
                args['property_living_space_from_value']))]])
        if args.get('property_living_space_to_value'):
            domains = AND(
                [domains, [('living_space', '<=', int(args['property_living_space_to_value']))]])

        # Plot Area
        if args.get('property_plot_area_from_value'):
            domains = AND(
                [domains, [('plot_area', '>=', int(args['property_plot_area_from_value']))]])
        if args.get('property_plot_area_to_value'):
            domains = AND(
                [domains, [('plot_area', '<=', int(args['property_plot_area_to_value']))]])

        return domains

    def _get_searchbar_data(self, **kwargs):
        PropertyProperty = request.env['property.property']
        PropertyType = request.env['property.type']
        PropertySubLocation = request.env['property.sub.location']
        data = {
            'currency_symbol': request.website.company_id.currency_id.symbol,
            'property_types': PropertyType.search([]),
        }

        # Sell Type
        sell_type = kwargs.get('sell_type')
        if sell_type:
            if sell_type == 'buy':
                data['selected_sell_type_str'] = _('Buy')
            elif sell_type == 'rent':
                data['selected_sell_type_str'] = _('Rent')
            else:
                data['selected_sell_type_str'] = _('Lease')
            # data['selected_sell_type_str'] = sell_type == 'buy' and _(
            #     'Buy') or _('Rent')
        # Property Type
        property_types = kwargs.get('property_type')
        if property_types:
            property_types_ids = PropertyType.browse(
                [int(i) for i in property_types.split(',')])
            data['selected_property_type_str'] = ', '.join(
                property_types_ids.mapped('name')[:2])
            data['selected_property_type_ids'] = [
                int(i) for i in property_types.split(',')]

        # Sublocations
        sublocation = kwargs.get('property_sublocation')
        if sublocation:
            sublocation_ids = PropertySubLocation.browse(
                [int(i) for i in sublocation.split(',')])
            data['selected_property_sublocation_str'] = ', '.join(
                sublocation_ids.mapped('name')[:2])
            data['selected_property_sublocation_ids'] = [
                int(i) for i in sublocation.split(',')]

        grouped_locations = PropertySubLocation.read_group(
            [], ['parent_location_id'], ['parent_location_id'])
        data['property_locations'] = {location['parent_location_id']: PropertySubLocation.search(
            location['__domain']) for location in grouped_locations}

        # Prices
        buy_prices = PropertyProperty.read_group([('for_sale', '=', True)], [
                                                 'buy_min_price:min(purchase_price)', 'buy_max_price:max(purchase_price)'], [])[0]
        buy_min_price = float(buy_prices['buy_min_price'] or 0)
        buy_max_price = float(buy_prices['buy_max_price'] or 0)

        rend_prices = PropertyProperty.read_group([('for_rent', '=', True)], [
                                                  'rent_min_price:min(rent_incl_heat)', 'rent_max_price:max(rent_incl_heat)'], [])[0]
        rent_min_price = float(rend_prices['rent_min_price'] or 0)
        rent_max_price = float(rend_prices['rent_max_price'] or 0)

        data['property_min_price'] = min(buy_min_price, rent_min_price)
        data['property_max_price'] = max(buy_max_price, rent_max_price)

        # Living Space
        living_space_values = PropertyProperty.read_group(
            [], ['property_living_space_min_value:min(living_space)', 'property_living_space_max_value:max(living_space)'], [])[0]
        data['property_living_space_min_value'] = float(
            living_space_values['property_living_space_min_value'] or 0)
        data['property_living_space_max_value'] = float(
            living_space_values['property_living_space_max_value'] or 0)

        # Plot Area
        plot_area_values = PropertyProperty.read_group(
            [], ['property_plot_area_min_value:min(plot_area)', 'property_plot_area_max_value:max(plot_area)'], [])[0]
        data['property_plot_area_min_value'] = float(
            plot_area_values['property_plot_area_min_value'] or 0)
        data['property_plot_area_max_value'] = float(
            plot_area_values['property_plot_area_max_value'] or 0)

        return data

    @http.route([
        '/real_estate/properties',
        '/real_estate/properties/page/<int:page>',
    ], type='http', auth='public', website=True)
    def properties(self, page=1, **kwargs):
        PropertyProperty = request.env['property.property']
        domain = self._get_search_domain()
        properties_count = PropertyProperty.search_count(domain)
        pager = request.website.pager(url='/real_estate/properties', total=properties_count,
                                      page=page, step=self._properties_per_page, url_args=kwargs)
        properties = PropertyProperty.search(domain, limit=self._properties_per_page, offset=pager['offset'], order=kwargs.get(
            'order') or 'published_date desc, create_date desc')

        data = {
            'properties': properties,
            'properties_count': properties_count,
            'properties_sort_by': self._properties_sort_by,
            'pager': pager,
            'keep': QueryURL('/real_estate/properties', order=kwargs.get('order')),
        }
        data.update(self._get_searchbar_data(**kwargs))

        return request.render('theme_realestate.properties', data)

    @http.route('/real_estate/property/<model("property.property"):property_id>', type='http', auth='public', website=True)
    def property_detail(self, property_id, **kwargs):
        data = {
            'property': property_id,
            'countries': request.env['res.country'].sudo().search([]),
            'main_object': property_id,
        }
        return request.render('theme_realestate.property', data)

    @http.route('/real_estate/get_search_snippet_data', type='json', auth='public', website=True)
    def get_search_snippet_data(self, **post):
        PropertyProperty = request.env['property.property']

        data = {
            'property_types': request.env['property.type'].search_read([]),
            'property_locations': request.env['property.location'].search_read([]),
            'currency_symbol': request.website.company_id.currency_id.symbol,
        }

        buy_prices = PropertyProperty.read_group([('for_sale', '=', True)], [
                                                 'buy_min_price:min(purchase_price)', 'buy_max_price:max(purchase_price)'], [])[0]
        buy_min_price = float(buy_prices['buy_min_price'] or 0)
        buy_max_price = float(buy_prices['buy_max_price'] or 0)

        rent_prices = PropertyProperty.read_group([('for_rent', '=', True)], [
                                                  'rent_min_price:min(rent_incl_heat)', 'rent_max_price:max(rent_incl_heat)'], [])[0]
        rent_min_price = float(rent_prices['rent_min_price'] or 0)
        rent_max_price = float(rent_prices['rent_max_price'] or 0)

        data['property_min_price'] = min(buy_min_price, rent_min_price)
        data['property_max_price'] = max(buy_max_price, rent_max_price)

        return data

    @http.route('/real_estate/get_search_2_snippet_data', type='json', auth='public', website=True)
    def get_search_2_snippet_data(self, **kwargs):
        return request.website.viewref('theme_realestate.property_searchbar')._render(self._get_searchbar_data(**kwargs))

    @http.route('/real_estate/get_categories_snippet_data', type='json', auth='public', website=True)
    def get_categories_snippet_data(self, **kwargs):
        PropertyProperty = request.env['property.property']
        grouped_categories = PropertyProperty.read_group(
            [('website_published', '=', True), ('show_on_website', '=', True)], [], ['property_type_id'])
        categories = []
        for category in grouped_categories:
            if category['property_type_id']:
                categories.append({'id': category['property_type_id'][0], 'name': category['property_type_id']
                                   [1], 'properties': PropertyProperty.sudo().search(category['__domain'])})
        return request.website.viewref('theme_realestate.s_real_estate_categories_template')._render({'categories': categories})

    @http.route('/real_estate/get_cover_snippet_data', type='json', auth='public', website=True)
    def get_cover_snippet_data(self, **kwargs):
        properties = request.env['property.property'].search(
            [('website_published', '=', True), ('show_on_cover', '=', True)])
        return request.website.viewref('theme_realestate.s_real_estate_cover_template')._render({'properties': properties})

    @http.route('/real_estate/add_to_favorite/<model(property.property):property_id>', type='json', auth='user', website=True)
    def add_to_favorite(self, property_id, **kwargs):
        return request.env['crm.lead'].sudo().create({
            'name': property_id.name,
            'type': 'opportunity',
            'partner_id': request.env.user.partner_id.id,
            'property_id': property_id.id,
            'user_id': property_id.sales_person_id.id,
            'team_id': request.website.dr_property_sales_team.id,
            'stage_id': request.website.dr_property_crm_stage.id,
        })

    @http.route(['/real_estate/country_infos/<model("res.country"):country>'], type='json', auth="public", methods=['POST'], website=True)
    def country_infos(self, country, **kw):
        return dict(
            states=[(st.id, st.name, st.code) for st in country.state_ids],
        )
