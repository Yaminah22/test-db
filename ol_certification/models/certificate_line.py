from odoo import api, fields, models
from odoo.exceptions import UserError


class CertificateLine(models.Model):
    _name = "certificate.line"
    
    certificate_id = fields.Many2one('certificate.form', string='certificate_id')
    hs_code = fields.Char('HS Code')
    country_of_origin = fields.Char('Country of Origin')
    trademark = fields.Char('Trademark')
    article_no = fields.Integer('Article No.')
    product_name = fields.Char('Product Name')
    group = fields.Char('Group', compute="compute_group_and_model", store=True)
    model = fields.Char('Model', compute="compute_group_and_model", store=True)
    saber_cert_no = fields.Char('Saber Certificate No.') 
    tr_no = fields.Char('TR No.') 
    common_des = fields.Many2one('description.form', string = "Common Description")

    @api.depends('hs_code', 'country_of_origin')
    def compute_group_and_model(self):
        for rec in self:
            rec.group = False
            rec.model = False
            if rec.hs_code and rec.country_of_origin:
                country = self.env['country.origin'].search([('country', 'ilike', rec.country_of_origin)])
                if country:
                    hs_code_trimmed = rec.hs_code[:8]
                    rec.model = hs_code_trimmed + "_" + country.short_code
                    rec.group = str(country.group)
                 


    