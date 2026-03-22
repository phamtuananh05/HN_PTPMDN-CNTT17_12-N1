from odoo import fields, models, _


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    btl_customer_count = fields.Integer(
        string='So khach hang phu trach',
        compute='_compute_btl_customer_count'
    )

    def _compute_btl_customer_count(self):
        Customer = self.env['btl.customer']
        data = Customer.read_group(
            [('employee_id', 'in', self.ids)],
            ['employee_id'],
            ['employee_id']
        )
        mapped_data = {
            item['employee_id'][0]: item['employee_id_count']
            for item in data if item.get('employee_id')
        }

        for record in self:
            record.btl_customer_count = mapped_data.get(record.id, 0)

    def action_open_btl_customers(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Khach hang phu trach'),
            'res_model': 'btl.customer',
            'view_mode': 'tree,form',
            'domain': [('employee_id', '=', self.id)],
            'context': {
                'default_employee_id': self.id,
            },
        }