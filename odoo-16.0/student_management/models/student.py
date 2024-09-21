from odoo import models, fields

class Student(models.Model):
    _inherit = 'student.management'

    def action_open_partner_contacts(self):
        return {
            'name': 'Contacts',
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'view_mode': 'tree,form',
            'domain': [('student_id', '=', self.id)],
            'context': {'default_student_id': self.id},
        }
