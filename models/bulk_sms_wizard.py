from odoo import models, fields, api
from odoo.exceptions import UserError
from ippanel import Client

class BulkSmsWizard(models.TransientModel):
    _name = 'bulk.sms.wizard'
    _description = 'Send Bulk SMS to Partners'

    partner_ids = fields.Many2many('res.partner', string="Recipients", required=True)
    message = fields.Text(string="Message", required=True)

    def action_send_bulk_sms(self):
        config = self.env['ir.config_parameter'].sudo()
        api_key = config.get_param('ippanel_sms.ippanel_api_key')
        sender = config.get_param('ippanel_sms.ippanel_sender_number')

        client = Client(api_key)
        errors = []

        for partner in self.partner_ids:
            if not partner.mobile:
                errors.append(f"{partner.name} شماره موبایل ندارد.")
                continue

            try:
                client.send(
                    sender,
                    [partner.mobile],
                    self.message,
                    "ارسال انبوه از Odoo"
                )

                # ثبت در چتر و لاگ
                partner.message_post(body=f"📨 پیامک ارسال شد:\n{self.message}", subject="ارسال پیامک انبوه")
                self.env['sms.log'].create({
                    'partner_id': partner.id,
                    'mobile': partner.mobile,
                    'message': self.message,
                    'sender': sender,
                    'status': 'sent',
                })

            except Exception as e:
                self.env['sms.log'].create({
                    'partner_id': partner.id,
                    'mobile': partner.mobile,
                    'message': self.message,
                    'sender': sender,
                    'status': 'failed',
                    'error_message': str(e),
                })
                errors.append(f"{partner.name}: {str(e)}")

        if errors:
            raise UserError("برخی پیامک‌ها ارسال نشدند:\n" + "\n".join(errors))
