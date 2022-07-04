# -*- coding: utf-8 -*-

import base64
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.addons.http_routing.models.ir_http import slug
from odoo.tools.mimetypes import guess_mimetype


class PropertyCategory(models.Model):
    _name = 'property.category'
    _description = 'Property Category'

    name = fields.Char(translate=True)
    is_commercial = fields.Boolean('Commercial ?')


class PropertyType(models.Model):
    _name = 'property.type'
    _description = 'Property Type'

    name = fields.Char(translate=True)
    # type = fields.Selection(
    #     [('private', 'Private'), ('commercial', 'Commercial')])
    category_id = fields.Many2one('property.category', 'Category') 


class LeadOrigin(models.Model):
    _name = 'lead.origin'
    _description = 'Lead Origin'

    name = fields.Char(translate=True)


class SaleReason(models.Model):
    _name = 'sale.reason'
    _description = 'Sale Reason'

    name = fields.Char(translate=True)


class PropertyLocation(models.Model):
    _name = 'property.location'
    _description = 'Property Location'

    name = fields.Char(string='Location', translate=True)
    child_location_ids = fields.One2many(
        'property.sub.location', 'parent_location_id')


class PropertySubLocation(models.Model):
    _name = 'property.sub.location'
    _description = 'Property Location'

    name = fields.Char(string='Sub Location', translate=True)
    parent_location_id = fields.Many2one(
        'property.location', string='Main Location')


class Features(models.Model):
    _name = 'features.features'
    _description = 'Features'

    name = fields.Char(translate=True)
    feature_value_ids = fields.One2many('features.values', 'feature_id')


class FeaturesValues(models.Model):
    _name = 'features.values'
    _description = 'Features Values'

    name = fields.Char(string='Value', translate=True)
    feature_id = fields.Many2one('features.features')


class PropertyFeatures(models.Model):
    _name = 'property.features'
    _description = 'Property Features'
    _rec_name = 'feature_id'

    feature_id = fields.Many2one('features.features')
    value_ids = fields.Many2many('features.values')
    property_id = fields.Many2one('property.property')


class PropertyContractType(models.Model):
    _name = 'property.contract.type'
    _description = 'Property Contract Type'

    name = fields.Char(translate=True)
    terms_ids = fields.Many2many('property.terms', string='Terms')


class PropertyTerms(models.Model):
    _name = 'property.terms'
    _description = 'Property Terms'

    name = fields.Char(required=True, translate=True)
    description = fields.Html(translate=True)
    is_required = fields.Boolean(string='Is Mandatory?')


class PropertyStage(models.Model):
    _name = 'property.stage'
    _description = 'Property Stages'

    name = fields.Char(required=True, translate=True)


class Property(models.Model):
    _name = 'property.property'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin',
                'utm.mixin', 'website.seo.metadata', 'website.published.multi.mixin']
    _description = 'Property'
    _rec_name = 'complete_name'

    name = fields.Char('Name')
    complete_name = fields.Char(
        'Name', compute='_compute_complete_name', store=True)
    reference_id = fields.Char('Reference ID', copy=False)
    external_headline_d = fields.Char(
        related='external_headline', string='External Headline', translate=True)
    property_type_id_d = fields.Many2one(
        related='property_type_id', string='Property Type')
    for_sale_d = fields.Boolean(related='for_sale')
    for_rent_d = fields.Boolean(related='for_rent')
    street_d = fields.Char(related='street', string='Street')
    zip_d = fields.Char(related='zip', string='Zip')
    city_d = fields.Char(related='city', string='City')
    country_id_d = fields.Many2one(related='country_id', string='Country')
    living_space_d = fields.Float(related='living_space', string='Living Space')
    plot_area_d = fields.Integer(related='plot_area', string='Plot Area')
    rooms_d = fields.Integer(related='rooms', string='Rooms')
    bed_rooms_d = fields.Integer(related='bed_rooms', string='Bed Rooms')
    bath_rooms_d = fields.Integer(related='bath_rooms', string='Bath Rooms')
    sales_person_id_d = fields.Many2one(
        related='sales_person_id', string='Sales Person')
    owner_id_d = fields.Many2one(related='owner_id', string='Owner')
    available_from_d = fields.Date(
        related='available_from', string='Available From')
    purchase_price_d = fields.Float(
        related='purchase_price', string='Purchase Price')
    rent_price_d = fields.Float(related='rent_price', string='Rent')
    rent_incl_heat_d = fields.Float(
        related='rent_incl_heat', string='Rent Including Heating')
    internal_label = fields.Char('Internal Label')
    external_headline = fields.Char('External Headline', translate=True)
    property_stage_ids = fields.Many2many(
        'property.stage', string='Property Status')
    child_property_ids = fields.One2many(
        'property.property', 'parent_property_id')
    parent_property_id = fields.Many2one(
        'property.property', 'Parent Property')
    parent_id = fields.Many2one('property.property', related='parent_property_id', store=True)
    property_type_id = fields.Many2one('property.type', 'Property Type')
    # property_type = fields.Selection(
    #     [('private', 'Private'), ('commercial', 'Commercial')], related='property_type_id.type')
    property_type = fields.Many2one('property.category', related='property_type_id.category_id', string='Property Category', store=True)
    is_commercial = fields.Boolean(related='property_type.is_commercial')
    for_sale = fields.Boolean('For Sale?')
    for_rent = fields.Boolean('For Rent?')
    for_lease = fields.Boolean('For Lease?')
    #type = fields.Selection([('g', 'Geschaftlich'), ('p', 'Privat'), ('s', 'Sonstiges')], string='Type')
    contract_type_id = fields.Many2one('property.contract.type', string='Type')
    street = fields.Char('Street')
    zip = fields.Char('Zip')
    city = fields.Char('City')
    country_id = fields.Many2one('res.country', 'Country')
    location_id = fields.Many2one('property.location', 'Location')
    sub_location_id = fields.Many2one('property.sub.location', 'Sub Location')
    living_space = fields.Float('Living Space')
    heating_space = fields.Float('Heating Space')
    ancillary_costs = fields.Float('Ancillary Costs')
    plot_area = fields.Integer('Plot Area')
    rooms = fields.Integer('Rooms')
    bed_rooms = fields.Integer('Bed Rooms')
    bath_rooms = fields.Integer('Bath Rooms')
    longitude = fields.Float('Longitude')
    latitude = fields.Float('Latitude')
    construction_year = fields.Date('Construction Year')
    sales_person_id = fields.Many2one('res.users', 'Sales Person')
    owner_id = fields.Many2one('res.partner', 'Owner')
    lead_origin_id = fields.Many2one('lead.origin')
    asking_price = fields.Float('Asking Price', digits='Property Sale Price')
    purchase_price = fields.Float('Purchase Price', digits='Property Sale Price')
    rent_price = fields.Float('Rent', digits='Property Rent Price')
    lease_amount = fields.Float('Lease Amount', digits='Property Lease Price')
    is_lease_including_vat = fields.Boolean("Lease including VAT?")
    rent_incl_heat = fields.Float('Rent Including Heating', digits='Property Rent Price')
    reason_sale_id = fields.Many2one('sale.reason', string='Reason for Sale')
    # fields.Selection([('i', 'Invest-Geschaft'),
    #                                ('u', 'Umzug'),
    #                                ('h', 'Hinterlassenschaft'),
    #                                ('t', 'Trennung'),
    #                                ('m', 'Monetare Grunde'),
    #                                ('s', 'Sonstiges')], string='Reason for sale')
    available_from = fields.Date('Available From')
    purchase_date = fields.Date('Purchase Date')
    contract_begin = fields.Date('Begin of Contract')
    contract_end = fields.Date('End of Contract')
    provision_client = fields.Float('Commission Customer')
    commission_client = fields.Float('Commission Client')
    comm_incl_vat = fields.Boolean('Commission Including VAT?')
    contract_document = fields.Binary('Contract Documents')
    prob_complete = fields.Selection([('0', 'Normal'), ('1', 'Low'), ('2', 'High'), ('3', 'Very High')], string="Probability of Complition")
    furnish_quality = fields.Selection([('0', 'Normal'), ('1', 'Low'), ('2', 'High'), ('3', 'Very High')], string="Furnised Quality")
    guest_toilet = fields.Boolean(string='Guest Toilet?')
    equipped_kitchen = fields.Boolean('Equipped Kitchen?')
    balcony = fields.Boolean('Balcony?')
    terrace = fields.Boolean('Terrace?')
    no_of_parking = fields.Integer('Number of Parking Spaces')
    no_of_garages = fields.Integer('Number of Gareges')
    certificate = fields.Selection([('ni', 'Nicht benotigt'), ('vo', 'Vorhanden'), ('no', 'Noch nicht vorhanden')], string="Certificate")
    certificate_type = fields.Selection([('v', 'Vebrauchsausweis'), ('b', 'Bedarfsausweis')], string="Certificte Type")
    eec = fields.Selection([('A+', 'A+'), ('A', 'A'), ('B', 'B'), ('C', 'C'),
                            ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G'), ('H', 'H')], string='EEC')
    energy_characteristic = fields.Float('Energy Characteristic')
    energy_source = fields.Char('Energy Source')
    incl_warm_water = fields.Boolean('Including Warm Water')
    created_on = fields.Date('Created On')
    valid_till = fields.Date('Valid Till')
    property_info = fields.Text('Property', translate=True)
    location_info = fields.Html('Location', translate=True)
    freitext = fields.Html('Frietext', translate=True)
    furnishing_info = fields.Html('Furnishing', translate=True)
    construction_year = fields.Char('Construction Year')
    # Photos/Documents
    cover_photo = fields.Binary('Cover Photo')
    public_photos_ids = fields.Many2many('ir.attachment', 'public_photos_ir_attachments_rel', 'property_id', 'attachment_id', string='Public Photos')
    internal_photos_ids = fields.Many2many('ir.attachment', 'internal_photos_ir_attachments_rel', 'property_id', 'attachment_id', string='Internal Photos')
    protected_photos_ids = fields.Many2many('ir.attachment', 'protected_photos_ir_attachments_rel', 'property_id', 'attachment_id', string='Protected Photos')
    internal_documents_ids = fields.Many2many('ir.attachment', 'internal_documents_ir_attachments_rel', 'property_id', 'attachment_id', string='Internal Documents')
    protected_documents_ids = fields.Many2many('ir.attachment', 'protected_documents_ir_attachments_rel', 'property_id', 'attachment_id', string='Protected Documents')
    #customer_ids = fields.Many2many('res.partner', 'rel_customer_property', 'property_id', 'customer_id')
    opportunity_ids = fields.One2many('crm.lead', 'property_id', string="Opportunities")
    property_features_ids = fields.One2many('property.features', 'property_id', 'Property Features')
    show_on_website = fields.Boolean(string='Show on Start Page?')
    show_on_cover = fields.Boolean(string='Show on Cover ?')
    published_date = fields.Datetime(string='Published Date')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    opportunity_count = fields.Integer(compute='compute_opportunity_cnt')
    property_search_profile_count = fields.Integer(compute='compute_search_profile_count')
    active = fields.Boolean('Active', default=True)
    child_prop_count = fields.Integer(compute='compute_child_prop_cnt')
    administration_stage = fields.Boolean(compute="compute_administration_stage")
    # purchase_price_on_demand = fields.Boolean("Purchase Price On Demand")
    # purchase_price_desc = fields.Char("Purchase Price Description", translate=True)

    def action_view_public_photos(self):
        self.env.cr.execute("SELECT attachment_id from public_photos_ir_attachments_rel where property_id = %s" % (self.id))
        result = self.env.cr.dictfetchall()

        ir_attachment_id = self.env.ref(
            'property_management.ir_attachment_real_estate_list_view',
            raise_if_not_found=True).id

        ir_attachment_kanban_id = self.env.ref(
            'property_management.ir_attachment_real_estate_kanban_view',
            raise_if_not_found=True).id

        attachments = [attach['attachment_id'] for attach in result]
        return {
            'name': ('Public Photos'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,kanban',
            'views': [(ir_attachment_id, 'tree'), (ir_attachment_kanban_id, 'kanban')],
            # 'view_id': ir_attachment_id,
            'domain': [('id', 'in', attachments)],
            'res_model': 'ir.attachment'
        }

    @api.depends('property_stage_ids')
    def compute_administration_stage(self):
        self.administration_stage = False
        if self.property_stage_ids:
            self.administration_stage = any(self.property_stage_ids.mapped('administration_stage'))

    # def action_redirect_administration(self):
    #     form_view_ref = self.env.ref(
    #         'property_administration.property_form_administration', False)
    #     return {
    #         'name': ('Managed Objects'),
    #         'type': 'ir.actions.act_window',
    #         'view_mode': 'form',
    #         'res_id': self.id,
    #         'views': [(form_view_ref.id, 'form')],
    #         'res_model': 'property.property'
    #     }

    def compute_child_prop_cnt(self):
        for rec in self:
            rec.child_prop_count = self.search_count(
                [('parent_property_id', '=', rec.id)])

    def action_view_child_properties(self):
        return {
            'name': ('Managed Objects'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'domain': [('parent_property_id', '=', self.id)],
            'res_model': 'property.property'
        }

    @api.depends('name', 'parent_property_id.complete_name')
    def _compute_complete_name(self):
        for property in self:
            if property.parent_property_id:
                property.complete_name = '%s / %s' % (
                    property.parent_property_id.complete_name, property.name)
            else:
                property.complete_name = property.name

    def compute_opportunity_cnt(self):
        for rec in self:
            rec.opportunity_count = self.env['crm.lead'].search_count(
                [('property_id', '=', rec.id)])

    def action_view_opportunity(self):
        action = self.env.ref('crm.crm_lead_opportunities').read()[0]
        action['domain'] = [('property_id', '=', self.id)]
        return action

    @api.model
    def _is_html_field_value_set(self, fieldname):
        value = self[fieldname]
        if value:
            value = value != '<p></p>' and value != '<p><br></p>'
        return value

    def compute_search_profile_count(self):
        for rec in self:
            self.env.cr.execute(
                'SELECT count(*) from rel_search_profile_property where property_id = %s' % (rec.id))
            result = self.env.cr.dictfetchall()
            rec.property_search_profile_count = result[0]['count']

    def action_view_search_profile(self):
        action = self.env.ref(
            'property_management.action_property_search_profile').read()[0]
        action['domain'] = [('property_ids', 'in', [self.id])]
        return action

    @api.onchange('internal_label')
    def change_label(self):
        self.name = self.internal_label

    @api.onchange('parent_property_id')
    def onchange_parent_property(self):
        self.street = self.parent_property_id.street
        self.city = self.parent_property_id.city
        self.zip = self.parent_property_id.zip
        self.country_id = self.parent_property_id.country_id.id
        self.location_id = self.parent_property_id.location_id.id or False
        self.company_id = self.parent_property_id.company_id.id

    @api.model
    def _geo_localize(self, street='', zip='', city='', state='', country=''):
        geo_obj = self.env['base.geocoder']
        search = geo_obj.geo_query_address(
            street=street, zip=zip, city=city, state=state, country=country)
        result = geo_obj.geo_find(search, force_country=country)
        if result is None:
            search = geo_obj.geo_query_address(
                city=city, state=state, country=country)
            result = geo_obj.geo_find(search, force_country=country)
        return result

    def geo_localize(self):
        for property in self.with_context(lang='en_US'):
            result = self._geo_localize(
                property.street, property.zip, property.city, '', property.country_id.name)
            if result:
                property.write({
                    'latitude': result[0],
                    'longitude': result[1],
                })

    @api.constrains('reference_id')
    def check_duplicate_reference(self):
        for rec in self:
            exist = self.search(
                [('reference_id', '=', rec.reference_id), ('id', '!=', rec.id)])
            if exist:
                raise UserError(
                    _('Property with the same reference already exist !'))

    def copy(self, default=None):
        if self.name:
            default = {'name': self.name + ' (copy)'}
            return super(Property, self).copy(default=default)

    @api.model
    def create(self, vals):
        if 'website_published' in vals and vals['website_published']:
            vals['published_date'] = fields.Datetime.now()
        if not vals.get('reference_id'):
            vals['reference_id'] = self.env['ir.sequence'].next_by_code(
                'property.property') or _('New')
        res = super(Property, self).create(vals)
        res.geo_localize()

        res.public_photos_ids.public = True
        res.protected_photos_ids.public = True
        res.protected_documents_ids.public = True

        return res

    def write(self, vals):
        if 'website_published' in vals and vals['website_published']:
            vals['published_date'] = fields.Datetime.now()

        res = super().write(vals)
        if 'street' in vals or 'zip' in vals or 'city' in vals or 'country_id' in vals:
            self.geo_localize()

        if 'public_photos_ids' in vals:
            self.public_photos_ids.public = True
        if 'protected_photos_ids' in vals:
            self.protected_photos_ids.public = True
        if 'protected_documents_ids' in vals:
            self.protected_documents_ids.public = True

        return res

    def create_opportuniy(self):
        property_id = self.id
        partner_id = self.env.context.get('partner_id')
        price = 0
        lead_found = self.env['crm.lead'].search(
            [('partner_id', '=', partner_id), ('property_id', '=', property_id)])
        if lead_found:
            raise UserError(
                _('opportunity already created for this Customer and Property !'))

        property = self.env['property.property'].browse(property_id)
        if property.for_rent:
            price = property.rent_incl_heat
        elif property.for_sale:
            price = property.purchase_price

        self.env['crm.lead'].create({'name': property.name,
                                     'planned_revenue': price,
                                     'partner_id': partner_id,
                                     'property_id': property_id,
                                     'type': 'opportunity'
                                     })

    # JAT
    def _compute_website_url(self):
        super(Property, self)._compute_website_url()
        for property_id in self:
            if property_id.id:
                property_id.website_url = '/real_estate/property/%s' % slug(
                    property_id)

    def _default_website_meta(self):
        res = super(Property, self)._default_website_meta()
        res['default_opengraph']['og:description'] = res['default_twitter']['twitter:description'] = self.property_info
        res['default_opengraph']['og:title'] = res['default_twitter']['twitter:title'] = self.name
        res['default_opengraph']['og:image'] = res['default_twitter']['twitter:image'] = self.env['website'].image_url(
            self, 'cover_photo_d')
        res['default_meta_description'] = self.property_info
        return res

    def image_format(self, images):
        res = tuple(images[x:x + 2]
                    for x in range(0, len(images), 2))
        ls = []
        # for r in res:
        v = 0
        for r in range(0, len(res), 4):
            if (len(images)-2) >= v:
                l = []
                for i in range(r, r + 4):
                    # print("iiiiiiiii", v,images[v:v + 2],len(images) )
                    if i <= len(res):
                        l.append(images[v:v + 2])
                        v += 2
                # print("DDDDDDDDDDDDDDDddd", l)
                ls.append(l)
        return res

    def property_features(self, property_features_ids):
        res = tuple(property_features_ids[x:x + 4]
                    for x in range(0, len(property_features_ids), 4))
        return res
