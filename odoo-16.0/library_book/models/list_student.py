from pkg_resources import require

from odoo import models, fields, api

class ListStudent(models.Model):
    _name = 'list.student'

    name = fields.Char(string="Name", required=True)
    student_code = fields.Char(string="Student Code", required=True)
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")

    book_ids = fields.Many2many(
        'library.book',
        'student_id',
        string="Borrowed Books"
    )
    is_student = fields.Boolean(string="Is a Student", default=False)

    book_count = fields.Integer(string="Number of Borrowed Books", compute='_compute_book_count', store=True)

    @api.depends('book_ids')
    def _compute_book_count(self):
        for student in self:
            student.book_count = len(student.book_ids) if student.book_ids else 0

    # @api.model
    # def create(self, vals):
    #     record = super(ListStudent, self).create(vals)
    #     if 'borrowed_books_ids' in vals:
    #         for book in record.borrowed_books_ids:
    #             book.student_ids = [(4, record.id)]
    #     return record
    #
    # def write(self, vals):
    #     result = super(ListStudent, self).write(vals)
    #     if 'borrowed_books_ids' in vals:
    #         for record in self:
    #             # Cập nhật lại student_ids của từng cuốn sách được thêm vào danh sách
    #             for book in record.borrowed_books_ids:
    #                 if record.id not in book.student_ids.ids:
    #                     book.student_ids = [(4, record.id)]
    #     return result

