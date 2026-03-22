from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import re


class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    que_quan = fields.Char(string='Que quan')
    so_cccd = fields.Char(string='So CCCD')
    ngay_cap_cccd = fields.Date(string='Ngay cap CCCD')
    noi_cap_cccd = fields.Char(string='Noi cap CCCD')
    sdt_khan_cap = fields.Char(string='SDT khan cap')
    ghi_chu_noi_bo = fields.Text(string='Ghi chu noi bo')

    family_ids = fields.One2many('btl.hr.family', 'employee_id', string='Than nhan')
    work_history_ids = fields.One2many('btl.hr.work.history', 'employee_id', string='Qua trinh cong tac')

    family_count = fields.Integer(string='So than nhan', compute='_compute_related_counts')
    work_history_count = fields.Integer(string='So lan cong tac', compute='_compute_related_counts')

    _sql_constraints = [
        ('so_cccd_unique', 'unique(so_cccd)', 'So CCCD phai la duy nhat.'),
    ]

    @api.depends('family_ids', 'work_history_ids')
    def _compute_related_counts(self):
        for record in self:
            record.family_count = len(record.family_ids)
            record.work_history_count = len(record.work_history_ids)

    def _validate_date_rules(self, birthday_value=None, ngay_cap_cccd_value=None):
        today = fields.Date.to_date(fields.Date.context_today(self))

        birthday_date = fields.Date.to_date(birthday_value) if birthday_value else False
        ngay_cap_cccd_date = fields.Date.to_date(ngay_cap_cccd_value) if ngay_cap_cccd_value else False

        if birthday_date and birthday_date >= today:
            raise ValidationError(_('Ngay sinh phai nho hon ngay hien tai.'))

        if ngay_cap_cccd_date and ngay_cap_cccd_date >= today:
            raise ValidationError(_('Ngay cap CCCD phai nho hon ngay hien tai.'))

    def _validate_email_rule(self, email_value=None):
        if not email_value:
            return

        email = (email_value or '').strip()
        pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

        if not re.match(pattern, email):
            raise ValidationError(_('Email cong viec khong dung dinh dang.'))

    @api.constrains('birthday', 'ngay_cap_cccd')
    def _check_dates(self):
        for record in self:
            record._validate_date_rules(
                birthday_value=record.birthday,
                ngay_cap_cccd_value=record.ngay_cap_cccd,
            )

    @api.constrains('work_email')
    def _check_work_email(self):
        for record in self:
            record._validate_email_rule(record.work_email)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            self._validate_date_rules(
                birthday_value=vals.get('birthday'),
                ngay_cap_cccd_value=vals.get('ngay_cap_cccd'),
            )
            self._validate_email_rule(vals.get('work_email'))
        return super().create(vals_list)

    def write(self, vals):
        for record in self:
            birthday_value = vals.get('birthday', record.birthday)
            ngay_cap_cccd_value = vals.get('ngay_cap_cccd', record.ngay_cap_cccd)
            email_value = vals.get('work_email', record.work_email)

            record._validate_date_rules(
                birthday_value=birthday_value,
                ngay_cap_cccd_value=ngay_cap_cccd_value,
            )
            record._validate_email_rule(email_value)

        return super().write(vals)

    def action_open_family(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Than nhan'),
            'res_model': 'btl.hr.family',
            'view_mode': 'tree,form',
            'domain': [('employee_id', '=', self.id)],
            'context': {'default_employee_id': self.id},
        }

    def action_open_work_history(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Qua trinh cong tac'),
            'res_model': 'btl.hr.work.history',
            'view_mode': 'tree,form',
            'domain': [('employee_id', '=', self.id)],
            'context': {'default_employee_id': self.id},
        }