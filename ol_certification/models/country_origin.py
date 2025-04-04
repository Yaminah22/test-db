from odoo import api, fields, models
from odoo.exceptions import UserError


class CountryOrigin(models.Model):
    _name = "country.origin"

    group = fields.Integer('Group')
    short_code = fields.Char('Short Code')
    country = fields.Char('Country')
