# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Property(models.Model):
    _inherit = 'property.property'

    district_court = fields.Many2one("res.partner", string="District Court")
    date = fields.Datetime(string="Date")
    room = fields.Char(string="Room")
    remarks = fields.Text(string="Remarks")
    status = fields.Char(string="Status")
    loan_number = fields.Char(string="Loan Number")
    principal_borrower = fields.Many2one("res.partner", string="Principal Borrower")
    chief_clerk = fields.Many2one("res.partner", string="Chief Clerk")
    main_appointment_represent = fields.Many2one("res.partner", string="Main Appointment Representative")
    status_foreclosure = fields.Selection([('not_foreclosure', 'Object is not in foreclosure'),
                                           ('in_foreclosure', 'Object is in foreclosure'),
                                           ('wait_foreclosure', 'Object is in foreclosure, waiting for a new date')])
    forclosure_market_value = fields.Float(string="Market Value")
    market_value_70 = fields.Float(compute="_compute_market_value_70")
    market_value_50 = fields.Float(compute="_compute_market_value_50")
    market_value_30 = fields.Float(compute="_compute_market_value_30")
    market_value_5 = fields.Float(compute="_compute_market_value_5")
    file_district_court = fields.Char(string="File number District Court")

    @api.depends('forclosure_market_value')
    def _compute_market_value_70(self):
        for rec in self:
            rec.market_value_70 = rec.forclosure_market_value * 0.7
            rec.market_value_50 = rec.forclosure_market_value * 0.5
            rec.market_value_30 = rec.forclosure_market_value * 0.3
            rec.market_value_5 = rec.forclosure_market_value * 0.05
