# -*- coding: utf-8 -*-

from odoo import fields, models, api
import base64
from PIL import Image
import io


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'
    _order = 'sequence'

    sequence = fields.Integer(default=16)

    @api.model
    def create(self, vals):
        if vals.get('res_model', False) == 'property.property':
            image_data = vals.get('datas')
            image_name = vals.get('name')
            vals['datas'] = self.compress_image(image_data, image_name)
        return super(IrAttachment, self).create(vals)

    def compress_image(self, image_data, image_name):
        image_extension = ['jpeg', 'jpg', 'png']
        try:
            if '.' in image_name and image_name.lower().split('.')[1] in image_extension:
                image = Image.open(io.BytesIO(base64.b64decode(image_data)))
                quality = 85
                #image_size = len(image.fp.read()) / 1000
                # if image_size > 2000:
                #     quality = 25
                # elif image_size > 1000:
                #     quality = 30
                # width, height = image.size
                # if width > 1920:
                #     image = image.resize((round(width * 0.8), round(height * 0.8)))
                ext = image_name.split('.')[1]
                opt = 'JPEG' if ext.lower() == 'jpg' else ext.upper()
                buffer = io.BytesIO()
                image.save(buffer, quality=quality, optimize=True, format=opt)
                data = buffer.getvalue()
                image_data = base64.b64encode(data)
                return image_data
        except Exception:
            return image_data
