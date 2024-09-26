from odoo import fields, models, api
from odoo.api import ondelete
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
    years_of_experience = fields.Integer(string="Years of Experience", help="Years of experience with this skill")
    employee_ids = fields.Many2one('hr.employee', ondelete='cascade')
