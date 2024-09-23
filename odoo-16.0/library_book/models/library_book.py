from odoo import fields, models, api


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    code = fields.Char(string="Book Code", required=True, default=lambda self: self._generate_book_code(),
                       readonly=True)
    name = fields.Char(string="Book Name", required=True)
    publish_year = fields.Date(string="Publish Year")
    author = fields.Char(string="Author")
    student_id = fields.Many2one(
        'list.student',
        string="Borrowed by Students",
        domain=[('is_student', '=', True)]
    )
    count_student_borrow = fields.Integer(compute='_compute_count_student_borrow', string="Number of Students")

    @api.model
    def _generate_book_code(self):
        last_code = self.search([], order='id desc', limit=1).code
        new_code = int(last_code[2:]) + 1 if last_code else 1
        return f'TV{str(new_code).zfill(5)}'

    @api.depends('student_id')
    def _compute_count_student_borrow(self):
        for record in self:
            if record.student_id:
                record.count_student_borrow = 1
            else:
                record.count_student_borrow = 0
