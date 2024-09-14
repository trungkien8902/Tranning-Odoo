from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_student = fields.Boolean(string="Là sinh viên")
    student_id = fields.Many2one('student.student', string="Sinh viên", domain="[('id', '!=', False)]")
