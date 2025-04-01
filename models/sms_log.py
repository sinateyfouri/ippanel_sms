from odoo import models, fields, api
from datetime import datetime

class SmsLog(models.Model):
    _name = 'sms.log'
    _description = 'SMS Log'
    _order = 'create_date desc'

    partner_id = fields.Many2one('res.partner', string='Recipient')
    mobile = fields.Char(string='Mobile Number')
    message = fields.Text(string='Message')
    sender = fields.Char(string='Sender Number')
    status = fields.Selection([
        ('sent', 'Sent'),
        ('failed', 'Failed')
    ], string='Status', default='sent')
    error_message = fields.Text(string='Error (if any)')
    send_date = fields.Datetime(string='Send Date', default=fields.Datetime.now)
