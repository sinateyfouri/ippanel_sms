from odoo import models, fields, api
from odoo.exceptions import UserError
from ippanel import Client

class BulkSmsWizard(models.TransientModel):
    _name = 'bulk.sms.wizard'
    _description = 'Send Bulk SMS to Partners'

    partner_ids = fields.Many2many('res.partner', string="مخاطبین خاص (اختیاری)")
    tag_ids = fields.Many2many('res.partner.category', string="فیلتر تگ مخاطبین")
    template_id = fields.Many2one('ippanel.sms.template', string="Template")
    message = fields.Text(string="متن پیام", required=True)

    @api.onchange('template_id')
    def _onchange_template_id(self):
        if self.template_id:
            self.message = self.template_id.message

    def action_send_bulk_sms(self):
        # اگر مخاطبین خاص انتخاب شده بودن، فقط به اون‌ها ارسال کن
        if self.partner_ids:
            partners = self.partner_ids.filtered(lambda p: p.mobile)
        else:
            # در غیر این صورت، براساس تگ ارسال کن
            partners = self.env['res.partner'].search([
                ('category_id', 'in', self.tag_ids.ids),
                ('mobile', '!=', False)
            ])

        if not partners:
            raise UserError("هیچ مخاطبی برای ارسال یافت نشد.")

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
                self.env['sms.log'].create({
                    'partner_id': partner.id,
                    'mobile': partner.mobile,
                    'message': self.message,
                    'sender': sender,
                    'status': 'sent',
                })
                partner.message_post(
                    body=f"📨 پیامک انبوه ارسال شد:\n{self.message}",
                    subject="ارسال پیامک با IPPanel",
                    message_type="comment"
                )
            except Exception as e:
                self.env['sms.log'].create({
                    'partner_id': partner.id,
                    'mobile': partner.mobile,
                    'message': self.message,
                    'sender': sender,
                    'status': 'failed',
                    'error_message': str(e),
                })

