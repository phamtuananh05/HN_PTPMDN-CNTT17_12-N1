from odoo import fields, models, _
from odoo.exceptions import UserError

import json
import urllib.parse
import urllib.request


class BtlTask(models.Model):
    _inherit = 'btl.task'

    telegram_message = fields.Text(string='Noi dung Telegram', readonly=True)
    telegram_notified = fields.Boolean(string='Da gui Telegram', default=False, readonly=True)
    telegram_sent_at = fields.Datetime(string='Thoi diem gui Telegram', readonly=True)

    telegram_type = fields.Selection(
        [
            ('test', 'Test'),
            ('followup', 'Follow-up'),
            ('overdue', 'Qua han'),
        ],
        string='Loai Telegram gan nhat',
        readonly=True,
    )

    overdue_telegram_sent = fields.Boolean(string='Da gui Telegram qua han', default=False, readonly=True)
    followup_telegram_sent = fields.Boolean(string='Da gui Telegram follow-up', default=False, readonly=True)

    def _build_telegram_message(self, title='Thong bao cong viec'):
        self.ensure_one()

        task_type = dict(self._fields['task_type'].selection).get(self.task_type, '')
        lines = [
            f'[BTL] {title}',
            f'Khach hang: {self.customer_id.name or ""}',
            f'Cong viec: {self.name or ""}',
            f'Loai cong viec: {task_type}',
            f'Nguoi lien he: {self.contact_person_id.name or ""}',
            f'Nhan vien phu trach: {self.employee_id.name or ""}',
            f'Han xu ly: {self.deadline_date or ""}',
            f'Giai doan: {self.stage_id.name or ""}',
        ]
        return '\n'.join(lines)

    def _get_telegram_config(self):
        config = self.env['ir.config_parameter'].sudo()
        bot_token = config.get_param('btl_ai_bot.telegram_bot_token')
        chat_id = config.get_param('btl_ai_bot.telegram_chat_id')
        return bot_token, chat_id

    def _send_telegram_message(self, message):
        bot_token, chat_id = self._get_telegram_config()

        if not bot_token:
            raise UserError(_('Chua cau hinh Telegram Bot Token trong phan Cai dat.'))
        if not chat_id:
            raise UserError(_('Chua cau hinh Telegram Chat ID trong phan Cai dat.'))

        url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
        payload = {
            'chat_id': chat_id,
            'text': message,
        }

        data = urllib.parse.urlencode(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, method='POST')

        try:
            with urllib.request.urlopen(req, timeout=20) as response:
                response_data = response.read().decode('utf-8')
                result = json.loads(response_data)
        except Exception as e:
            raise UserError(_('Khong gui duoc Telegram: %s') % str(e))

        if not result.get('ok'):
            raise UserError(_('Telegram API tra ve loi: %s') % result)

        return result

    def _write_telegram_log(self, message, telegram_type):
        self.ensure_one()
        vals = {
            'telegram_message': message,
            'telegram_notified': True,
            'telegram_sent_at': fields.Datetime.now(),
            'telegram_type': telegram_type,
        }
        if telegram_type == 'overdue':
            vals['overdue_telegram_sent'] = True
        if telegram_type == 'followup':
            vals['followup_telegram_sent'] = True
        self.write(vals)

    def action_send_test_telegram(self):
        for record in self:
            message = record._build_telegram_message(title='Thong bao test Telegram')
            record._send_telegram_message(message)
            record._write_telegram_log(message, 'test')

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Da gui Telegram'),
                'message': _('Da gui thong bao Telegram thanh cong.'),
                'type': 'success',
                'sticky': False,
            }
        }

    def action_move_to_done(self):
        before_child_map = {}
        for record in self:
            before_child_map[record.id] = set(record.child_task_ids.ids)

        res = super().action_move_to_done()

        for record in self:
            before_ids = before_child_map.get(record.id, set())
            new_followups = record.child_task_ids.filtered(lambda t: t.id not in before_ids)

            for followup in new_followups:
                if not followup.followup_telegram_sent:
                    message = followup._build_telegram_message(title='Da tao cong viec follow-up moi')
                    try:
                        followup._send_telegram_message(message)
                        followup._write_telegram_log(message, 'followup')
                    except Exception:
                        # Khong chan luong nghiep vu chinh neu Telegram loi
                        pass

        return res

    def cron_notify_overdue_tasks_telegram(self):
        overdue_tasks = self.search([
            ('is_overdue', '=', True),
            ('is_done', '=', False),
            ('active', '=', True),
            ('overdue_telegram_sent', '=', False),
        ])

        for task in overdue_tasks:
            message = task._build_telegram_message(title='Canh bao cong viec qua han')
            try:
                task._send_telegram_message(message)
                task._write_telegram_log(message, 'overdue')
            except Exception:
                # Khong lam cron dung toan bo neu 1 task gui loi
                continue

        return True