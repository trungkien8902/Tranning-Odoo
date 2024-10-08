from odoo import fields, models, api
from odoo.api import ondelete
from odoo.exceptions import UserError
from odoo.fields import Many2one, Boolean

class EmployeeSkills(models.Model):
    _name = "employee.skill"
    _description = "Employee Skill"

    name = fields.Char(string="Skills Name", required=True)
    description = fields.Char(string="Skills Description")
    proficiency_level = fields.Selection([
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert')
    ], string="Proficiency Level", default='beginner')
    employee_ids = fields.Many2many(
        'hr.employee',
        'employee_skill_rel',
        'skill_id',
        'employee_id',
        string="Employees"
    )
    certification_id = fields.Many2one(
        'employee.certification',
        string="Certification",
        ondelete='restrict',
        required=True
    )

    @api.model
    def check_skill_manager_rights(self):
        if not self.env.user.has_group('hr_employee.group_skill_manager'):
            raise UserError("You do not have the necessary permissions to access this skill.")