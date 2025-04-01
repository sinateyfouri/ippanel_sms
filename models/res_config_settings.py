from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    _description = 'ippanel sms settings'


    use_ippanel_sms = fields.Boolean(string="Enable Sending SMS with ippanel", config_parameter='ippanel_sms.use_feature')
    ippanel_api_key = fields.Char(string="ippannel API")
    ippanel_sender_number = fields.Char(string="ippanel sender number")

    @api.model
    def set_values(self):
        """ذخیره مقادیر در پایگاه داده"""
        super(ResConfigSettings, self).set_values()
        params = self.env['ir.config_parameter'].sudo()

        params.set_param('ippanel_sms.use_ippanel_sms', "True" if self.use_ippanel_sms else "False")
        params.set_param('ippanel_sms.ippanel_api_key', self.ippanel_api_key or "")
        params.set_param('ippanel_sms.ippanel_sender_number', self.ippanel_sender_number or "")



    @api.model
    def get_values(self):
        """خواندن مقادیر از پایگاه داده هنگام باز کردن صفحه تنظیمات"""
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()

        res.update({
            'use_ippanel_sms': params.get_param('ippannel_sms.use_ippanel_sms', 'False') == "True",
            'ippanel_api_key': params.get_param('ippanel_sms.ippanel_api_key', default=''),
            'ippanel_sender_number' : params.get_param('ippanel_sms.ippanel_sender_number', default=''),

        })
        return res