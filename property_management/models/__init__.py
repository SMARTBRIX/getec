# -*- coding: utf-8 -*-

from . import realestate
from . import crm
from . import res_partner
from . import res_company
from . import property_search_profile
from . import website
from . import ir_qweb_fields
from . import attachment
from odoo.addons.base_import.models import base_import as base_import

base_import.IMAGE_FIELDS = ["icon", "image", "logo", "picture", "photo"]