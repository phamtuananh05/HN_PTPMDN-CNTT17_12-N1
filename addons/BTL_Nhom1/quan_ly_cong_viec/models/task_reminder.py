from odoo import fields, models


class BtlTaskReminder(models.Model):
    _name = 'btl.task.reminder'
    _description = 'Nhat ky nhac viec'
    _order = 'reminder_date desc, id desc'

    name = fields.Char(string='Tieu de', required=True)
    task_id = fields.Many2one('btl.task', string='Cong viec', required=True, ondelete='cascade')
    employee_id = fields.Many2one('hr.employee', string='Nhan vien phu trach')
    reminder_date = fields.Date(string='Ngay nhac', required=True, default=lambda self: fields.Date.context_today(self))
    note = fields.Text(string='Noi dung')