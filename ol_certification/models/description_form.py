from odoo import api, fields, models
from odoo.exceptions import UserError


class DescriptionForm(models.Model):
    _name = "description.form"

    name = fields.Char('Name')
