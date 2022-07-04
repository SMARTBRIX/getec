# -*- coding: utf-8 -*-

from odoo import api, fields, models


class DrPropertyContactFields(models.Model):
    _name = 'dr.property.contact.fields'
    _description = 'Property Contact Fields'

    name = fields.Char()
    required = fields.Boolean(string='Required?')
    field_name = fields.Char(related='field_id.name')
    field_id = fields.Many2one('ir.model.fields', domain=[('model_id.model', '=', 'crm.lead')], required=True, ondelete='cascade')


class Website(models.Model):
    _inherit = 'website'

    dr_property_sales_team = fields.Many2one('crm.team', string='Sales Team')
    dr_property_crm_stage = fields.Many2one('crm.stage', string='CRM Stage')
    dr_property_contact_fields_ids = fields.Many2many('dr.property.contact.fields', string='Contact Form Fields')


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    dr_property_sales_team = fields.Many2one(related='website_id.dr_property_sales_team', readonly=False)
    dr_property_crm_stage = fields.Many2one(related='website_id.dr_property_crm_stage', readonly=False)
    dr_property_contact_fields_ids = fields.Many2many(related='website_id.dr_property_contact_fields_ids', readonly=False)
