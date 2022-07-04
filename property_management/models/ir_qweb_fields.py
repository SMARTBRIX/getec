# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.tools import html_escape as escape, posix_to_ldml, safe_eval, float_utils, format_date, format_duration, pycompat


class PropertyMonetaryConverter(models.AbstractModel):
    _name = 'ir.qweb.field.property.monetary'
    _description = 'Qweb Field Property Monetary'
    _inherit = 'ir.qweb.field.monetary'

    @api.model
    def get_available_options(self):
        options = super(PropertyMonetaryConverter, self).get_available_options()
        options.update(
            precision=dict(type='integer', string=_('Rounding precision')),
        )
        return options

    @api.model
    def value_to_html(self, value, options):
        display_currency = options['display_currency']

        # Hook
        if not isinstance(value, (int, float)):
            raise ValueError(_("The value send to monetary field is not a number."))

        if 'decimal_precision' in options:
            precision = self.env['decimal.precision'].precision_get(options['decimal_precision'])
        else:
            precision = options['precision']

        if precision is None:
            fmt = "%.{0}f".format(display_currency.decimal_places)
        else:
            value = float_utils.float_round(value, precision_digits=precision)
            fmt = '%.{precision}f'.format(precision=precision)
        # Hook end

        if options.get('from_currency'):
            date = options.get('date') or fields.Date.today()
            company_id = options.get('company_id')
            if company_id:
                company = self.env['res.company'].browse(company_id)
            else:
                company = self.env.company
            value = options['from_currency']._convert(value, display_currency, company, date)

        lang = self.user_lang()
        formatted_amount = lang.format(fmt, display_currency.round(value),
                                grouping=True, monetary=True).replace(r' ', u'\N{NO-BREAK SPACE}').replace(r'-', u'-\N{ZERO WIDTH NO-BREAK SPACE}')

        pre = post = u''
        if display_currency.position == 'before':
            pre = u'{symbol}\N{NO-BREAK SPACE}'.format(symbol=display_currency.symbol or '')
        else:
            post = u'\N{NO-BREAK SPACE}{symbol}'.format(symbol=display_currency.symbol or '')

        return u'{pre}<span class="oe_currency_value">{0}</span>{post}'.format(formatted_amount, pre=pre, post=post)

    @api.model
    def record_to_html(self, record, field_name, options):
        if 'precision' not in options and 'decimal_precision' not in options:
            _, precision = record._fields[field_name].get_digits(record.env) or (None, None)
            options = dict(options, precision=precision)
        return super(PropertyMonetaryConverter, self).record_to_html(record, field_name, options)
