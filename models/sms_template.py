# models/sms_template.py
from odoo import models, fields

class SmsTemplate(models.Model):
    _name = 'ippanel.sms.template'
    _description = 'SMS Template'

    name = fields.Char(string="Template Name", required=True)
    message = fields.Text(string="Template Message", required=True)
    active = fields.Boolean(string="Active", default=True)
