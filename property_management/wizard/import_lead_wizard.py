# -*- coding: utf-8 -*-

import base64
import logging

import openpyxl
from io import BytesIO

from odoo import fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ImportLeadizard(models.TransientModel):
    _name = 'import.lead.wizard'
    _description = 'Import Lead Wizard'

    file = fields.Binary('File')
    name = fields.Char('File Name')

    def import_data(self):
        self.ensure_one()
        CRM = self.env['crm.lead']
        UtmSource = self.env['utm.source']
        PropertyType = self.env['property.type']
        #Company = self.env['res.company']

        skipped_lines = []

        decoded_data = base64.b64decode(self.file)
        file = BytesIO(decoded_data)
        workbook = openpyxl.load_workbook(file)
        sheet = workbook[workbook.get_sheet_names()[0]]

        for row in sheet.iter_rows(min_row=2):
            data = []
            try:
                r = sheet._current_row
                internal_note = ''

                source = row[0].value
                source_id = False
                if source:
                    source_id = UtmSource.search([('name', '=', source)], limit=1)
                    if not source_id:
                        source_id = UtmSource.create({
                            'name': source
                        })

                property_typ_first = row[1].value
                if property_typ_first.find('zum Kauf') > 0:
                    property_typ = 's'
                else:
                    property_typ = 'r'

                property_street = row[2].value
                property_zip = row[3].value
                property_city = row[4].value
                phone = row[5].value

                # property_owner = row[6].value
                # if property_owner:
                #     property_owner_id = Company.search([('name', '=', property_owner)], limit=1)
                #     if not property_owner_id:
                #         raise UserError(_('Please First Create Company : %s. And assigned to logged User First!') % (property_owner))

                company_name = row[6].value
                contact_name = row[7].value

                start_offer = row[8].value

                internal_note += 'Start of offer :' + ' ' + start_offer + '\n'

                end_offer = row[9].value

                internal_note += 'End of offer :' + ' ' + end_offer + '\n'

                minimum_price = row[10].value
                maximum_price = row[11].value

                internal_note += 'Maximum Price :' + ' ' + maximum_price + '\n'

                last_change = row[12].value

                internal_note += 'Last Changed :' + ' ' + last_change + '\n'

                currently_rented = row[13].value

                internal_note += 'Currenty Rented :' + ' ' + currently_rented + '\n'

                double_field = row[14].value

                construction_year = row[15].value
                rooms = float(row[16].value.replace(',', '.'))

                living_space = row[17].value
                price_per_square_feet = row[18].value.replace(',', '.')

                internal_note += 'Price per Square Meter :' + ' ' + price_per_square_feet + '\n'

                property_type = row[19].value
                property_type_id = False

                if property_type:
                    property_type_id = PropertyType.search([('name', '=', property_type)], limit=1)
                    if not property_type_id:
                        property_type_id = PropertyType.create({
                            'name': property_type
                        })

                commission_client = row[20].value

                data_provider = row[21].value

                link = row[22].hyperlink.target

                vals = {
                    'name': property_typ_first + ', ' + property_city,
                    'source_id': source_id.id,
                    'property_type': property_typ,
                    'property_type_id': property_type_id.id,
                    'property_street': property_street,
                    'property_zip': property_zip,
                    'phone': phone,
                    'property_city': property_city,
                    #'company_id': property_owner_id.id,
                    'contact_name': contact_name,
                    'partner_name': company_name,
                    'construction_year': construction_year,
                    'rooms': rooms,
                    'living_space': living_space,
                    'property_price': minimum_price,
                    'commission_client': commission_client,
                    'referred': data_provider,
                    'website': link,
                    'description': internal_note,
                }
                CRM.sudo().create(vals)
                data = [
                    source,
                    property_typ_first,
                    property_street,
                    property_zip,
                    property_city,
                    phone,
                    company_name,
                    contact_name,
                    start_offer,
                    end_offer,
                    minimum_price,
                    maximum_price,
                    last_change,
                    currently_rented,
                    double_field,
                    construction_year,
                    rooms,
                    living_space,
                    price_per_square_feet,
                    property_type,
                    commission_client,
                    data_provider,
                    row[22].value
                ]
            except Exception as e:
                line = ','.join(map(str, data))
                skipped_lines.append(data)
                raise UserError(_('Please Check Row #%s\nLine : %s\nProblem : %s') % (r, line, e))

        _logger.info("____ Skipped Lines : %s", skipped_lines)

        return {'type': 'ir.actions.act_window_close'}
