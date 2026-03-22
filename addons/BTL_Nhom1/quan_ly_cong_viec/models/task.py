from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class BtlTask(models.Model):
    _name = 'btl.task'
    _description = 'Cong viec'
    _order = 'id desc'

    name = fields.Char(string='Ten cong viec', required=True)
    code = fields.Char(string='Ma cong viec', readonly=True, copy=False, default='New')
    task_type = fields.Selection(
        [
            ('goi_dien', 'Goi dien'),
            ('tu_van_1', 'Tu van lan 1'),
            ('gui_bao_gia', 'Gui bao gia'),
            ('hen_gap', 'Hen gap'),
            ('ky_hop_dong', 'Ky hop dong'),
            ('cham_soc', 'Cham soc'),
            ('khac', 'Khac'),
        ],
        string='Loai cong viec',
        required=True,
        default='goi_dien',
    )
    customer_id = fields.Many2one('btl.customer', string='Khach hang', required=True)
    contact_person_id = fields.Many2one(
        'btl.customer.contact',
        string='Nguoi lien he',
        domain="[('customer_id', '=', customer_id)]",
    )
    customer_rank = fields.Selection(
        related='customer_id.rank',
        string='Hang khach hang',
        store=True,
        readonly=True,
    )
    employee_id = fields.Many2one(
        'hr.employee',
        string='Nhan vien phu trach',
        required=True,
        default=lambda self: self._default_employee_id(),
    )
    department_id = fields.Many2one(
        'hr.department',
        string='Phong ban',
        related='employee_id.department_id',
        store=True,
        readonly=True,
    )
    stage_id = fields.Many2one(
        'btl.task.stage',
        string='Giai doan',
        required=True,
        default=lambda self: self._default_stage_id(),
    )
    is_done = fields.Boolean(
        related='stage_id.is_done',
        string='Da hoan thanh',
        store=True,
        readonly=True,
    )
    priority = fields.Selection(
        [
            ('0', 'Thap'),
            ('1', 'Trung binh'),
            ('2', 'Cao'),
            ('3', 'Khan'),
        ],
        string='Do uu tien',
        default='1',
        required=True,
    )
    planned_date = fields.Date(string='Ngay bat dau', default=lambda self: fields.Date.context_today(self))
    deadline_date = fields.Date(string='Han xu ly')
    completed_date = fields.Date(string='Ngay hoan thanh', readonly=True)
    description = fields.Text(string='Mo ta')
    is_overdue = fields.Boolean(string='Qua han', default=False)
    followup_created = fields.Boolean(string='Da tao follow-up', default=False)
    last_reminder_date = fields.Date(string='Ngay nhac gan nhat', readonly=True)
    active = fields.Boolean(default=True)

    parent_task_id = fields.Many2one('btl.task', string='Cong viec goc', ondelete='set null')
    child_task_ids = fields.One2many('btl.task', 'parent_task_id', string='Cong viec follow-up')
    child_task_count = fields.Integer(string='So follow-up', compute='_compute_child_task_count')

    reminder_ids = fields.One2many('btl.task.reminder', 'task_id', string='Nhat ky nhac viec')
    reminder_count = fields.Integer(string='So lan nhac', compute='_compute_reminder_count')

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'Ma cong viec phai la duy nhat.'),
    ]

    def _default_stage_id(self):
        stage = self.env['btl.task.stage'].search([], order='sequence, id', limit=1)
        return stage.id

    def _default_employee_id(self):
        employee = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1)
        return employee.id

    @api.depends('child_task_ids')
    def _compute_child_task_count(self):
        for record in self:
            record.child_task_count = len(record.child_task_ids)

    @api.depends('reminder_ids')
    def _compute_reminder_count(self):
        for record in self:
            record.reminder_count = len(record.reminder_ids)

    @api.constrains('deadline_date', 'planned_date')
    def _check_dates(self):
        for record in self:
            if record.deadline_date and record.planned_date and record.deadline_date < record.planned_date:
                raise ValidationError(_('Han xu ly khong duoc nho hon ngay bat dau.'))

    @api.constrains('contact_person_id', 'customer_id')
    def _check_contact_customer(self):
        for record in self:
            if record.contact_person_id and record.contact_person_id.customer_id != record.customer_id:
                raise ValidationError(_('Nguoi lien he phai thuoc dung khach hang da chon.'))

    def _build_description_text(self, customer=False, contact=False):
        customer = customer or self.customer_id
        contact = contact or self.contact_person_id

        lines = []
        if customer:
            lines.append('THONG TIN KHACH HANG')
            lines.append('Khach hang: %s' % (customer.name or ''))
            lines.append('So dien thoai: %s' % (customer.phone or ''))
            lines.append('Email: %s' % (customer.email or ''))
            lines.append('Dia chi: %s' % (customer.address or ''))
            lines.append('Hang khach hang: %s' % (dict(customer._fields['rank'].selection).get(customer.rank, '')))

        if contact:
            lines.append('')
            lines.append('NGUOI LIEN HE')
            lines.append('Ho ten: %s' % (contact.name or ''))
            lines.append('Chuc vu: %s' % (contact.position or ''))
            lines.append('So dien thoai: %s' % (contact.phone or ''))
            lines.append('Email: %s' % (contact.email or ''))

        return '\n'.join(lines)

    @api.onchange('customer_id')
    def _onchange_customer_id(self):
        if not self.customer_id:
            self.contact_person_id = False
            self.description = False
            return

        primary_contact = self.customer_id.contact_ids.filtered(lambda x: x.is_primary)[:1]
        if primary_contact:
            self.contact_person_id = primary_contact.id
        elif self.customer_id.contact_ids:
            self.contact_person_id = self.customer_id.contact_ids[:1].id
        else:
            self.contact_person_id = False

        if self.customer_id.employee_id:
            self.employee_id = self.customer_id.employee_id.id

        if self.customer_id.rank == 'vang' and self.priority in (False, '0', '1'):
            self.priority = '2'

        self.description = self._build_description_text(self.customer_id, self.contact_person_id)

    @api.onchange('contact_person_id')
    def _onchange_contact_person_id(self):
        if self.customer_id:
            self.description = self._build_description_text(self.customer_id, self.contact_person_id)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('code', 'New') == 'New':
                vals['code'] = self.env['ir.sequence'].next_by_code('btl.task') or 'New'
            if not vals.get('stage_id'):
                vals['stage_id'] = self._default_stage_id()

        records = super().create(vals_list)

        if not self.env.context.get('skip_sync_task'):
            records._sync_task_flags()

        if not self.env.context.get('skip_vip_priority'):
            records._apply_vip_priority()

        if not self.env.context.get('skip_followup'):
            records._create_followup_if_needed()

        return records

    def write(self, vals):
        res = super().write(vals)

        if not self.env.context.get('skip_sync_task'):
            self._sync_task_flags()

        if not self.env.context.get('skip_vip_priority'):
            self._apply_vip_priority()

        if not self.env.context.get('skip_followup'):
            self._create_followup_if_needed()

        return res

    def _sync_task_flags(self):
        today = fields.Date.to_date(fields.Date.context_today(self))
        for record in self:
            vals = {}

            new_completed_date = fields.Date.to_string(today) if record.is_done else False
            if record.completed_date != new_completed_date:
                vals['completed_date'] = new_completed_date

            overdue = bool(record.deadline_date and record.deadline_date < today and not record.is_done)
            if record.is_overdue != overdue:
                vals['is_overdue'] = overdue

            if vals:
                super(BtlTask, record.with_context(
                    skip_sync_task=True,
                    skip_vip_priority=True,
                    skip_followup=True
                )).write(vals)

    def _apply_vip_priority(self):
        for record in self:
            if record.customer_rank == 'vang' and record.priority in ('0', '1'):
                super(BtlTask, record.with_context(
                    skip_sync_task=True,
                    skip_vip_priority=True,
                    skip_followup=True
                )).write({'priority': '2'})

    def _create_followup_if_needed(self):
        next_stage = self.env['btl.task.stage'].search([('is_done', '=', False)], order='sequence, id', limit=1)
        today = fields.Date.to_date(fields.Date.context_today(self))

        for record in self:
            if not record.is_done:
                continue
            if record.followup_created:
                continue
            if record.task_type not in ('gui_bao_gia', 'tu_van_1'):
                continue

            completed_date = fields.Date.to_date(record.completed_date or fields.Date.context_today(self))
            next_deadline = completed_date + timedelta(days=3)

            if record.task_type == 'gui_bao_gia':
                followup_name = 'Goi lai sau bao gia - %s' % (record.customer_id.name or '')
                followup_type = 'cham_soc'
            else:
                followup_name = 'Hen gap sau tu van - %s' % (record.customer_id.name or '')
                followup_type = 'hen_gap'

            self.create({
                'name': followup_name,
                'task_type': followup_type,
                'customer_id': record.customer_id.id,
                'contact_person_id': record.contact_person_id.id or False,
                'employee_id': record.employee_id.id,
                'stage_id': next_stage.id or record.stage_id.id,
                'priority': '2' if record.customer_rank == 'vang' else '1',
                'planned_date': fields.Date.to_string(today),
                'deadline_date': fields.Date.to_string(next_deadline),
                'description': 'Cong viec follow-up tu %s (%s)' % (record.name or '', record.code or ''),
                'parent_task_id': record.id,
            })

            super(BtlTask, record.with_context(
                skip_sync_task=True,
                skip_vip_priority=True,
                skip_followup=True
            )).write({'followup_created': True})

    def action_move_to_in_progress(self):
        stage = self.env['btl.task.stage'].search([('code', '=', 'dang_thuc_hien')], limit=1)
        if stage:
            self.write({'stage_id': stage.id})

    def action_move_to_done(self):
        stage = self.env['btl.task.stage'].search([('is_done', '=', True)], order='sequence, id', limit=1)
        if stage:
            self.write({'stage_id': stage.id})

    def action_open_followups(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Cong viec follow-up'),
            'res_model': 'btl.task',
            'view_mode': 'tree,form',
            'domain': [('parent_task_id', '=', self.id)],
            'context': {'default_parent_task_id': self.id},
        }

    def action_open_reminders(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Nhat ky nhac viec'),
            'res_model': 'btl.task.reminder',
            'view_mode': 'tree,form',
            'domain': [('task_id', '=', self.id)],
            'context': {'default_task_id': self.id},
        }

    @api.model
    def cron_check_overdue_tasks(self):
        today = fields.Date.to_date(fields.Date.context_today(self))

        all_tasks = self.search([('active', '=', True)])
        for task in all_tasks:
            overdue = bool(task.deadline_date and task.deadline_date < today and not task.is_done)
            if task.is_overdue != overdue:
                super(BtlTask, task.with_context(
                    skip_sync_task=True,
                    skip_vip_priority=True,
                    skip_followup=True
                )).write({'is_overdue': overdue})

        overdue_tasks = self.search([
            ('active', '=', True),
            ('deadline_date', '<', today),
            ('is_done', '=', False),
        ])

        for task in overdue_tasks:
            if task.last_reminder_date == today:
                continue

            vals = {
                'last_reminder_date': fields.Date.to_string(today),
            }
            if task.priority in ('0', '1', '2'):
                vals['priority'] = '3'

            super(BtlTask, task.with_context(
                skip_sync_task=True,
                skip_vip_priority=True,
                skip_followup=True
            )).write(vals)

            self.env['btl.task.reminder'].create({
                'name': 'Nhac viec qua han - %s' % (task.code or task.name or ''),
                'task_id': task.id,
                'employee_id': task.employee_id.id,
                'reminder_date': fields.Date.to_string(today),
                'note': 'Cong viec da qua han va he thong tu dong tao nhac viec.',
            })