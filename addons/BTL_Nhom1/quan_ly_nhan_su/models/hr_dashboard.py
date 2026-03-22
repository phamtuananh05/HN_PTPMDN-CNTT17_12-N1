from odoo import api, fields, models, _


class BtlHrDashboard(models.Model):
    _name = 'btl.hr.dashboard'
    _description = 'Dashboard nhan su'

    name = fields.Char(default='Dashboard Nhan Su', required=True)
    total_employee = fields.Integer(string='Tong nhan vien', compute='_compute_stats')
    total_department = fields.Integer(string='Tong phong ban', compute='_compute_stats')
    my_profile = fields.Integer(string='Ho so cua toi', compute='_compute_stats')
    total_family = fields.Integer(string='Tong than nhan', compute='_compute_stats')
    total_work_history = fields.Integer(string='Tong QT cong tac', compute='_compute_stats')

    def _get_my_employee(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1)

    @api.depends_context('uid')
    def _compute_stats(self):
        Employee = self.env['hr.employee']
        Department = self.env['hr.department']
        Family = self.env['btl.hr.family']
        WorkHistory = self.env['btl.hr.work.history']
        my_employee = self._get_my_employee()

        for record in self:
            record.total_employee = Employee.search_count([])
            record.total_department = Department.search_count([])
            record.my_profile = 1 if my_employee else 0
            record.total_family = Family.search_count([])
            record.total_work_history = WorkHistory.search_count([])

    def action_open_employees(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Nhan vien'),
            'res_model': 'hr.employee',
            'view_mode': 'tree,form',
        }

    def action_open_departments(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Phong ban'),
            'res_model': 'hr.department',
            'view_mode': 'tree,form',
        }

    def action_open_my_profile(self):
        employee = self._get_my_employee()
        if employee:
            return {
                'type': 'ir.actions.act_window',
                'name': _('Ho so cua toi'),
                'res_model': 'hr.employee',
                'view_mode': 'form',
                'res_id': employee.id,
            }
        return {
            'type': 'ir.actions.act_window',
            'name': _('Ho so cua toi'),
            'res_model': 'hr.employee',
            'view_mode': 'tree,form',
            'domain': [('id', '=', 0)],
        }

    def action_open_family(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Than nhan'),
            'res_model': 'btl.hr.family',
            'view_mode': 'tree,form',
        }

    def action_open_work_history(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Qua trinh cong tac'),
            'res_model': 'btl.hr.work.history',
            'view_mode': 'tree,form',
        }