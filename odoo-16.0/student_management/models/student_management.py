from email.policy import default

from Tools.scripts.dutree import store
from pkg_resources import require
from odoo import fields, models, api
from odoo.fields import Many2one, Boolean


class StudentManagement(models.Model):
    _name = "student.management"
    _description = "Student Infomation"

    name = fields.Char(string="Student Name", required=True, size=50)
    student_code = fields.Char(string="Student Code", required=True, size=10)
    display_name = fields.Char(compute='_compute_display_name', string='Display Name', store=True)
    birthdate = fields.Date(string='Date of Birth')
    email = fields.Char(string='Email', required=True)
    phone = fields.Char(string='Phone Number', required=True)

    is_student = Boolean(default=False, string="Is Student")

    _sql_constraints = [
        ('student_code_unique', 'unique(student_code', 'Mã sinh viên đã tồn tại, vui lòng nhập mã sinh viên khác!')
    ]

    @api.depends('name', 'student_code')
    def _compute_display_name(self):
        for record in self:
            if record.student_code and record.name:
                record.display_name = f"{record.student_code} - {record.name}"
            else:
                record.display_name = ""
