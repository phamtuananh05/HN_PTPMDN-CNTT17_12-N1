from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class BtlHrWorkHistory(models.Model):
    _name = 'btl.hr.work.history'
    _description = 'Qua trinh cong tac'
    _order = 'date_start desc, id desc'

    employee_id = fields.Many2one('hr.employee', string='Nhan vien', required=True, ondelete='cascade')
    company_name = fields.Char(string='Don vi cong tac', required=True)
    position = fields.Char(string='Chuc vu')
    date_start = fields.Date(string='Tu ngay', required=True)
    date_end = fields.Date(string='Den ngay')
    note = fields.Text(string='Ghi chu')

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for record in self:
            if record.date_start and record.date_end and record.date_end < record.date_start:
                raise ValidationError(_('Ngay ket thuc khong duoc nho hon ngay bat dau.'))