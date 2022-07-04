# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    dr_gdpr_info = fields.Html('GDPR Info')
