from odoo import models, fields, api
from odoo.exceptions import UserError
from ippanel import Client

class BulkSmsWizard(models.TransientModel):
    _name = 'bulk.sms.wizard'
    _description = 'Send Bulk SMS to Partners'

    tag_ids = fields.Many2many('res.partner.category', string="فیلتر تگ مخاطبین")
    message = fields.Text(string="متن پیام", required=True)

    def action_send_bulk_sms(self):
        partners = self.env['res.partner'].search([
            ('category_id', 'in', self.tag_ids.ids),
            ('mobile', '!=', False)
        ])

        if not partners:
            raise UserError("هیچ مخاطبی با این تگ‌ها و شماره موبایل پیدا نشد!")

        config = self.env['ir.config_parameter'].sudo()
        api_key = config.get_param('ippanel_sms.ippanel_api_key')
        sender = config.get_param('ippanel_sms.ippanel_sender_number')
        client = Client(api_key)

        for partner in partners:
            try:
                client.send(
                    sender,
                    [partner.mobile],
                    self.message,
                    "ارسال انبوه پیامک"
                )
                # لاگ موفق
                self.env['sms.log'].create({
                    'partner_id': partner.id,
                    'mobile': partner.mobile,
                    'message': self.message,
                    'sender': sender,
                    'status': 'sent',
                })
                # در چتر مخاطب ثبت کن
                partner.message_post(
                    body=f"📨 پیامک انبوه ارسال شد:\n{self.message}",
                    subject="ارسال پیامک با IPPanel",
                    message_type="comment"
                )
            except Exception as e:
                # لاگ شکست
                self.env['sms.log'].create({
                    'partner_id': partner.id,
                    'mobile': partner.mobile,
                    'message': self.message,
                    'sender': sender,
                    'status': 'failed',
                    'error_message': str(e),
                })
