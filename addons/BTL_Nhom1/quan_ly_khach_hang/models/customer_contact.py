from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class BtlCustomerContact(models.Model):
    _name = 'btl.customer.contact'
    _description = 'Nguoi lien he khach hang'
    _order = 'is_primary desc, id desc'

    customer_id = fields.Many2one('btl.customer', string='Khach hang', required=True, ondelete='cascade')
    name = fields.Char(string='Ten nguoi lien he', required=True)
    position = fields.Char(string='Chuc vu')
    phone = fields.Char(string='So dien thoai')
    email = fields.Char(string='Email')
    birthday = fields.Date(string='Ngay sinh')
    is_primary = fields.Boolean(string='Lien he chinh')
    note = fields.Text(string='Ghi chu')

    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if record.email and '@' not in record.email:
                raise ValidationError(_('Email nguoi lien he khong hop le.'))