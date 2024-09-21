from pkg_resources import require

from odoo import models, fields, api

class ListStudent(models.Model):
    _name = 'list.student'

    name = fields.Char(string="Name", required=True)
    student_code = fields.Char(string="Student Code", required=True)
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")

    book_ids = fields.One2many('library.book', 'student_id', string="Borrowed Books")
    is_student = fields.Boolean(string="Is a Student", default=False)

    book_count = fields.Integer(string="Number of Borrowed Books", compute='_compute_book_count', store=True)

    @api.depends('book_ids')
    def _compute_book_count(self):
        for record in self:
            # Đếm số lượng sách đã mượn dựa trên trường One2many book_ids
            record.book_count = len(record.book_ids)
