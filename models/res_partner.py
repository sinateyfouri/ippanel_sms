# models/res_partner.py

from odoo import models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    def action_open_sms_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Send SMS',
            'res_model': 'send.sms.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_partner_id': self.id,
            },
        }
