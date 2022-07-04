# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, datetime, timedelta
import math


class PropertyTenancy(models.Model):
    _name = 'property.tenancy'
    _description = "Tenancy"
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin',
                'utm.mixin', 'website.seo.metadata', 'website.published.multi.mixin']

    name = fields.Char('Name', required=True)
    property_id = fields.Many2one('property.property', string="Property")
    type = fields.Selection([('rental', 'Rental'), ('owner', 'Ownership'), ('own', 'Own Use'), ('vacancy', 'Vacancy')])
    partner_id = fields.Many2one('res.partner', string="Invoice address")
    contractual_partner_ids = fields.Many2many('res.partner', 'rel_tenancy_contractual', 'tenancy_id', 'partner_id', string="Contractual Partner")
    resident_ids = fields.Many2many('res.partner', string="Residents")
    date_start = fields.Date("Start Date")
    date_end = fields.Date("End Date")
    billing_type = fields.Selection([('separate', 'Separate advance payments for ancillary costs and heating'), (
        'combined', 'Combined advance payment for all ancillary costs'), ('flatrate', 'Flatrate Rent')], string="Billing Type")
    rent_ids = fields.One2many('property.rent', 'tenancy_id', string="Rent Price")
    cost_type_ids = fields.Many2many('property.cost.type', string="Cost Types")
    property_cost_type_ids = fields.Many2many('property.cost.type', related='property_id.cost_type_ids')
    documents = fields.Many2many('ir.attachment', string="Contract Documents")
    stage_id = fields.Many2one('tenancy.stage', tracking=True)
    cover_photo = fields.Binary('Cover Photo', related="partner_id.image_1920")
    contract_text = fields.Html("Tenancy Contract Text")
    template_id = fields.Many2one('mail.template', string="Mail Template", domain="[('model', '=', 'property.tenancy')]")
    rent_product_id = fields.Many2one('product.template', string="Rent Product")
    heating_cost_type_id = fields.Many2one('property.cost.type', string="Heating Cost Type")
    ancillary_cost_type_id = fields.Many2one('property.cost.type', string="Ancillary Cost Type")
    company_id = fields.Many2one('res.company', related='property_id.company_id', string="Company", store=True)

    @api.onchange('property_id')
    def _onchange_property(self):
        if self.property_id:
            self.property_cost_type_ids = self.property_id.cost_type_ids
        else:
            self.property_cost_type_ids = False

    @api.onchange('template_id')
    def _onchange_of_template(self):
        template_id = self.env['mail.template'].search([('id', '=', self.template_id.id)])
        self.contract_text = template_id._render_template(template_id.body_html, 'property.tenancy', [self.id])[self.id]

    def _create_rent_invoice(self):
        res = self.env['property.tenancy'].search([('type', '=', 'rental')])
        for rec in res:
            if date.today() >= rec.date_start and date.today() <= rec.date_end:
                month_name = datetime.now().strftime('%B')
                rents = self.env['property.rent'].search([('tenancy_id', '=', rec.id), ('date_start', '<=', date.today()),
                                                          ('day_of_invoice', '=', date.today().day)])
                rent_product = rec.rent_product_id
                ancillary_product = rec.ancillary_cost_type_id.product_id
                heating_product = rec.heating_cost_type_id.product_id
                tax_rent_product = rent_product.taxes_id.filtered(lambda t: t.company_id == rec.property_id.company_id)
                tax_ancillary_product = ancillary_product.taxes_id.filtered(lambda t: t.company_id == rec.property_id.company_id)
                tax_heating_product = heating_product.taxes_id.filtered(lambda t: t.company_id == rec.property_id.company_id)
                fiscal_position = rec.partner_id.property_account_position_id.id
                for line in rents:
                    period = ''
                    billing_period = ''
                    mydate = datetime.now()
                    quarters = [['January', 'February', 'March'], ['April', 'May', 'June'], [
                        'July', 'August', 'September'], ['October', 'November', 'December']]

                    if line.billing_period == 'monthly':
                        period = period + \
                            mydate.strftime("%B") + ' ' + mydate.strftime("%Y")
                        billing_period = 'monthly'
                    elif line.billing_period == 'quarterly':
                        quarter = quarters[math.ceil(float(mydate.strftime("%m")) / 3) - 1]
                        period = period + \
                            ' ' .join(str(i) for i in quarter)
                        billing_period = 'quarterly'
                    else:
                        period = period + mydate.strftime("%Y")
                        billing_period = 'yearly'

                    end_date = self.get_billing_end_date(datetime.today(), billing_period)

                    if line.billing_period == 'monthly' or (line.billing_period == 'quarterly' and month_name in ('January', 'April', 'July', 'October')) or (line.billing_period == 'yearly' and month_name == 'January'):
                        narration = 'Contractual Partners: ' + ', '.join([partner.name for partner in rec.contractual_partner_ids]) + "\n" + 'Residents: ' + \
                            ','.join([recident.name for recident in rec.resident_ids]) + "\n" + 'Billing Period: ' + period + "\n" + 'Property Name: ' + line.tenancy_id.property_id.name or ' ' + "\n" + 'Property Address: ' + line.tenancy_id.property_id.street or ' ' + line.tenancy_id.property_id.city or ' ' + line.tenancy_id.property_id.zip or ' '
                        invoice_id = self.env['account.move'].create(
                            {'company_id': line.tenancy_id.company_id.id, 'partner_id': line.tenancy_id.partner_id.id,
                             'ref': line.tenancy_id.name, 'type': 'out_invoice',
                             'narration': narration})
                        rec.property_id.bill_id = invoice_id.id
                        description = "Your rent for property " + \
                            line.tenancy_id.property_id.name + ", billed " + line.billing_period + ""
                        rent_product_account = rent_product.get_product_accounts(fiscal_pos=fiscal_position)['income']
                        self.env['account.move.line'].with_context({'check_move_validity': False}).create(
                            {'move_id': invoice_id.id, 'product_id': rent_product.id, 'account_id': rent_product_account.id,
                             'name': description, 'quantity': 1, 'analytic_account_id': rec.property_id.analytic_account_id.id,
                             'price_unit': line.rent, 'tax_ids': tax_rent_product.ids, 'company_id': line.tenancy_id.company_id.id})
                        if rec.billing_type == 'combined' or rec.billing_type == 'separate':
                            description = 'Advance payment for ancillary costs'
                            ancillary_product_account = ancillary_product.product_tmpl_id.get_product_accounts(
                                fiscal_pos=fiscal_position)['income']
                            self.env['account.move.line'].with_context({'check_move_validity': False}).create(
                                {'move_id': invoice_id.id, 'product_id': ancillary_product.id, 'account_id': ancillary_product_account.id,
                                 'name': description, 'quantity': 1, 'analytic_account_id': rec.property_id.analytic_account_id.id,
                                 'price_unit': line.ancillary_costs, 'tax_ids': tax_ancillary_product.ids, 'company_id': line.tenancy_id.company_id.id})
                            self.env['property.journal'].create({'tenancy_id': rec.id, 'cost_type_id': rec.ancillary_cost_type_id.id, 'date_start': datetime.today(), 'date_end': end_date, 'amount': -line.ancillary_costs})
                        if rec.billing_type == 'separate':
                            description = 'Separate advance payment for heating costs'
                            heating_product_account = heating_product.product_tmpl_id.get_product_accounts(
                                fiscal_pos=fiscal_position)['income']
                            self.env['account.move.line'].with_context({'check_move_validity': False}).create(
                                {'move_id': invoice_id.id, 'product_id': heating_product.id, 'account_id': heating_product_account.id,
                                 'name': description, 'quantity': 1, 'analytic_account_id': rec.property_id.analytic_account_id.id,
                                 'price_unit': line.heating_costs, 'tax_ids': tax_heating_product.ids, 'company_id': line.tenancy_id.company_id.id})
                            self.env['property.journal'].create({'tenancy_id': rec.id, 'cost_type_id': rec.heating_cost_type_id.id, 'date_start': datetime.today(), 'date_end': end_date, 'amount': -line.heating_costs})
                        invoice_id.with_context({'check_move_validity': False})._recompute_tax_lines()
                        invoice_id.with_context({'check_move_validity': False})._onchange_recompute_dynamic_lines()

    def get_billing_end_date(self, date, type):
        if type == 'monthly':
            if date.month == 12:
                return date.replace(day=31)
            return date.replace(month=date.month + 1, day=1) - timedelta(days=1)
        elif type == 'quarterly':
            current_quarter = round((date.month - 1) / 3 + 1)
            month = 3 * current_quarter + 1
            if month > 12:
                month = 12
                last_date = datetime(date.year, month, 31)
            else:
                last_date = datetime(date.year, month, 1) + timedelta(days=-1)
            return last_date.date()
        else:
            epoch_year = date.today().year
            return datetime(epoch_year, 12, 31)


class TenancyStage(models.Model):
    _name = 'tenancy.stage'
    _description = "Tenancy Stage"

    name = fields.Char()
