from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_student = fields.Boolean(string="Is a Student", default=False)
    borrowed_books_count = fields.Integer(compute='_compute_borrowed_books_count', string="Books Borrowed")

    @api.depends('library_book_ids')
    def _compute_borrowed_books_count(self):
        for record in self:
            record.borrowed_books_count = self.env['library.book'].search_count([('student_id', '=', record.id)])

    library_book_ids = fields.One2many('library.book', 'student_id', string="Borrowed Books")
