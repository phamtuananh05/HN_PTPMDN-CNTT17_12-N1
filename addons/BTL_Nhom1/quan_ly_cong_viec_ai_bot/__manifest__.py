{
    'name': 'Quan ly cong viec Telegram Bot',
    'version': '15.0.1.0.0',
    'summary': 'Mo rong Telegram cho module quan ly cong viec',
    'description': """
Mo rong module quan ly cong viec:
- Gui thong bao qua Telegram Bot
- Ho tro nhac viec qua han va follow-up
""",
    'category': 'Services',
    'author': 'BTL Nhom 1',
    'license': 'LGPL-3',
    'depends': ['quan_ly_cong_viec', 'base_setup'],
    'data': [
        'data/telegram_task_cron.xml',
        'views/res_config_settings_views.xml',
        'views/task_ai_views.xml',
    ],
    'application': True,
    'installable': True,
}