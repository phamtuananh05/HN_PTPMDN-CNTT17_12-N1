from odoo import api, fields, models, _


class BtlCustomerDashboard(models.Model):
    _name = 'btl.customer.dashboard'
    _description = 'Dashboard khach hang'

    name = fields.Char(default='Dashboard Khach Hang', required=True)
    total_customer = fields.Integer(string='Tong khach hang', compute='_compute_stats')
    gold_customer = fields.Integer(string='Khach hang vang', compute='_compute_stats')
    my_customer = fields.Integer(string='Khach hang cua toi', compute='_compute_stats')
    need_care_today = fields.Integer(string='Can cham soc hom nay', compute='_compute_stats')

    def _get_my_employee(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1)

    @api.depends_context('uid')
    def _compute_stats(self):
        Customer = self.env['btl.customer']
        today = fields.Date.context_today(self)
        employee = self._get_my_employee()
        for record in self:
            record.total_customer = Customer.search_count([])
            record.gold_customer = Customer.search_count([('rank', '=', 'vang')])
            record.my_customer = Customer.search_count([('employee_id', '=', employee.id)]) if employee else 0
            record.need_care_today = Customer.search_count([
                ('next_care_date', '=', today),
                ('active', '=', True),
            ])

    def _action_customer(self, domain=None):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Khach hang'),
            'res_model': 'btl.customer',
            'view_mode': 'tree,form',
            'domain': domain or [],
        }

    def action_open_all_customers(self):
        return self._action_customer([])

    def action_open_gold_customers(self):
        return self._action_customer([('rank', '=', 'vang')])

    def action_open_my_customers(self):
        employee = self._get_my_employee()
        return self._action_customer([('employee_id', '=', employee.id)]) if employee else self._action_customer([('id', '=', 0)])

    def action_open_need_care(self):
        today = fields.Date.context_today(self)
        return self._action_customer([('next_care_date', '=', today)])