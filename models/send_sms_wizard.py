# models/send_sms_wizard.py

from odoo import models, fields, api
from odoo.exceptions import UserError
from ippanel import Client

class SendSmsWizard(models.TransientModel):
    _name = 'send.sms.wizard'
    _description = 'Send SMS to Partner'

    partner_id = fields.Many2one('res.partner', string="Recipient", required=True)
    mobile = fields.Char(string="Mobile", related='partner_id.mobile')
    message = fields.Text(string="Message", required=True)

    def action_send_sms(self):
        config = self.env['ir.config_parameter'].sudo()
        api_key = config.get_param('ippanel_sms.ippanel_api_key')
        sender = config.get_param('ippanel_sms.ippanel_sender_number')

        if not self.mobile:
            raise UserError("مخاطب شماره موبایل ندارد!")

        try:
            client = Client(api_key)
            client.send(
                sender,
                [self.mobile],
                self.message,
                "ارسال پیامک تستی از ماژول Odoo"
            )
        except Exception as e:
            raise UserError(f"خطا در ارسال پیامک: {str(e)}")
