from odoo import fields, models


class BtlTaskStage(models.Model):
    _name = 'btl.task.stage'
    _description = 'Tien trinh cong viec'
    _order = 'sequence, id'

    name = fields.Char(string='Ten giai doan', required=True)
    code = fields.Selection(
        [
            ('moi', 'Moi'),
            ('dang_thuc_hien', 'Dang thuc hien'),
            ('cho_phan_hoi', 'Cho phan hoi'),
            ('hoan_thanh', 'Hoan thanh'),
            ('huy', 'Huy'),
        ],
        string='Ma giai doan',
        required=True,
        default='moi',
    )
    sequence = fields.Integer(string='Thu tu', default=10)
    is_done = fields.Boolean(string='La giai doan hoan thanh')
    fold = fields.Boolean(string='Thu gon tren kanban')

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'Ma giai doan phai la duy nhat.'),
    ]