# -*- coding: utf-8 -*-

from odoo import fields, models


class PortfolioReportWizard(models.TransientModel):
    _name = 'portfolio.report.wizard'
    _description = "For Property Pivot"

    date = fields.Date("Date")

    def action_show_graph(self):
        self.env['portfolio.report'].with_context().init()
        return{
            'type': 'ir.actions.act_window',
            'name': 'Portfolio Report',
            'view_mode': 'pivot',
            'res_model': 'portfolio.report',
            'context': self.env.context
        }
