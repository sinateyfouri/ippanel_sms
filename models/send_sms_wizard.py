# models/send_sms_wizard.py

from odoo import models, fields, api
from odoo.exceptions import UserError
from ippanel import Client

class SendSmsWizard(models.TransientModel):
    _name = 'send.sms.wizard'
    _description = 'Send SMS to Partner'

    partner_id = fields.Many2one('res.partner', string="Recipient", required=True)
    mobile = fields.Char(string="Mobile", related='partner_id.mobile')
    # template_id = fields.Many2one('sms.template', string="Template")
    message = fields.Text(string="Message", required=True)

    # @api.onchange('template_id')
    # def _onchange_template_id(self):
    #     if self.template_id:
    #         self.message = self.template_id.message

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
                "ارسال پیامک از Odoo"
            )

            self.partner_id.message_post(
                body=f"📨 پیامک ارسال شد:\n{self.message}",
                subject="ارسال پیامک با IPPanel",
                message_type="comment"
            )

            self.env['sms.log'].create({
                'partner_id': self.partner_id.id,
                'mobile': self.mobile,
                'message': self.message,
                'sender': sender,
                'status': 'sent',
            })

        except Exception as e:
            self.env['sms.log'].create({
                'partner_id': self.partner_id.id,
                'mobile': self.mobile,
                'message': self.message,
                'sender': sender,
                'status': 'failed',
                'error_message': str(e),
            })
            raise UserError(f"خطا در ارسال پیامک: {str(e)}")
