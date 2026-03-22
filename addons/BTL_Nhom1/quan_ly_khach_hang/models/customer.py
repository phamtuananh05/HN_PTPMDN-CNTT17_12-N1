from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class BtlCustomer(models.Model):
    _name = 'btl.customer'
    _description = 'Khach hang'
    _order = 'id desc'

    name = fields.Char(string='Ten khach hang', required=True)
    code = fields.Char(string='Ma khach hang', readonly=True, copy=False, default='New')
    company_type = fields.Selection(
        [('ca_nhan', 'Ca nhan'), ('doanh_nghiep', 'Doanh nghiep')],
        string='Loai khach hang',
        default='doanh_nghiep',
        required=True,
    )
    phone = fields.Char(string='So dien thoai')
    email = fields.Char(string='Email')
    address = fields.Text(string='Dia chi')
    tax_code = fields.Char(string='Ma so thue')
    rank = fields.Selection(
        [('dong', 'Dong'), ('bac', 'Bac'), ('vang', 'Vang')],
        string='Hang khach hang',
        default='dong',
        required=True,
    )
    state = fields.Selection(
        [
            ('moi', 'Moi'),
            ('dang_cham_soc', 'Dang cham soc'),
            ('tiem_nang', 'Tiem nang'),
            ('ky_hop_dong', 'Ky hop dong'),
            ('ngung_hop_tac', 'Ngung hop tac'),
        ],
        string='Trang thai',
        default='moi',
        required=True,
    )
    employee_id = fields.Many2one('hr.employee', string='Nhan vien phu trach', required=True)
    department_id = fields.Many2one(
        'hr.department',
        string='Phong ban',
        related='employee_id.department_id',
        store=True,
        readonly=True,
    )
    next_care_date = fields.Date(string='Ngay cham soc tiep theo')
    last_care_date = fields.Date(string='Lan cham soc gan nhat')
    note = fields.Text(string='Ghi chu')
    active = fields.Boolean(default=True)
    contact_ids = fields.One2many('btl.customer.contact', 'customer_id', string='Nguoi lien he')
    contact_count = fields.Integer(string='So nguoi lien he', compute='_compute_contact_count')

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'Ma khach hang phai la duy nhat.'),
    ]

    @api.depends('contact_ids')
    def _compute_contact_count(self):
        for record in self:
            record.contact_count = len(record.contact_ids)

    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code('btl.customer') or 'New'
        return super().create(vals)

    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if record.email and '@' not in record.email:
                raise ValidationError(_('Email khong hop le.'))

    @api.constrains('next_care_date', 'last_care_date')
    def _check_care_dates(self):
        for record in self:
            if record.next_care_date and record.last_care_date and record.next_care_date < record.last_care_date:
                raise ValidationError(_('Ngay cham soc tiep theo khong duoc nho hon lan cham soc gan nhat.'))

    def action_open_contacts(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Nguoi lien he'),
            'res_model': 'btl.customer.contact',
            'view_mode': 'tree,form',
            'domain': [('customer_id', '=', self.id)],
            'context': {'default_customer_id': self.id},
        }