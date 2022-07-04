# -*- coding: utf-8 -*-

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    charges_account_id = fields.Many2one('account.account')


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    charges_account_id = fields.Many2one('account.account', related='company_id.charges_account_id', string="Charges Account", readonly=False)
