{
    'name': 'Ippanel SMS Integration',
    'version': '18.0',
    'category': 'Communication',
    'summary': 'Send sms with ippanel.com',
    'author': 'Sina Teyfouri',
    'website' : 'https://asiapardaz.ir',
    'depends': ['base', 'contacts', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'views/send_sms_wizard_view.xml',
        'views/res_partner_view.xml',
        'views/sms_log_views.xml',

    ],
    'application': True,
    'installable': True,
}