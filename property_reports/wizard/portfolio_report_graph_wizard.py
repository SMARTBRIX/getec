# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class PortfolioGraph(models.TransientModel):
    _name = 'portfolio.graph'
    _description = "For Property Graph"

    start_year = fields.Integer("Start Year")
    end_year = fields.Integer("End Year")

    @api.constrains('start_year', 'end_year')
    def _year_validation(self):
        for record in self:
            if len(str(record.start_year)) != 4:
                raise ValidationError(_("Start Year is not Valid."))
            if len(str(record.end_year)) != 4:
                raise ValidationError(_("End Year is not Valid."))

    def action_show_graph(self):
        self.env['portfolio.report.graph'].with_context().init()
        return{
            'type': 'ir.actions.act_window',
            'name': 'Portfolio Development Graph',
            'view_mode': 'graph',
            'res_model': 'portfolio.report.graph',
            'context': self.env.context
        }
