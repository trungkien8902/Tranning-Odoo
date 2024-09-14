from email.policy import default
from odoo.exceptions import ValidationError
from odoo import models, fields, api

class Student(models.Model):
    _name = 'student.student'
    _description = 'Student'

    name = fields.Char(string="Tên sinh viên", required=True)
    student_code = fields.Char(string="Mã sinh viên", required=True)
    display_name = fields.Char(string="Tên hiển thị", compute="_compute_display_name", store=True, readonly=True)
    birthdate = fields.Date(string="Ngày sinh")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Số điện thoại")
    last_seen = fields.Datetime()
    active = fields.Boolean(string="Đang Hoạt Động", default=True)

    _sql_constraints = [
        ('student_code_unique', 'unique(student_code)', 'Mã sinh viên đã tồn tại, vui lòng nhập mã sinh viên khác!')
    ]

    @api.depends('name', 'student_code')
    def _compute_display_name(self):
        for record in self:
            if record.student_code and record.name:
                record.display_name = f'{record.student_code} - {record.name}'
            else:
                record.display_name = ''

    @api.model
    def create(self, vals):
        # Kiểm tra xem mã sinh viên đã tồn tại chưa
        if self.search([('student_code', '=', vals.get('student_code'))]):
            raise ValidationError("Mã sinh viên đã tồn tại, vui lòng nhập mã sinh viên khác!")
        return super(Student, self).create(vals)

    # Kiểm tra mã sinh viên trước khi cập nhật bản ghi
    def write(self, vals):
        if 'student_code' in vals:
            # Kiểm tra nếu mã sinh viên mới đã tồn tại
            if self.search([('student_code', '=', vals.get('student_code')), ('id', '!=', self.id)]):
                raise ValidationError("Mã sinh viên đã tồn tại, vui lòng nhập mã sinh viên khác!")
        return super(Student, self).write(vals)

    # Button để mở tất cả liên hệ liên quan tới sinh viên này
    def action_open_partner_contacts(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Liên Hệ Sinh Viên',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'res.partner',
            'domain': [('student_id', '=', self.id)],
            'context': dict(self._context),
        }