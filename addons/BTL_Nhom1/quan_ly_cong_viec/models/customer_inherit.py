from odoo import api, fields, models, _


class BtlCustomer(models.Model):
    _inherit = 'btl.customer'

    task_count = fields.Integer(string='So cong viec', compute='_compute_task_count')

    def _compute_task_count(self):
        Task = self.env['btl.task']
        for record in self:
            record.task_count = Task.search_count([('customer_id', '=', record.id)])

    def action_open_tasks(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Cong viec'),
            'res_model': 'btl.task',
            'view_mode': 'tree,form',
            'domain': [('customer_id', '=', self.id)],
            'context': {'default_customer_id': self.id},
        }