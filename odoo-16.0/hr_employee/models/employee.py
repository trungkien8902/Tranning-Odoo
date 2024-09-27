from email.policy import default

from odoo import fields, models, api
from odoo.tools.populate import compute


class Employee(models.Model):
    _inherit = "hr.employee"

    years_of_experience = fields.Integer(compute="_compute_years_of_experience", string="Experience Year")
    certification_ids = fields.Many2many('employee.certification', string="Certifications")
    skill_ids = fields.Many2many('employee.skill', string="Skills")

    is_manager = fields.Boolean(string="Is HR Manager", compute="_compute_is_manager", store=False, default=True)

    @api.depends('user_id')
    def _compute_is_manager(self):
        for record in self:
            record.is_manager = self.env.user.has_group('base.group_user')

    @api.depends('certification_ids', 'skill_ids')
    def _compute_years_of_experience(self):
        for employee in self:
            years_of_experience = 0
            if employee.certification_ids:
                for cert in employee.certification_ids:
                    if cert.date_received:
                        years_of_experience += (fields.Date.today().year - cert.date_received.year)
            for skill in employee.skill_ids:
                if skill.proficiency_level == 'beginner':
                    years_of_experience += 1
                elif skill.proficiency_level == 'intermediate':
                    years_of_experience += 2
                elif skill.proficiency_level == 'advanced':
                    years_of_experience += 3
                elif skill.proficiency_level == 'expert':
                    years_of_experience += 4
            employee.years_of_experience = years_of_experience