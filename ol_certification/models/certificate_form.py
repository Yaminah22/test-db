from odoo import api, fields, models
from odoo.exceptions import UserError


class CertificateForm(models.Model):
    _name = "certificate.form"
    _inherit =['mail.thread', 'mail.activity.mixin']


    name = fields.Char('Name', required=True)
    email = fields.Char('Email', required=True)
    sample_template = fields.Binary('Sample Template')
    
    state = fields.Selection([('new', 'New'), ('sent', 'Sent'),
                                ('received', 'Received'), ('certification_body', 'Certification Body'),
                                ('submit', 'Submitted on SASO'), ('in_payment', 'In Payment'),
                                ('approved', 'Approved'), ('issued', 'Issued')
                                
                                ], default='new')

    certificate_ids = fields.One2many('certificate.line', 'certificate_id', string='Certicate Information')

    def write(self, vals):
        """Create an attachment when a file is uploaded in the sample_template field."""
        res = super(CertificateForm, self).write(vals)

        # Check if sample_template is updated and is not False
        if 'sample_template' in vals and vals.get('sample_template'):
            self.env['ir.attachment'].create({
                'name': "Sample_Template",
                'datas': vals['sample_template'],
                'res_model': 'certificate.form',
                'res_id': self.id,
                'type': 'binary',
            })
            self.message_post(body="Sample template uploaded successfully.")

        return res
    
    @api.model
    def create(self, vals):
        """Create an attachment when a file is uploaded in the sample_template field."""
        res = super(CertificateForm, self).create(vals)

        # Check if sample_template is updated and is not False
        if 'sample_template' in vals and vals.get('sample_template'):
            self.env['ir.attachment'].create({
                'name': "Sample_Template",
                'datas': vals['sample_template'],
                'res_model': 'certificate.form',
                'res_id': self.id,
                'type': 'binary',
            })
            self.message_post(body="Sample template uploaded successfully.")

        return res
    
    def action_send_email(self):
        """Send an email with the document attached and update the state."""
        if not self.sample_template:
            raise UserError("No attachment found! Please attach a document before sending.")

        if not self.email:
            raise UserError("Please enter an email address.")

        # Get attachments related to this record
        attachments = self.env['ir.attachment'].search([
            ('res_model', '=', 'certificate.form'),
            ('res_id', '=', self.id)
        ])
        attachment_data = [(4, attachment.id) for attachment in attachments]

        # Create an email message
        mail_values = {
            'subject': f"Certificate Document - {self.name}",
            'body_html': f"<p>Dear Sir/Madam,</p><p>Please find the attached certificate document.</p>",
            'email_to': self.email,
            'attachment_ids': attachment_data,
            'auto_delete': False,
        }

        # Send email using mail.mail
        mail = self.env['mail.mail'].create(mail_values)
        mail.send()
        
        # Change state to 'sent' and log in chatter
        self.write({'state': 'sent'})
        self.message_post(
            body="Dear Sir/Madam,<br/>Please find the attached certificate document.",
            body_is_html=True,
            subject=f"Certificate Document - {self.name}",
            message_type='comment',
            subtype_xmlid="mail.mt_comment",
            email_from=self.env.user.email,  # Sender's email
            # email_to=self.email,  # Recipient's email
            attachment_ids=attachments.ids
        )
