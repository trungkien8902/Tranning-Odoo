from odoo import fields, models, api

class Employee(models.Model):
    _inherit = "hr.employee"

    years_of_experience = fields.Char(string="Experience Year")
    certifications_id = fields.One2many('employee.certifications', 'employee_id', string="Certifications")
    skills_id = fields.One2many('employee.skills', 'employee_id', string="Skills")

    @api.depends('skills_id', 'certifications_id')
    def _compute_years_of_experience(self):
        for record in self:
            experience_from_certs = sum(cert.years for cert in record.certification_ids)
            experience_from_skills = sum(skill.years_of_experience for skill in record.skill_ids)
            record.years_of_experience = experience_from_certs + experience_from_skills