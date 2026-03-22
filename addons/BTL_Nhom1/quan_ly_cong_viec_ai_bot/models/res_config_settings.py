from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    telegram_bot_token = fields.Char(
        string='Telegram Bot Token',
        config_parameter='btl_ai_bot.telegram_bot_token',
    )

    telegram_chat_id = fields.Char(
        string='Telegram Chat ID',
        config_parameter='btl_ai_bot.telegram_chat_id',
    )