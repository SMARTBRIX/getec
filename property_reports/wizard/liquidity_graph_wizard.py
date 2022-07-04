# -*- coding: utf-8 -*-

from odoo import fields, models, api


class LiquidityGraph(models.TransientModel):
    _name = 'liquidity.graph'
    _description = "For Liquidity Graph"

    number_of_months = fields.Integer("Number of Months", default='12')
    property_ids = fields.Many2many('property.property', string="Properties")

    def action_show_graph(self):
        self.env['liquidity.report'].with_context({'number_of_months': self.number_of_months, 'property_ids': self.property_ids}).init()
        return{
            'type': 'ir.actions.act_window',
            'name': 'Liquidity Development Graph',
            'view_mode': 'graph,tree',
            'res_model': 'liquidity.report',
            'context': self.env.context
        }
