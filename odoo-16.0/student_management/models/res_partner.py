from odoo import fields, models, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_student = fields.Boolean(default=False, string="Is a Student")
    student_id = fields.Many2one('student.management', string="Linked Student")
