from odoo import api, fields, models, _


class BtlTaskDashboard(models.Model):
    _name = 'btl.task.dashboard'
    _description = 'Dashboard cong viec'

    name = fields.Char(default='Dashboard Cong Viec', required=True)
    total_task = fields.Integer(string='Tong cong viec', compute='_compute_stats')
    my_task = fields.Integer(string='Cong viec cua toi', compute='_compute_stats')
    overdue_task = fields.Integer(string='Cong viec qua han', compute='_compute_stats')
    done_today = fields.Integer(string='Hoan thanh hom nay', compute='_compute_stats')
    vip_task = fields.Integer(string='Cong viec khach VIP', compute='_compute_stats')

    def _get_my_employee(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1)

    @api.depends_context('uid')
    def _compute_stats(self):
        Task = self.env['btl.task']
        today = fields.Date.context_today(self)
        employee = self._get_my_employee()

        for record in self:
            record.total_task = Task.search_count([('active', '=', True)])
            record.my_task = Task.search_count([('employee_id', '=', employee.id)]) if employee else 0
            record.overdue_task = Task.search_count([('is_overdue', '=', True), ('active', '=', True)])
            record.done_today = Task.search_count([('completed_date', '=', today)])
            record.vip_task = Task.search_count([('customer_rank', '=', 'vang')])

    def _open_task_action(self, domain=None, name='Cong viec'):
        return {
            'type': 'ir.actions.act_window',
            'name': _(name),
            'res_model': 'btl.task',
            'view_mode': 'tree,form',
            'domain': domain or [],
        }

    def action_open_all_tasks(self):
        return self._open_task_action([], 'Danh sach cong viec')

    def action_open_my_tasks(self):
        employee = self._get_my_employee()
        return self._open_task_action([('employee_id', '=', employee.id)], 'Cong viec cua toi') if employee else self._open_task_action([('id', '=', 0)], 'Cong viec cua toi')

    def action_open_overdue_tasks(self):
        return self._open_task_action([('is_overdue', '=', True)], 'Cong viec qua han')

    def action_open_done_today(self):
        today = fields.Date.context_today(self)
        return self._open_task_action([('completed_date', '=', today)], 'Hoan thanh hom nay')

    def action_open_vip_tasks(self):
        return self._open_task_action([('customer_rank', '=', 'vang')], 'Cong viec khach VIP')