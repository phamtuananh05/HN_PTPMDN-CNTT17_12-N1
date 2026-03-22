from odoo import api, fields, models


class BtlHrFamily(models.Model):
    _name = 'btl.hr.family'
    _description = 'Than nhan nhan vien'
    _order = 'id desc'

    employee_id = fields.Many2one('hr.employee', string='Nhan vien', required=True, ondelete='cascade')
    name = fields.Char(string='Ho ten', required=True)
    relationship = fields.Selection(
        [
            ('vo', 'Vo'),
            ('chong', 'Chong'),
            ('con', 'Con'),
            ('bo', 'Bo'),
            ('me', 'Me'),
            ('khac', 'Khac'),
        ],
        string='Moi quan he',
        required=True,
        default='khac',
    )
    birth_date = fields.Date(string='Ngay sinh')
    age = fields.Integer(string='Tuoi', compute='_compute_age', store=True)
    is_dependent = fields.Boolean(string='Nguoi phu thuoc', compute='_compute_is_dependent', store=True)
    phone = fields.Char(string='So dien thoai')
    note = fields.Text(string='Ghi chu')

    @api.depends('birth_date')
    def _compute_age(self):
        today = fields.Date.context_today(self)
        for record in self:
            age = 0
            if record.birth_date:
                age = today.year - record.birth_date.year
                if (today.month, today.day) < (record.birth_date.month, record.birth_date.day):
                    age -= 1
            record.age = age

    @api.depends('relationship', 'age')
    def _compute_is_dependent(self):
        for record in self:
            record.is_dependent = bool(record.relationship == 'con' and record.age < 18)