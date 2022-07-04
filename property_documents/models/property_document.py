# -*- coding: utf-8 -*-

from odoo import fields, models


class DocumentsDocument(models.Model):
    _inherit = 'documents.document'

    property_id = fields.Many2one('property.property', string="Property")
