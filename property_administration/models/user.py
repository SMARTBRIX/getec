# -*- coding: utf-8 -*-

from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    signature_img = fields.Binary(string="Signature")
