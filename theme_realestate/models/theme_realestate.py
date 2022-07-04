# -*- coding: utf-8 -*-

from odoo import models


class ThemeRealestate(models.AbstractModel):
    _inherit = 'theme.utils'

    def _theme_realestate_post_copy(self, mod):
        self.disable_view('website_theme_install.customize_modal')
