from odoo import fields, models, _


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    btl_task_count = fields.Integer(
        string='So cong viec phu trach',
        compute='_compute_btl_task_count'
    )

    def _compute_btl_task_count(self):
        Task = self.env['btl.task']
        data = Task.read_group(
            [('employee_id', 'in', self.ids)],
            ['employee_id'],
            ['employee_id']
        )
        mapped_data = {
            item['employee_id'][0]: item['employee_id_count']
            for item in data if item.get('employee_id')
        }

        for record in self:
            record.btl_task_count = mapped_data.get(record.id, 0)

    def action_open_btl_tasks(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Cong viec phu trach'),
            'res_model': 'btl.task',
            'view_mode': 'tree,form',
            'domain': [('employee_id', '=', self.id)],
            'context': {
                'default_employee_id': self.id,
            },
        }